from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import base64
import json
import tweepy
import tempfile
import io
import requests
from requests_oauthlib import OAuth2Session
import httpx

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Twitter API v2 Client Setup
twitter_client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_API_SECRET"),
    access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    wait_on_rate_limit=True
)

# Twitter API v1.1 for media uploads
twitter_auth = tweepy.OAuth1UserHandler(
    os.environ.get("TWITTER_API_KEY"),
    os.environ.get("TWITTER_API_SECRET"),
    os.environ.get("TWITTER_ACCESS_TOKEN"),
    os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
)
twitter_api = tweepy.API(twitter_auth)

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = "http://localhost:8000/auth/linkedin/callback"
LINKEDIN_AUTHORIZATION_BASE_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# TikTok Business API Configuration
TIKTOK_CLIENT_KEY = os.environ.get("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")
TIKTOK_BASE_URL = "https://business-api.tiktok.com/open_api/v1.3"

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class SocialAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str  # twitter, facebook, instagram, linkedin, tiktok, youtube, pinterest
    username: str
    access_token: str
    refresh_token: Optional[str] = None
    account_id: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SocialAccountCreate(BaseModel):
    platform: str
    username: str
    access_token: str
    refresh_token: Optional[str] = None
    account_id: str

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    media_files: List[str] = []  # base64 encoded media
    platforms: List[str] = []  # which platforms to post to
    status: str = "draft"  # draft, scheduled, published, failed
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = "default_user"  # for MVP, single user
    analytics: Dict[str, Any] = {}
    social_post_ids: Dict[str, str] = {}  # platform -> post_id mapping

class PostCreate(BaseModel):
    title: str
    content: str
    media_files: List[str] = []
    platforms: List[str] = []
    scheduled_time: Optional[datetime] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    media_files: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    status: Optional[str] = None
    scheduled_time: Optional[datetime] = None

class Analytics(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str
    platform: str
    likes: int = 0
    shares: int = 0
    comments: int = 0
    reach: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TwitterPostRequest(BaseModel):
    text: str
    media_files: List[str] = []  # base64 encoded media

class LinkedInPostRequest(BaseModel):
    text: str
    visibility: str = "PUBLIC"  # PUBLIC, CONNECTIONS
    media_url: Optional[str] = None

class LinkedInAuthRequest(BaseModel):
    access_token: str

class TikTokVideoRequest(BaseModel):
    title: str
    description: str = ""
    privacy_level: str = "PUBLIC_TO_EVERYONE"

class TikTokAuthRequest(BaseModel):
    access_token: str
    advertiser_id: str

# TikTok Client Class
class TikTokClient:
    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.headers = {
            "Access-Token": access_token,
            "Content-Type": "application/json"
        }
    
    async def upload_video(self, video_content: bytes, title: str, description: str = "") -> Dict[str, Any]:
        """Upload video to TikTok"""
        try:
            # Initialize video upload
            async with httpx.AsyncClient() as http_client:
                init_response = await http_client.post(
                    f"{TIKTOK_BASE_URL}/file/video/ad/upload/",
                    headers=self.headers,
                    json={
                        "advertiser_id": self.advertiser_id,
                        "upload_type": "UPLOAD_BY_FILE",
                        "video_file_size": len(video_content)
                    }
                )
                
                init_result = init_response.json()
                
                if init_result.get("code") != 0:
                    return {
                        'success': False,
                        'error': f"Upload init failed: {init_result.get('message')}",
                        'platform': 'tiktok'
                    }
                
                upload_url = init_result["data"]["upload_url"]
                video_id = init_result["data"]["video_id"]
                
                # Upload video content
                upload_response = await http_client.post(
                    upload_url,
                    files={"video": ("video.mp4", video_content, "video/mp4")}
                )
                
                if upload_response.status_code == 200:
                    return {
                        'success': True,
                        'post_id': video_id,
                        'platform': 'tiktok',
                        'upload_url': upload_url
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Video upload failed: {upload_response.text}",
                        'platform': 'tiktok'
                    }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': 'tiktok'
            }
    
    async def publish_video(self, video_id: str, privacy_level: str = "PUBLIC_TO_EVERYONE") -> Dict[str, Any]:
        """Publish uploaded video"""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{TIKTOK_BASE_URL}/video/publish/",
                    headers=self.headers,
                    json={
                        "advertiser_id": self.advertiser_id,
                        "video_id": video_id,
                        "privacy_level": privacy_level
                    }
                )
                
                result = response.json()
                
                if result.get("code") == 0:
                    return {'success': True, 'platform': 'tiktok'}
                else:
                    return {
                        'success': False,
                        'error': f"Publish failed: {result.get('message')}",
                        'platform': 'tiktok'
                    }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': 'tiktok'
            }

# Helper function to decode base64 media
def decode_base64_media(base64_data: str) -> bytes:
    """Decode base64 media data"""
    if base64_data.startswith('data:'):
        base64_data = base64_data.split(',')[1]
    return base64.b64decode(base64_data)

# Twitter Integration Functions
async def post_to_twitter(content: str, media_files: List[str] = None) -> Dict[str, Any]:
    """Post content to Twitter with optional media"""
    try:
        media_ids = []
        
        # Handle media uploads
        if media_files:
            for media_file in media_files:
                try:
                    # Decode base64 media
                    media_data = decode_base64_media(media_file)
                    
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                        temp_file.write(media_data)
                        temp_file_path = temp_file.name
                    
                    # Upload media to Twitter
                    media = twitter_api.media_upload(temp_file_path)
                    media_ids.append(media.media_id)
                    
                    # Clean up temp file
                    os.unlink(temp_file_path)
                except Exception as e:
                    logging.error(f"Error uploading media to Twitter: {str(e)}")
                    continue
        
        # Post tweet
        if media_ids:
            response = twitter_client.create_tweet(text=content, media_ids=media_ids)
        else:
            response = twitter_client.create_tweet(text=content)
        
        # Get tweet details for analytics
        tweet_id = response.data['id']
        tweet_details = twitter_client.get_tweet(
            tweet_id,
            tweet_fields=['created_at', 'public_metrics']
        )
        
        return {
            'success': True,
            'post_id': tweet_id,
            'platform': 'twitter',
            'metrics': tweet_details.data.public_metrics if tweet_details.data.public_metrics else {}
        }
        
    except Exception as e:
        logging.error(f"Error posting to Twitter: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'platform': 'twitter'
        }

# LinkedIn Integration Functions
async def post_to_linkedin(content: str, access_token: str, visibility: str = "PUBLIC", media_files: List[str] = None) -> Dict[str, Any]:
    """Post content to LinkedIn with optional media"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Get user profile to get person URN
        profile_response = requests.get(
            "https://api.linkedin.com/v2/people/~:(id)",
            headers=headers
        )
        
        if profile_response.status_code != 200:
            return {
                'success': False,
                'error': f"Failed to get user profile: {profile_response.text}",
                'platform': 'linkedin'
            }
        
        user_id = profile_response.json()["id"]
        
        # Basic text post payload
        payload = {
            "author": f"urn:li:person:{user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        # Post to LinkedIn
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            json=payload,
            headers=headers
        )
        
        if response.status_code != 201:
            return {
                'success': False,
                'error': f"LinkedIn API error: {response.text}",
                'platform': 'linkedin'
            }
        
        # Get post URN from response headers
        post_urn = response.headers.get("X-Restli-Id")
        
        return {
            'success': True,
            'post_id': post_urn,
            'platform': 'linkedin',
            'metrics': {}
        }
        
    except Exception as e:
        logging.error(f"Error posting to LinkedIn: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'platform': 'linkedin'
        }

# TikTok Integration Functions
async def post_to_tiktok(title: str, description: str, media_files: List[str], access_token: str, advertiser_id: str) -> Dict[str, Any]:
    """Post video content to TikTok"""
    try:
        if not media_files:
            return {
                'success': False,
                'error': 'TikTok requires video content',
                'platform': 'tiktok'
            }
        
        tiktok_client = TikTokClient(access_token, advertiser_id)
        
        # Use the first media file as video content
        video_content = decode_base64_media(media_files[0])
        
        # Upload video
        upload_result = await tiktok_client.upload_video(video_content, title, description)
        
        if upload_result['success']:
            video_id = upload_result['post_id']
            
            # Publish video
            publish_result = await tiktok_client.publish_video(video_id)
            
            if publish_result['success']:
                return {
                    'success': True,
                    'post_id': video_id,
                    'platform': 'tiktok',
                    'metrics': {}
                }
            else:
                return publish_result
        else:
            return upload_result
            
    except Exception as e:
        logging.error(f"Error posting to TikTok: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'platform': 'tiktok'
        }

# Original routes
@api_router.get("/")
async def root():
    return {"message": "Social Media Management Platform API with Twitter, LinkedIn & TikTok Integration"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# LinkedIn OAuth endpoints
@api_router.get("/auth/linkedin/login")
async def linkedin_login():
    """Initiate LinkedIn OAuth flow"""
    scope = ["r_liteprofile", "r_emailaddress", "w_member_social"]
    linkedin = OAuth2Session(LINKEDIN_CLIENT_ID, redirect_uri=LINKEDIN_REDIRECT_URI, scope=scope)
    authorization_url, state = linkedin.authorization_url(LINKEDIN_AUTHORIZATION_BASE_URL)
    
    return {
        "authorization_url": authorization_url,
        "state": state
    }

@api_router.get("/auth/linkedin/callback")
async def linkedin_callback(code: str, state: str = None):
    """Handle LinkedIn OAuth callback and exchange code for token"""
    try:
        linkedin = OAuth2Session(LINKEDIN_CLIENT_ID, redirect_uri=LINKEDIN_REDIRECT_URI)
        token = linkedin.fetch_token(
            LINKEDIN_TOKEN_URL,
            client_secret=LINKEDIN_CLIENT_SECRET,
            code=code,
            include_client_id=True
        )
        
        # Get user profile information
        headers = {
            "Authorization": f"Bearer {token['access_token']}",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        profile_response = requests.get(
            "https://api.linkedin.com/v2/people/~:(id,firstName,lastName)",
            headers=headers
        )
        
        if profile_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user profile")
        
        profile_data = profile_response.json()
        
        # Store user and token in MongoDB
        user_data = {
            "linkedin_id": profile_data["id"],
            "first_name": profile_data["firstName"]["localized"]["en_US"],
            "last_name": profile_data["lastName"]["localized"]["en_US"],
            "access_token": token["access_token"],
            "token_expires_at": datetime.utcnow() + timedelta(seconds=token.get("expires_in", 3600)),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Upsert user data
        await db.linkedin_users.insert_one(user_data)
        
        return {
            "access_token": token["access_token"],
            "user_id": profile_data["id"],
            "expires_in": token.get("expires_in", 3600),
            "first_name": profile_data["firstName"]["localized"]["en_US"],
            "last_name": profile_data["lastName"]["localized"]["en_US"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")

# Social Accounts Management
@api_router.post("/social-accounts", response_model=SocialAccount)
async def create_social_account(account: SocialAccountCreate):
    account_dict = account.dict()
    account_obj = SocialAccount(**account_dict)
    await db.social_accounts.insert_one(account_obj.dict())
    return account_obj

@api_router.get("/social-accounts", response_model=List[SocialAccount])
async def get_social_accounts():
    accounts = await db.social_accounts.find({"is_active": True}).to_list(1000)
    return [SocialAccount(**account) for account in accounts]

@api_router.delete("/social-accounts/{account_id}")
async def delete_social_account(account_id: str):
    result = await db.social_accounts.update_one(
        {"id": account_id},
        {"$set": {"is_active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}

# Posts Management
@api_router.post("/posts", response_model=Post)
async def create_post(post: PostCreate):
    post_dict = post.dict()
    post_obj = Post(**post_dict)
    await db.posts.insert_one(post_obj.dict())
    return post_obj

@api_router.get("/posts", response_model=List[Post])
async def get_posts(status: Optional[str] = None, limit: int = 50):
    query = {}
    if status:
        query["status"] = status
    
    posts = await db.posts.find(query).sort("created_at", -1).limit(limit).to_list(limit)
    return [Post(**post) for post in posts]

# Calendar view - get posts by date range
@api_router.get("/posts/calendar")
async def get_posts_calendar(start_date: str, end_date: str):
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    posts = await db.posts.find({
        "$or": [
            {"scheduled_time": {"$gte": start, "$lte": end}},
            {"published_time": {"$gte": start, "$lte": end}}
        ]
    }).sort("scheduled_time", 1).to_list(1000)
    
    return [Post(**post) for post in posts]

@api_router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: str):
    post = await db.posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**post)

@api_router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: str, post_update: PostUpdate):
    update_dict = {k: v for k, v in post_update.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.posts.update_one(
        {"id": post_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    updated_post = await db.posts.find_one({"id": post_id})
    return Post(**updated_post)

@api_router.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    result = await db.posts.delete_one({"id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

# Enhanced publish post to social media platforms
@api_router.post("/posts/{post_id}/publish")
async def publish_post(post_id: str, linkedin_auth: Optional[LinkedInAuthRequest] = None, tiktok_auth: Optional[TikTokAuthRequest] = None):
    post = await db.posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_obj = Post(**post)
    publish_results = {}
    
    # Publish to selected platforms
    for platform in post_obj.platforms:
        if platform == "twitter":
            result = await post_to_twitter(post_obj.content, post_obj.media_files)
            publish_results[platform] = result
            
            # Store social post ID and analytics
            if result['success']:
                post_obj.social_post_ids[platform] = result['post_id']
                
                # Create analytics entry
                analytics_data = Analytics(
                    post_id=post_id,
                    platform=platform,
                    likes=result['metrics'].get('like_count', 0),
                    shares=result['metrics'].get('retweet_count', 0),
                    comments=result['metrics'].get('reply_count', 0),
                    impressions=result['metrics'].get('impression_count', 0)
                )
                await db.analytics.insert_one(analytics_data.dict())
        
        elif platform == "linkedin":
            if linkedin_auth and linkedin_auth.access_token:
                result = await post_to_linkedin(post_obj.content, linkedin_auth.access_token, "PUBLIC", post_obj.media_files)
                publish_results[platform] = result
                
                # Store social post ID
                if result['success']:
                    post_obj.social_post_ids[platform] = result['post_id']
                    
                    # Create analytics entry
                    analytics_data = Analytics(
                        post_id=post_id,
                        platform=platform,
                        likes=0,  # LinkedIn analytics would need separate API call
                        shares=0,
                        comments=0,
                        impressions=0
                    )
                    await db.analytics.insert_one(analytics_data.dict())
            else:
                publish_results[platform] = {
                    'success': False,
                    'error': 'LinkedIn access token required',
                    'platform': platform
                }
        
        elif platform == "tiktok":
            if tiktok_auth and tiktok_auth.access_token and tiktok_auth.advertiser_id:
                result = await post_to_tiktok(post_obj.title, post_obj.content, post_obj.media_files, tiktok_auth.access_token, tiktok_auth.advertiser_id)
                publish_results[platform] = result
                
                # Store social post ID
                if result['success']:
                    post_obj.social_post_ids[platform] = result['post_id']
                    
                    # Create analytics entry
                    analytics_data = Analytics(
                        post_id=post_id,
                        platform=platform,
                        likes=0,  # TikTok analytics would need separate API call
                        shares=0,
                        comments=0,
                        impressions=0
                    )
                    await db.analytics.insert_one(analytics_data.dict())
            else:
                publish_results[platform] = {
                    'success': False,
                    'error': 'TikTok access token and advertiser ID required',
                    'platform': platform
                }
        else:
            # Placeholder for other platforms
            publish_results[platform] = {
                'success': False,
                'error': f'{platform} integration not yet implemented',
                'platform': platform
            }
    
    # Update post status
    status = "published" if any(r['success'] for r in publish_results.values()) else "failed"
    await db.posts.update_one(
        {"id": post_id},
        {"$set": {
            "status": status,
            "published_time": datetime.utcnow(),
            "social_post_ids": post_obj.social_post_ids,
            "analytics": publish_results
        }}
    )
    
    return {
        "message": "Post publishing completed",
        "results": publish_results
    }

# Twitter-specific endpoints
@api_router.post("/twitter/post")
async def post_tweet_direct(tweet_request: TwitterPostRequest):
    """Direct Twitter posting endpoint"""
    result = await post_to_twitter(tweet_request.text, tweet_request.media_files)
    
    if result['success']:
        return {
            "message": "Tweet posted successfully",
            "tweet_id": result['post_id'],
            "metrics": result['metrics']
        }
    else:
        raise HTTPException(status_code=400, detail=result['error'])

@api_router.get("/twitter/analytics/{tweet_id}")
async def get_twitter_analytics(tweet_id: str):
    """Get Twitter analytics for a specific tweet"""
    try:
        tweet = twitter_client.get_tweet(
            tweet_id,
            tweet_fields=['created_at', 'public_metrics']
        )
        
        return {
            "tweet_id": tweet_id,
            "text": tweet.data.text,
            "created_at": str(tweet.data.created_at),
            "metrics": tweet.data.public_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching Twitter analytics: {str(e)}")

# LinkedIn-specific endpoints
@api_router.post("/linkedin/post")
async def post_linkedin_direct(linkedin_request: LinkedInPostRequest, access_token: str):
    """Direct LinkedIn posting endpoint"""
    result = await post_to_linkedin(linkedin_request.text, access_token, linkedin_request.visibility)
    
    if result['success']:
        return {
            "message": "LinkedIn post created successfully",
            "post_urn": result['post_id'],
            "platform": "linkedin"
        }
    else:
        raise HTTPException(status_code=400, detail=result['error'])

@api_router.get("/linkedin/profile")
async def get_linkedin_profile(access_token: str):
    """Get LinkedIn user profile"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        response = requests.get(
            "https://api.linkedin.com/v2/people/~:(id,firstName,lastName,profilePicture(displayImage~:playableStreams))",
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch LinkedIn profile")
        
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching LinkedIn profile: {str(e)}")

# TikTok-specific endpoints
@api_router.post("/tiktok/upload")
async def upload_tiktok_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    access_token: str = Form(...),
    advertiser_id: str = Form(...)
):
    """Upload video to TikTok"""
    try:
        video_content = await file.read()
        tiktok_client = TikTokClient(access_token, advertiser_id)
        
        result = await tiktok_client.upload_video(video_content, title, description)
        
        if result['success']:
            # Store video metadata in MongoDB
            video_record = {
                "video_id": result['post_id'],
                "title": title,
                "description": description,
                "status": "UPLOADED",
                "file_name": file.filename,
                "file_size": len(video_content),
                "upload_timestamp": datetime.utcnow()
            }
            
            await db.tiktok_videos.insert_one(video_record)
            
            return {
                "success": True,
                "video_id": result['post_id'],
                "message": "Video uploaded successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@api_router.post("/tiktok/publish/{video_id}")
async def publish_tiktok_video(
    video_id: str,
    access_token: str,
    advertiser_id: str,
    privacy_level: str = "PUBLIC_TO_EVERYONE"
):
    """Publish uploaded TikTok video"""
    try:
        tiktok_client = TikTokClient(access_token, advertiser_id)
        result = await tiktok_client.publish_video(video_id, privacy_level)
        
        if result['success']:
            # Update video status in database
            await db.tiktok_videos.update_one(
                {"video_id": video_id},
                {"$set": {"status": "PUBLISHED", "publish_timestamp": datetime.utcnow()}}
            )
            
            return {"success": True, "message": "Video published successfully"}
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Publish failed: {str(e)}")

@api_router.get("/tiktok/analytics/{video_id}")
async def get_tiktok_analytics(video_id: str, access_token: str, advertiser_id: str):
    """Get TikTok video analytics"""
    try:
        headers = {
            "Access-Token": access_token,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                f"{TIKTOK_BASE_URL}/report/integrated/get/",
                headers=headers,
                params={
                    "advertiser_id": advertiser_id,
                    "report_type": "BASIC",
                    "dimensions": ["video_id"],
                    "metrics": ["impressions", "clicks", "video_play_actions"],
                    "filters": [{"field": "video_id", "operator": "IN", "value": [video_id]}],
                    "start_date": "2025-01-01",
                    "end_date": "2025-12-31"
                }
            )
            
            result = response.json()
            
            if result.get("code") == 0:
                analytics_data = result["data"]["list"][0] if result["data"]["list"] else {}
                
                # Store analytics in MongoDB
                await db.tiktok_analytics.update_one(
                    {"video_id": video_id},
                    {"$set": {
                        "analytics": analytics_data,
                        "last_updated": datetime.utcnow()
                    }},
                    upsert=True
                )
                
                return {"success": True, "analytics": analytics_data}
            else:
                raise HTTPException(status_code=400, detail=f"Analytics fetch failed: {result.get('message')}")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

# Analytics endpoints
@api_router.post("/analytics", response_model=Analytics)
async def create_analytics(analytics: Analytics):
    await db.analytics.insert_one(analytics.dict())
    return analytics

@api_router.get("/analytics/post/{post_id}")
async def get_post_analytics(post_id: str):
    analytics = await db.analytics.find({"post_id": post_id}).to_list(1000)
    return [Analytics(**analytic) for analytic in analytics]

@api_router.get("/analytics/dashboard")
async def get_dashboard_analytics():
    # Get basic stats for dashboard
    total_posts = await db.posts.count_documents({})
    published_posts = await db.posts.count_documents({"status": "published"})
    scheduled_posts = await db.posts.count_documents({"status": "scheduled"})
    draft_posts = await db.posts.count_documents({"status": "draft"})
    
    # Get recent analytics
    recent_analytics = await db.analytics.find().sort("created_at", -1).limit(10).to_list(10)
    
    # Get TikTok video count
    tiktok_videos = await db.tiktok_videos.count_documents({})
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "scheduled_posts": scheduled_posts,
        "draft_posts": draft_posts,
        "tiktok_videos": tiktok_videos,
        "recent_analytics": [Analytics(**analytic) for analytic in recent_analytics]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
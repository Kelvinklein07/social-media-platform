from fastapi import FastAPI, APIRouter, HTTPException
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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

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

# Original routes
@api_router.get("/")
async def root():
    return {"message": "Social Media Management Platform API"}

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

# Publish post to social media platforms
@api_router.post("/posts/{post_id}/publish")
async def publish_post(post_id: str):
    post = await db.posts.find_one({"id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # For MVP, we'll just update the status to published
    # In later phases, we'll add actual API calls to social media platforms
    await db.posts.update_one(
        {"id": post_id},
        {"$set": {
            "status": "published",
            "published_time": datetime.utcnow()
        }}
    )
    
    return {"message": "Post published successfully"}

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
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "scheduled_posts": scheduled_posts,
        "draft_posts": draft_posts,
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
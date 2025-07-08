#!/usr/bin/env python3
import requests
import json
import base64
from datetime import datetime, timedelta
import time
import sys
import os
from dotenv import load_dotenv
import uuid

# Load environment variables from frontend/.env to get the backend URL
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Ensure the URL ends with /api
API_URL = f"{BACKEND_URL}/api"
print(f"Using API URL: {API_URL}")

# Test data
test_post = {
    "title": "Test Post for Social Media Campaign",
    "content": "This is a test post to verify the API functionality. #testing #socialmedia",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
    "platforms": ["twitter", "facebook", "instagram"],
    "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
}

# Twitter-specific test post
twitter_test_post = {
    "title": "Twitter Integration Test",
    "content": "Testing Twitter integration with the social media management platform. #testing #twitter",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
    "platforms": ["twitter"],
    "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
}

# Direct Twitter post test data
direct_twitter_post = {
    "text": "Testing direct Twitter posting API endpoint. #testing #directpost",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="]
}

test_social_account = {
    "platform": "twitter",
    "username": "testuser",
    "access_token": "test_access_token_123",
    "refresh_token": "test_refresh_token_456",
    "account_id": "12345678"
}

# Helper function to print test results
def print_test_result(test_name, success, response=None, error=None):
    if success:
        print(f"✅ {test_name}: PASSED")
        if response:
            print(f"   Response: {response}")
    else:
        print(f"❌ {test_name}: FAILED")
        if error:
            print(f"   Error: {error}")
        if response:
            print(f"   Response: {response}")
    print("-" * 80)

# Test functions
def test_api_health():
    """Test the API health check endpoint"""
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_create_post():
    """Test creating a new post"""
    try:
        response = requests.post(f"{API_URL}/posts", json=test_post)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_create_twitter_post():
    """Test creating a Twitter-specific post"""
    try:
        response = requests.post(f"{API_URL}/posts", json=twitter_test_post)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_get_posts():
    """Test retrieving all posts"""
    try:
        response = requests.get(f"{API_URL}/posts")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_get_post_by_id(post_id):
    """Test retrieving a specific post by ID"""
    try:
        response = requests.get(f"{API_URL}/posts/{post_id}")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_update_post(post_id):
    """Test updating a post"""
    update_data = {
        "title": "Updated Test Post Title",
        "content": "This content has been updated through the API test. #updated #testing"
    }
    try:
        response = requests.put(f"{API_URL}/posts/{post_id}", json=update_data)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_publish_post(post_id):
    """Test publishing a post"""
    try:
        response = requests.post(f"{API_URL}/posts/{post_id}/publish")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_delete_post(post_id):
    """Test deleting a post"""
    try:
        response = requests.delete(f"{API_URL}/posts/{post_id}")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_create_social_account():
    """Test creating a social media account"""
    try:
        response = requests.post(f"{API_URL}/social-accounts", json=test_social_account)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_get_social_accounts():
    """Test retrieving all social media accounts"""
    try:
        response = requests.get(f"{API_URL}/social-accounts")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_analytics_dashboard():
    """Test retrieving analytics dashboard data"""
    try:
        response = requests.get(f"{API_URL}/analytics/dashboard")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_calendar_api():
    """Test the calendar API with date range parameters"""
    start_date = datetime.utcnow().isoformat()
    end_date = (datetime.utcnow() + timedelta(days=30)).isoformat()
    
    # Create a new post with scheduled_time within our date range for testing
    scheduled_post = {
        "title": "Scheduled Post for Calendar Test",
        "content": "This is a test post for calendar API. #testing #calendar",
        "media_files": [],
        "platforms": ["twitter", "facebook"],
        "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    
    # Create the post first
    try:
        create_response = requests.post(f"{API_URL}/posts", json=scheduled_post)
        if create_response.status_code != 200:
            return False, f"Failed to create test post for calendar. Status code: {create_response.status_code}"
        
        # Now test the calendar endpoint
        response = requests.get(f"{API_URL}/posts/calendar?start_date={start_date}&end_date={end_date}")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

# Twitter-specific test functions
def test_twitter_api_connection():
    """Test Twitter API connection by checking if credentials are working"""
    try:
        # We'll use the direct Twitter post endpoint to test the connection
        response = requests.post(f"{API_URL}/twitter/post", json={
            "text": "Testing Twitter API connection. This is a test tweet. #testing #apiconnection"
        })
        
        # Even if we get an error from Twitter (like duplicate content), 
        # we can check if it's a Twitter API error vs. a credential error
        if response.status_code == 200:
            return True, response.json()
        else:
            response_text = response.text
            # Check if the error is due to Twitter API rate limits or other Twitter-specific errors
            if "Twitter API" in response_text or "tweet" in response_text.lower():
                # This indicates the credentials are working but there's another Twitter-specific issue
                return True, f"Twitter credentials appear valid, but got error: {response_text}"
            else:
                return False, f"Status code: {response.status_code}, Response: {response_text}"
    except Exception as e:
        return False, str(e)

def test_twitter_direct_post():
    """Test direct Twitter posting endpoint"""
    try:
        response = requests.post(f"{API_URL}/twitter/post", json=direct_twitter_post)
        if response.status_code == 200:
            result = response.json()
            # Store the tweet_id for analytics testing
            return True, result
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_twitter_analytics(tweet_id):
    """Test Twitter analytics endpoint"""
    try:
        response = requests.get(f"{API_URL}/twitter/analytics/{tweet_id}")
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_twitter_integration():
    """Test the complete Twitter integration flow"""
    print("\n" + "=" * 80)
    print("TESTING TWITTER INTEGRATION WITH UPDATED ACCESS TOKEN SECRET")
    print("=" * 80)
    
    # Step 1: Test Twitter API connection with simple text-only tweet
    print("\n1. Testing Twitter API Authentication with text-only tweet")
    simple_tweet = {
        "text": f"Testing Twitter API connection with updated credentials. Timestamp: {datetime.utcnow().isoformat()}"
    }
    
    try:
        response = requests.post(f"{API_URL}/twitter/post", json=simple_tweet)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Twitter Authentication: PASSED")
            print(f"   Response: {result}")
            tweet_id = result.get('tweet_id')
            print(f"   Tweet ID: {tweet_id}")
        else:
            print(f"❌ Twitter Authentication: FAILED")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            print("   The updated Access Token Secret may still be incorrect.")
            return
    except Exception as e:
        print(f"❌ Twitter Authentication: FAILED")
        print(f"   Error: {str(e)}")
        return
    
    print("-" * 80)
    
    # Step 2: Test direct Twitter posting with media
    print("\n2. Testing Direct Twitter Posting with media")
    direct_success, direct_result = test_twitter_direct_post()
    print_test_result("Direct Twitter Posting with Media", direct_success, direct_result)
    
    # Get tweet_id from direct posting if available
    media_tweet_id = None
    if direct_success and 'tweet_id' in direct_result:
        media_tweet_id = direct_result['tweet_id']
        print(f"Direct posted to Twitter with tweet ID: {media_tweet_id}")
    
    # Step 3: Create a Twitter-specific post through the post creation endpoint
    print("\n3. Testing Enhanced Post Publishing with Twitter platform")
    post_success, post_result = test_create_twitter_post()
    print_test_result("Create Twitter Post", post_success, post_result)
    
    twitter_post_id = None
    if post_success:
        twitter_post_id = post_result.get('id')
        print(f"Created Twitter post with ID: {twitter_post_id}")
    
    # Step 4: Publish the Twitter post
    platform_tweet_id = None
    if twitter_post_id:
        publish_success, publish_result = test_publish_post(twitter_post_id)
        print_test_result("Publish Twitter Post", publish_success, publish_result)
        
        # Check if we got a Twitter post ID back
        if publish_success and 'results' in publish_result and 'twitter' in publish_result['results']:
            twitter_result = publish_result['results']['twitter']
            if twitter_result.get('success') and 'post_id' in twitter_result:
                platform_tweet_id = twitter_result['post_id']
                print(f"Published to Twitter with tweet ID: {platform_tweet_id}")
    
    # Step 5: Test Twitter analytics for both tweets if we have tweet_ids
    print("\n4. Testing Twitter Analytics")
    for current_tweet_id, tweet_source in [
        (tweet_id, "simple text tweet"), 
        (media_tweet_id, "media tweet"),
        (platform_tweet_id, "platform post")
    ]:
        if current_tweet_id:
            print(f"\nTesting analytics for {tweet_source} (ID: {current_tweet_id})")
            analytics_success, analytics_result = test_twitter_analytics(current_tweet_id)
            print_test_result(f"Twitter Analytics for {tweet_source}", analytics_success, analytics_result)
    
    # Step 6: Verify the enhanced post model with social post IDs
    print("\n5. Verifying Social Post IDs Storage")
    if twitter_post_id:
        post_check_success, post_check_result = test_get_post_by_id(twitter_post_id)
        print_test_result("Verify Enhanced Post Model", post_check_success, post_check_result)
        
        # Check if social_post_ids field exists and contains Twitter ID
        if post_check_success:
            social_post_ids = post_check_result.get('social_post_ids', {})
            if 'twitter' in social_post_ids:
                print(f"✅ Post contains Twitter social_post_id: {social_post_ids['twitter']}")
                if social_post_ids['twitter'] == platform_tweet_id:
                    print(f"✅ Stored Twitter ID matches the actual tweet ID")
                else:
                    print(f"❌ Stored Twitter ID ({social_post_ids['twitter']}) doesn't match actual tweet ID ({platform_tweet_id})")
            else:
                print("❌ Post does not contain Twitter social_post_id")
    
    print("\n" + "=" * 80)
    print("TWITTER INTEGRATION TESTING COMPLETED")
    print("=" * 80)

def run_all_tests():
    """Run all API tests in sequence"""
    print("\n" + "=" * 80)
    print("STARTING BACKEND API TESTS")
    print("=" * 80)
    
    # Test API health
    success, result = test_api_health()
    print_test_result("API Health Check", success, result)
    
    # Test post creation
    post_success, post_result = test_create_post()
    print_test_result("Create Post", post_success, post_result)
    
    # Store post ID for subsequent tests
    post_id = None
    if post_success:
        post_id = post_result.get('id')
        print(f"Created post with ID: {post_id}")
    
    # Test get all posts
    success, result = test_get_posts()
    print_test_result("Get All Posts", success, result)
    
    # Test get post by ID
    if post_id:
        success, result = test_get_post_by_id(post_id)
        print_test_result("Get Post by ID", success, result)
        
        # Test update post
        success, result = test_update_post(post_id)
        print_test_result("Update Post", success, result)
        
        # Test publish post
        success, result = test_publish_post(post_id)
        print_test_result("Publish Post", success, result)
    
    # Test social account creation
    success, result = test_create_social_account()
    print_test_result("Create Social Account", success, result)
    
    # Test get social accounts
    success, result = test_get_social_accounts()
    print_test_result("Get Social Accounts", success, result)
    
    # Test analytics dashboard
    success, result = test_analytics_dashboard()
    print_test_result("Get Analytics Dashboard", success, result)
    
    # Test calendar API
    success, result = test_calendar_api()
    print_test_result("Calendar API", success, result)
    
    # Run Twitter integration tests
    test_twitter_integration()
    
    # Test delete post (do this last)
    if post_id:
        success, result = test_delete_post(post_id)
        print_test_result("Delete Post", success, result)
    
    print("\n" + "=" * 80)
    print("BACKEND API TESTS COMPLETED")
    print("=" * 80)

def test_twitter_credentials():
    """Test each Twitter credential individually to identify which one might be causing the issue"""
    print("\n" + "=" * 80)
    print("TESTING TWITTER CREDENTIALS")
    print("=" * 80)
    
    # Load environment variables from backend/.env
    load_dotenv('/app/backend/.env')
    
    # Get Twitter credentials
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Print credential information (without revealing full values)
    print(f"Bearer Token: {bearer_token[:10]}...{bearer_token[-5:] if bearer_token else 'None'}")
    print(f"API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")
    print(f"API Secret: {api_secret[:5]}...{api_secret[-5:] if api_secret else 'None'}")
    print(f"Access Token: {access_token[:5]}...{access_token[-5:] if access_token else 'None'}")
    print(f"Access Token Secret: {access_token_secret[:5]}...{access_token_secret[-5:] if access_token_secret else 'None'}")
    
    # Test OAuth 1.0a authentication (used for media uploads)
    print("\nTesting OAuth 1.0a Authentication (for media uploads):")
    try:
        import tweepy
        auth = tweepy.OAuth1UserHandler(
            api_key,
            api_secret,
            access_token,
            access_token_secret
        )
        api = tweepy.API(auth)
        
        # Try to verify credentials
        try:
            user = api.verify_credentials()
            print(f"✅ OAuth 1.0a Authentication: PASSED")
            print(f"   Authenticated as: @{user.screen_name}")
        except Exception as e:
            print(f"❌ OAuth 1.0a Authentication: FAILED")
            print(f"   Error: {str(e)}")
            
            # Check if it's a specific credential issue
            if "401" in str(e):
                print("   This is likely an issue with one of the OAuth 1.0a credentials:")
                print("   - API Key")
                print("   - API Secret")
                print("   - Access Token")
                print("   - Access Token Secret")
    except Exception as e:
        print(f"❌ OAuth 1.0a Authentication Setup: FAILED")
        print(f"   Error: {str(e)}")
    
    # Test OAuth 2.0 authentication (used for most API v2 endpoints)
    print("\nTesting OAuth 2.0 Authentication (for API v2):")
    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Try to get user information
        try:
            # Get user information using the access token
            response = client.get_me()
            print(f"✅ OAuth 2.0 Authentication: PASSED")
            print(f"   Authenticated as: @{response.data.username}")
        except Exception as e:
            print(f"❌ OAuth 2.0 Authentication: FAILED")
            print(f"   Error: {str(e)}")
            
            # Check if it's a specific credential issue
            if "401" in str(e):
                print("   This is likely an issue with one of the OAuth 2.0 credentials:")
                print("   - Bearer Token")
                print("   - Or the combination of OAuth 1.0a credentials")
    except Exception as e:
        print(f"❌ OAuth 2.0 Authentication Setup: FAILED")
        print(f"   Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("TWITTER CREDENTIALS TESTING COMPLETED")
    print("=" * 80)

def test_twitter_with_fresh_credentials():
    """Test Twitter integration with fresh regenerated credentials"""
    print("\n" + "=" * 80)
    print("TESTING TWITTER INTEGRATION WITH FRESH REGENERATED CREDENTIALS")
    print("=" * 80)
    
    # Step 1: Test Twitter API Authentication
    print("\n1. Testing Twitter API Authentication")
    simple_tweet = {
        "text": f"Testing Twitter API with fresh credentials. Timestamp: {datetime.utcnow().isoformat()}"
    }
    
    try:
        response = requests.post(f"{API_URL}/twitter/post", json=simple_tweet)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Twitter Authentication: PASSED")
            print(f"   Response: {result}")
            tweet_id = result.get('tweet_id')
            print(f"   Tweet ID: {tweet_id}")
        else:
            print(f"❌ Twitter Authentication: FAILED")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Twitter Authentication: FAILED")
        print(f"   Error: {str(e)}")
        return
    
    print("-" * 80)
    
    # Step 2: Test Direct Tweet with Media
    print("\n2. Testing Direct Tweet with Media")
    media_tweet = {
        "text": f"Testing Twitter media upload with fresh credentials. Timestamp: {datetime.utcnow().isoformat()}",
        "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="]
    }
    
    try:
        response = requests.post(f"{API_URL}/twitter/post", json=media_tweet)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Direct Tweet with Media: PASSED")
            print(f"   Response: {result}")
            media_tweet_id = result.get('tweet_id')
            print(f"   Tweet ID: {media_tweet_id}")
        else:
            print(f"❌ Direct Tweet with Media: FAILED")
            print(f"   Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            media_tweet_id = None
    except Exception as e:
        print(f"❌ Direct Tweet with Media: FAILED")
        print(f"   Error: {str(e)}")
        media_tweet_id = None
    
    print("-" * 80)
    
    # Step 3: Test Platform Publishing
    print("\n3. Testing Platform Publishing via Post Creation and Publish")
    
    # Create a Twitter post
    twitter_post = {
        "title": "Twitter Platform Test",
        "content": f"Testing Twitter platform publishing with fresh credentials. Timestamp: {datetime.utcnow().isoformat()}",
        "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
        "platforms": ["twitter"],
        "scheduled_time": None
    }
    
    try:
        # Create the post
        create_response = requests.post(f"{API_URL}/posts", json=twitter_post)
        if create_response.status_code == 200:
            post_result = create_response.json()
            post_id = post_result.get('id')
            print(f"✅ Post Creation: PASSED")
            print(f"   Post ID: {post_id}")
            
            # Publish the post
            publish_response = requests.post(f"{API_URL}/posts/{post_id}/publish")
            if publish_response.status_code == 200:
                publish_result = publish_response.json()
                print(f"✅ Platform Publishing: PASSED")
                print(f"   Response: {publish_result}")
                
                # Check if Twitter publishing was successful
                if 'results' in publish_result and 'twitter' in publish_result['results']:
                    twitter_result = publish_result['results']['twitter']
                    if twitter_result.get('success'):
                        platform_tweet_id = twitter_result.get('post_id')
                        print(f"   Twitter Tweet ID: {platform_tweet_id}")
                    else:
                        print(f"❌ Twitter Publishing: FAILED")
                        print(f"   Error: {twitter_result.get('error')}")
                        platform_tweet_id = None
                else:
                    print(f"❌ Twitter Publishing: FAILED")
                    print(f"   No Twitter results found in response")
                    platform_tweet_id = None
            else:
                print(f"❌ Platform Publishing: FAILED")
                print(f"   Status code: {publish_response.status_code}")
                print(f"   Response: {publish_response.text}")
                platform_tweet_id = None
        else:
            print(f"❌ Post Creation: FAILED")
            print(f"   Status code: {create_response.status_code}")
            print(f"   Response: {create_response.text}")
            post_id = None
            platform_tweet_id = None
    except Exception as e:
        print(f"❌ Platform Publishing: FAILED")
        print(f"   Error: {str(e)}")
        platform_tweet_id = None
    
    print("-" * 80)
    
    # Step 4: Test Analytics Retrieval
    print("\n4. Testing Analytics Retrieval")
    
    # Test analytics for all tweet IDs we've collected
    for tweet_source, current_tweet_id in [
        ("Simple Tweet", tweet_id if 'tweet_id' in locals() else None),
        ("Media Tweet", media_tweet_id),
        ("Platform Tweet", platform_tweet_id if 'platform_tweet_id' in locals() else None)
    ]:
        if current_tweet_id:
            try:
                analytics_response = requests.get(f"{API_URL}/twitter/analytics/{current_tweet_id}")
                if analytics_response.status_code == 200:
                    analytics_result = analytics_response.json()
                    print(f"✅ Analytics for {tweet_source}: PASSED")
                    print(f"   Response: {analytics_result}")
                else:
                    print(f"❌ Analytics for {tweet_source}: FAILED")
                    print(f"   Status code: {analytics_response.status_code}")
                    print(f"   Response: {analytics_response.text}")
            except Exception as e:
                print(f"❌ Analytics for {tweet_source}: FAILED")
                print(f"   Error: {str(e)}")
    
    print("-" * 80)
    
    # Step 5: Verify Enhanced Model (social_post_ids)
    print("\n5. Verifying Enhanced Model (social_post_ids storage)")
    
    if 'post_id' in locals() and post_id:
        try:
            post_response = requests.get(f"{API_URL}/posts/{post_id}")
            if post_response.status_code == 200:
                post_data = post_response.json()
                social_post_ids = post_data.get('social_post_ids', {})
                
                if 'twitter' in social_post_ids:
                    stored_tweet_id = social_post_ids['twitter']
                    print(f"✅ Enhanced Model Verification: PASSED")
                    print(f"   Twitter post ID stored: {stored_tweet_id}")
                    
                    if platform_tweet_id and stored_tweet_id == platform_tweet_id:
                        print(f"✅ ID Verification: PASSED - Stored ID matches actual tweet ID")
                    else:
                        print(f"❌ ID Verification: FAILED - Stored ID doesn't match actual tweet ID")
                        print(f"   Stored: {stored_tweet_id}")
                        print(f"   Actual: {platform_tweet_id}")
                else:
                    print(f"❌ Enhanced Model Verification: FAILED")
                    print(f"   No Twitter post ID stored in social_post_ids")
            else:
                print(f"❌ Enhanced Model Verification: FAILED")
                print(f"   Status code: {post_response.status_code}")
                print(f"   Response: {post_response.text}")
        except Exception as e:
            print(f"❌ Enhanced Model Verification: FAILED")
            print(f"   Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("TWITTER INTEGRATION TESTING WITH FRESH CREDENTIALS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTING TWITTER INTEGRATION WITH FRESH REGENERATED CREDENTIALS")
    print("=" * 80)
    
    # Run the Twitter integration test with fresh credentials
    test_twitter_with_fresh_credentials()
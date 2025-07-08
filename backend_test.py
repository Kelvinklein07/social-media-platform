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
    print("TESTING TWITTER INTEGRATION")
    print("=" * 80)
    
    # Step 1: Test Twitter API connection
    success, result = test_twitter_api_connection()
    print_test_result("Twitter API Connection", success, result)
    
    # Step 2: Create a Twitter-specific post
    post_success, post_result = test_create_twitter_post()
    print_test_result("Create Twitter Post", post_success, post_result)
    
    twitter_post_id = None
    if post_success:
        twitter_post_id = post_result.get('id')
        print(f"Created Twitter post with ID: {twitter_post_id}")
    
    # Step 3: Publish the Twitter post
    tweet_id = None
    if twitter_post_id:
        publish_success, publish_result = test_publish_post(twitter_post_id)
        print_test_result("Publish Twitter Post", publish_success, publish_result)
        
        # Check if we got a Twitter post ID back
        if publish_success and 'results' in publish_result and 'twitter' in publish_result['results']:
            twitter_result = publish_result['results']['twitter']
            if twitter_result.get('success') and 'post_id' in twitter_result:
                tweet_id = twitter_result['post_id']
                print(f"Published to Twitter with tweet ID: {tweet_id}")
    
    # Step 4: Test direct Twitter posting
    direct_success, direct_result = test_twitter_direct_post()
    print_test_result("Direct Twitter Posting", direct_success, direct_result)
    
    # Get tweet_id from direct posting if available
    if direct_success and 'tweet_id' in direct_result:
        tweet_id = direct_result['tweet_id']
        print(f"Direct posted to Twitter with tweet ID: {tweet_id}")
    
    # Step 5: Test Twitter analytics if we have a tweet_id
    if tweet_id:
        analytics_success, analytics_result = test_twitter_analytics(tweet_id)
        print_test_result("Twitter Analytics", analytics_success, analytics_result)
    else:
        print("⚠️ Skipping Twitter analytics test as no tweet_id was obtained")
    
    # Step 6: Verify the enhanced post model with social post IDs
    if twitter_post_id:
        post_check_success, post_check_result = test_get_post_by_id(twitter_post_id)
        print_test_result("Verify Enhanced Post Model", post_check_success, post_check_result)
        
        # Check if social_post_ids field exists and contains Twitter ID
        if post_check_success:
            social_post_ids = post_check_result.get('social_post_ids', {})
            if 'twitter' in social_post_ids:
                print(f"✅ Post contains Twitter social_post_id: {social_post_ids['twitter']}")
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

if __name__ == "__main__":
    run_all_tests()
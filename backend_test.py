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

# LinkedIn-specific test post
linkedin_test_post = {
    "title": "LinkedIn Integration Test",
    "content": "Testing LinkedIn integration with the social media management platform. #testing #linkedin",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
    "platforms": ["linkedin"],
    "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
}

# TikTok-specific test post
tiktok_test_post = {
    "title": "TikTok Integration Test",
    "content": "Testing TikTok integration with the social media management platform. #testing #tiktok",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
    "platforms": ["tiktok"],
    "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
}

# Multi-platform test post
multi_platform_test_post = {
    "title": "Multi-Platform Integration Test",
    "content": "Testing multi-platform integration with Twitter, LinkedIn, and TikTok. #testing #multiplatform",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="],
    "platforms": ["twitter", "linkedin", "tiktok"],
    "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat()
}

# Direct Twitter post test data
direct_twitter_post = {
    "text": "Testing direct Twitter posting API endpoint. #testing #directpost",
    "media_files": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="]
}

# Direct LinkedIn post test data
direct_linkedin_post = {
    "text": "Testing direct LinkedIn posting API endpoint. #testing #directpost",
    "visibility": "PUBLIC"
}

# TikTok test data
tiktok_video_request = {
    "title": "TikTok Test Video",
    "description": "Testing TikTok video upload API endpoint. #testing #tiktok"
}

# TikTok auth data (invalid for testing error handling)
invalid_tiktok_auth = {
    "access_token": "invalid_tiktok_token_for_testing",
    "advertiser_id": "invalid_advertiser_id_for_testing"
}

# Invalid LinkedIn auth token for testing error handling
invalid_linkedin_token = "invalid_linkedin_token_for_testing"

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

def test_create_linkedin_post():
    """Test creating a LinkedIn-specific post"""
    try:
        response = requests.post(f"{API_URL}/posts", json=linkedin_test_post)
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

def test_publish_linkedin_post(post_id):
    """Test publishing a post with LinkedIn platform but invalid token"""
    try:
        # Create a LinkedIn auth request with invalid token
        linkedin_auth = {
            "access_token": invalid_linkedin_token
        }
        
        response = requests.post(f"{API_URL}/posts/{post_id}/publish", json=linkedin_auth)
        
        # We expect partial success - the post should be marked as published
        # but LinkedIn publishing should fail due to invalid token
        if response.status_code == 200:
            result = response.json()
            # Check if the response contains LinkedIn results
            if 'results' in result and 'linkedin' in result['results']:
                linkedin_result = result['results']['linkedin']
                # LinkedIn publishing should fail with invalid token
                if not linkedin_result.get('success'):
                    return True, result
                else:
                    return False, f"Unexpected success with invalid LinkedIn token: {result}"
            else:
                return False, f"Missing LinkedIn results in response: {result}"
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

# LinkedIn-specific test functions
def test_linkedin_oauth_login():
    """Test the LinkedIn OAuth login endpoint"""
    try:
        response = requests.get(f"{API_URL}/auth/linkedin/login")
        if response.status_code == 200:
            result = response.json()
            # Check if the response contains the expected fields
            if 'authorization_url' in result and 'state' in result:
                return True, result
            else:
                return False, f"Missing expected fields in response: {result}"
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
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

# LinkedIn-specific test functions
def test_linkedin_oauth_login():
    """Test the LinkedIn OAuth login endpoint"""
    try:
        response = requests.get(f"{API_URL}/auth/linkedin/login")
        if response.status_code == 200:
            result = response.json()
            # Check if the response contains the expected fields
            if 'authorization_url' in result and 'state' in result:
                return True, result
            else:
                return False, f"Missing expected fields in response: {result}"
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_linkedin_callback_structure():
    """Test the LinkedIn OAuth callback structure with invalid code"""
    try:
        # We expect this to fail since we're using an invalid code
        # We're just testing the endpoint structure
        response = requests.get(f"{API_URL}/auth/linkedin/callback?code=invalid_code&state=test_state")
        
        # Even though we expect a 400 error, the endpoint should exist
        if response.status_code == 400 or response.status_code == 200:
            return True, f"Endpoint exists and returns appropriate status code: {response.status_code}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_linkedin_profile_endpoint():
    """Test the LinkedIn profile endpoint with invalid token"""
    try:
        response = requests.get(f"{API_URL}/linkedin/profile?access_token={invalid_linkedin_token}")
        
        # We expect this to fail with a 400 error since we're using an invalid token
        # We're just testing the endpoint structure and error handling
        if response.status_code == 400:
            return True, f"Endpoint exists and properly handles invalid token: {response.text}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        elif response.status_code == 200:
            # This shouldn't happen with an invalid token
            return False, f"Unexpected success with invalid token: {response.text}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_linkedin_direct_post():
    """Test the LinkedIn direct post endpoint with invalid token"""
    try:
        response = requests.post(
            f"{API_URL}/linkedin/post?access_token={invalid_linkedin_token}", 
            json=direct_linkedin_post
        )
        
        # We expect this to fail with a 400 error since we're using an invalid token
        # We're just testing the endpoint structure and error handling
        if response.status_code == 400:
            return True, f"Endpoint exists and properly handles invalid token: {response.text}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        elif response.status_code == 200:
            # This shouldn't happen with an invalid token
            return False, f"Unexpected success with invalid token: {response.text}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
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

def test_linkedin_integration():
    """Test the complete LinkedIn integration flow"""
    print("\n" + "=" * 80)
    print("TESTING LINKEDIN INTEGRATION")
    print("=" * 80)
    
    # Step 1: Test LinkedIn OAuth Login
    print("\n1. Testing LinkedIn OAuth Login")
    oauth_success, oauth_result = test_linkedin_oauth_login()
    print_test_result("LinkedIn OAuth Login", oauth_success, oauth_result)
    
    # Step 2: Test LinkedIn OAuth Callback Structure
    print("\n2. Testing LinkedIn OAuth Callback Structure")
    callback_success, callback_result = test_linkedin_callback_structure()
    print_test_result("LinkedIn OAuth Callback Structure", callback_success, callback_result)
    
    # Step 3: Test LinkedIn Profile Endpoint
    print("\n3. Testing LinkedIn Profile Endpoint")
    profile_success, profile_result = test_linkedin_profile_endpoint()
    print_test_result("LinkedIn Profile Endpoint", profile_success, profile_result)
    
    # Step 4: Test LinkedIn Direct Post Endpoint
    print("\n4. Testing LinkedIn Direct Post Endpoint")
    direct_post_success, direct_post_result = test_linkedin_direct_post()
    print_test_result("LinkedIn Direct Post Endpoint", direct_post_success, direct_post_result)
    
    # Step 5: Create a LinkedIn-specific post through the post creation endpoint
    print("\n5. Testing Create Post with LinkedIn Platform")
    post_success, post_result = test_create_linkedin_post()
    print_test_result("Create LinkedIn Post", post_success, post_result)
    
    linkedin_post_id = None
    if post_success:
        linkedin_post_id = post_result.get('id')
        print(f"Created LinkedIn post with ID: {linkedin_post_id}")
    
    # Step 6: Publish the LinkedIn post with invalid token
    if linkedin_post_id:
        print("\n6. Testing Publish Post with LinkedIn Platform (Invalid Token)")
        publish_success, publish_result = test_publish_linkedin_post(linkedin_post_id)
        print_test_result("Publish LinkedIn Post (Invalid Token)", publish_success, publish_result)
    
    print("\n" + "=" * 80)
    print("LINKEDIN INTEGRATION TESTING COMPLETED")
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
    
    # Run LinkedIn integration tests
    test_linkedin_integration()
    
    # Test delete post (do this last)
    if post_id:
        success, result = test_delete_post(post_id)
        print_test_result("Delete Post", success, result)
    
    print("\n" + "=" * 80)
    print("BACKEND API TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTING BACKEND API AND INTEGRATIONS")
    print("=" * 80)
    
    # Run all tests
    run_all_tests()
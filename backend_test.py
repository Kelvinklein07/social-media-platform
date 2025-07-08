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
    
    # Test delete post (do this last)
    if post_id:
        success, result = test_delete_post(post_id)
        print_test_result("Delete Post", success, result)
    
    print("\n" + "=" * 80)
    print("BACKEND API TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()
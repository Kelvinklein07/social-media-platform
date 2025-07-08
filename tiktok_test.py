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

# TikTok auth data (invalid for testing error handling)
invalid_tiktok_auth = {
    "access_token": "invalid_tiktok_token_for_testing",
    "advertiser_id": "invalid_advertiser_id_for_testing"
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

# TikTok-specific test functions
def test_create_tiktok_post():
    """Test creating a TikTok-specific post"""
    try:
        response = requests.post(f"{API_URL}/posts", json=tiktok_test_post)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_create_multi_platform_post():
    """Test creating a post for multiple platforms including TikTok"""
    try:
        response = requests.post(f"{API_URL}/posts", json=multi_platform_test_post)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_tiktok_upload_endpoint_structure():
    """Test the TikTok video upload endpoint structure"""
    try:
        # Create a small test file
        test_file = {
            'file': ('test_video.mp4', base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='), 'video/mp4')
        }
        
        # Form data
        form_data = {
            'title': 'Test Video',
            'description': 'Test video description',
            'access_token': invalid_tiktok_auth['access_token'],
            'advertiser_id': invalid_tiktok_auth['advertiser_id']
        }
        
        response = requests.post(f"{API_URL}/tiktok/upload", files=test_file, data=form_data)
        
        # We expect this to fail with a 400 or 500 error since we're using invalid credentials
        # We're just testing the endpoint structure
        if response.status_code in [400, 500]:
            return True, f"Endpoint exists and properly handles invalid credentials: {response.text}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        elif response.status_code == 200:
            # This shouldn't happen with invalid credentials
            return False, f"Unexpected success with invalid credentials: {response.text}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_tiktok_publish_endpoint_structure():
    """Test the TikTok video publish endpoint structure"""
    try:
        # Use a fake video_id
        fake_video_id = "fake_video_id_123"
        
        response = requests.post(
            f"{API_URL}/tiktok/publish/{fake_video_id}",
            params={
                'access_token': invalid_tiktok_auth['access_token'],
                'advertiser_id': invalid_tiktok_auth['advertiser_id'],
                'privacy_level': 'PUBLIC_TO_EVERYONE'
            }
        )
        
        # We expect this to fail with a 400 or 500 error since we're using invalid credentials
        # We're just testing the endpoint structure
        if response.status_code in [400, 500]:
            return True, f"Endpoint exists and properly handles invalid credentials: {response.text}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        elif response.status_code == 200:
            # This shouldn't happen with invalid credentials
            return False, f"Unexpected success with invalid credentials: {response.text}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_tiktok_analytics_endpoint_structure():
    """Test the TikTok analytics endpoint structure"""
    try:
        # Use a fake video_id
        fake_video_id = "fake_video_id_123"
        
        response = requests.get(
            f"{API_URL}/tiktok/analytics/{fake_video_id}",
            params={
                'access_token': invalid_tiktok_auth['access_token'],
                'advertiser_id': invalid_tiktok_auth['advertiser_id']
            }
        )
        
        # We expect this to fail with a 400 or 500 error since we're using invalid credentials
        # We're just testing the endpoint structure
        if response.status_code in [400, 500]:
            return True, f"Endpoint exists and properly handles invalid credentials: {response.text}"
        elif response.status_code == 404:
            return False, f"Endpoint not found: {response.status_code}"
        elif response.status_code == 200:
            # This shouldn't happen with invalid credentials
            return False, f"Unexpected success with invalid credentials: {response.text}"
        else:
            return False, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, str(e)

def test_publish_multi_platform_post(post_id):
    """Test publishing a post to multiple platforms with authentication"""
    try:
        # Create auth data for LinkedIn and TikTok (invalid for testing)
        auth_data = {
            "linkedin_auth": {
                "access_token": "invalid_linkedin_token_for_testing"
            },
            "tiktok_auth": {
                "access_token": invalid_tiktok_auth['access_token'],
                "advertiser_id": invalid_tiktok_auth['advertiser_id']
            }
        }
        
        response = requests.post(f"{API_URL}/posts/{post_id}/publish", json=auth_data)
        
        # We expect partial success - the post should be marked as published
        # but platform publishing should fail due to invalid tokens
        if response.status_code == 200:
            result = response.json()
            # Check if the response contains platform results
            if 'results' in result:
                # Check if all platforms are in the results
                platforms = multi_platform_test_post['platforms']
                all_platforms_present = all(platform in result['results'] for platform in platforms)
                
                if all_platforms_present:
                    return True, result
                else:
                    return False, f"Not all platforms in results: {result}"
            else:
                return False, f"Missing platform results in response: {result}"
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

def test_tiktok_integration():
    """Test the complete TikTok integration flow"""
    print("\n" + "=" * 80)
    print("TESTING TIKTOK INTEGRATION")
    print("=" * 80)
    
    # Step 1: Test TikTok Upload Endpoint Structure
    print("\n1. Testing TikTok Upload Endpoint Structure")
    upload_success, upload_result = test_tiktok_upload_endpoint_structure()
    print_test_result("TikTok Upload Endpoint Structure", upload_success, upload_result)
    
    # Step 2: Test TikTok Publish Endpoint Structure
    print("\n2. Testing TikTok Publish Endpoint Structure")
    publish_success, publish_result = test_tiktok_publish_endpoint_structure()
    print_test_result("TikTok Publish Endpoint Structure", publish_success, publish_result)
    
    # Step 3: Test TikTok Analytics Endpoint Structure
    print("\n3. Testing TikTok Analytics Endpoint Structure")
    analytics_success, analytics_result = test_tiktok_analytics_endpoint_structure()
    print_test_result("TikTok Analytics Endpoint Structure", analytics_success, analytics_result)
    
    # Step 4: Create a TikTok-specific post through the post creation endpoint
    print("\n4. Testing Create Post with TikTok Platform")
    post_success, post_result = test_create_tiktok_post()
    print_test_result("Create TikTok Post", post_success, post_result)
    
    tiktok_post_id = None
    if post_success:
        tiktok_post_id = post_result.get('id')
        print(f"Created TikTok post with ID: {tiktok_post_id}")
    
    # Step 5: Create a multi-platform post including TikTok
    print("\n5. Testing Create Multi-Platform Post with TikTok")
    multi_post_success, multi_post_result = test_create_multi_platform_post()
    print_test_result("Create Multi-Platform Post", multi_post_success, multi_post_result)
    
    multi_post_id = None
    if multi_post_success:
        multi_post_id = multi_post_result.get('id')
        print(f"Created multi-platform post with ID: {multi_post_id}")
    
    # Step 6: Test publishing multi-platform post
    if multi_post_id:
        print("\n6. Testing Publish Multi-Platform Post")
        multi_publish_success, multi_publish_result = test_publish_multi_platform_post(multi_post_id)
        print_test_result("Publish Multi-Platform Post", multi_publish_success, multi_publish_result)
    
    # Step 7: Test analytics dashboard includes TikTok metrics
    print("\n7. Testing Analytics Dashboard for TikTok Metrics")
    dashboard_success, dashboard_result = test_analytics_dashboard()
    print_test_result("Analytics Dashboard TikTok Metrics", dashboard_success, dashboard_result)
    
    # Check if tiktok_videos count is included in the dashboard
    if dashboard_success and 'tiktok_videos' in dashboard_result:
        print(f"✅ Dashboard includes TikTok videos count: {dashboard_result['tiktok_videos']}")
    else:
        print("❌ Dashboard does not include TikTok videos count")
    
    print("\n" + "=" * 80)
    print("TIKTOK INTEGRATION TESTING COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTING TIKTOK INTEGRATION")
    print("=" * 80)
    
    # Run TikTok integration tests
    test_tiktok_integration()
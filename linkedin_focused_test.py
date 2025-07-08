#!/usr/bin/env python3
import requests
import json
import sys
import os
from dotenv import load_dotenv
import time

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

# Invalid LinkedIn auth token for testing error handling
invalid_linkedin_token = "invalid_linkedin_token_for_testing"

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
            json={"text": "Test post", "visibility": "PUBLIC"}
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

def run_linkedin_tests():
    """Run all LinkedIn integration tests with delays to avoid rate limits"""
    print("\n" + "=" * 80)
    print("TESTING LINKEDIN INTEGRATION")
    print("=" * 80)
    
    # Test 1: LinkedIn OAuth Login
    print("\n1. Testing LinkedIn OAuth Login")
    success, result = test_linkedin_oauth_login()
    print_test_result("LinkedIn OAuth Login", success, result)
    time.sleep(2)  # Add delay to avoid rate limits
    
    # Test 2: LinkedIn OAuth Callback Structure
    print("\n2. Testing LinkedIn OAuth Callback Structure")
    success, result = test_linkedin_callback_structure()
    print_test_result("LinkedIn OAuth Callback Structure", success, result)
    time.sleep(2)  # Add delay to avoid rate limits
    
    # Test 3: LinkedIn Profile Endpoint
    print("\n3. Testing LinkedIn Profile Endpoint")
    success, result = test_linkedin_profile_endpoint()
    print_test_result("LinkedIn Profile Endpoint", success, result)
    time.sleep(2)  # Add delay to avoid rate limits
    
    # Test 4: LinkedIn Direct Post Endpoint
    print("\n4. Testing LinkedIn Direct Post Endpoint")
    success, result = test_linkedin_direct_post()
    print_test_result("LinkedIn Direct Post Endpoint", success, result)
    
    print("\n" + "=" * 80)
    print("LINKEDIN INTEGRATION TESTING COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    run_linkedin_tests()
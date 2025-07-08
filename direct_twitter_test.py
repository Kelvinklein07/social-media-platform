#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import tweepy
from datetime import datetime

# Load environment variables from backend/.env
load_dotenv('/app/backend/.env')

# Get Twitter credentials
bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

print("Testing direct tweepy posting...")

# Set up OAuth 1.0a authentication
auth = tweepy.OAuth1UserHandler(
    api_key,
    api_secret,
    access_token,
    access_token_secret
)
api = tweepy.API(auth)

# Set up OAuth 2.0 client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Test OAuth 1.0a authentication
try:
    user = api.verify_credentials()
    print(f"OAuth 1.0a Authentication: PASSED")
    print(f"Authenticated as: @{user.screen_name}")
except Exception as e:
    print(f"OAuth 1.0a Authentication: FAILED")
    print(f"Error: {str(e)}")

# Test posting a tweet using OAuth 2.0 client
try:
    tweet_text = f"Testing direct tweepy posting with OAuth 2.0. Timestamp: {datetime.utcnow().isoformat()}"
    response = client.create_tweet(text=tweet_text)
    print(f"OAuth 2.0 Tweet Posting: PASSED")
    print(f"Tweet ID: {response.data['id']}")
    
    # Try to get tweet details
    tweet_id = response.data['id']
    tweet_details = client.get_tweet(
        tweet_id,
        tweet_fields=['created_at', 'public_metrics']
    )
    print(f"Tweet Details: {tweet_details.data}")
    print(f"Tweet Metrics: {tweet_details.data.public_metrics if hasattr(tweet_details.data, 'public_metrics') else 'No metrics available'}")
except Exception as e:
    print(f"OAuth 2.0 Tweet Posting: FAILED")
    print(f"Error: {str(e)}")

# Test posting a tweet using OAuth 1.0a API
try:
    tweet_text = f"Testing direct tweepy posting with OAuth 1.0a. Timestamp: {datetime.utcnow().isoformat()}"
    status = api.update_status(status=tweet_text)
    print(f"OAuth 1.0a Tweet Posting: PASSED")
    print(f"Tweet ID: {status.id}")
except Exception as e:
    print(f"OAuth 1.0a Tweet Posting: FAILED")
    print(f"Error: {str(e)}")
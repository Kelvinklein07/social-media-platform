#!/bin/bash

# Social Media Platform Deployment Script
echo "🚀 Deploying Social Media Management Platform..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Login to Railway (you'll need to do this manually)
echo "Please run: railway login"
echo "Then run: railway init"
echo "Then run: railway up"

echo "📋 Environment Variables to set in Railway:"
echo "================================"
cat .env.production
echo "================================"

echo "✅ After deployment, your platform will be live!"
echo "🌐 Railway will provide you with a live URL"
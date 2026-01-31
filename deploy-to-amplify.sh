#!/bin/bash

# Quick deployment script for AWS Amplify
# This script helps you prepare and deploy the Cafe Phoenicia site to AWS Amplify

echo "=========================================="
echo "🚀 AWS AMPLIFY DEPLOYMENT HELPER"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
else
    echo "✅ Git repository already initialized"
    echo ""
fi

# Check if remote is set
if ! git remote | grep -q origin; then
    echo "⚠️  No Git remote found."
    echo ""
    echo "Please set up your Git repository:"
    echo "1. Create a new repository on GitHub/GitLab/Bitbucket"
    echo "2. Run: git remote add origin YOUR_REPO_URL"
    echo ""
    read -p "Enter your Git repository URL (or press Enter to skip): " repo_url
    
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added: $repo_url"
        echo ""
    else
        echo "⚠️  Skipping remote setup. You can add it later with:"
        echo "   git remote add origin YOUR_REPO_URL"
        echo ""
    fi
else
    echo "✅ Git remote already configured"
    git remote -v
    echo ""
fi

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes detected"
    echo ""
    
    read -p "Do you want to commit all changes? (y/n): " commit_choice
    
    if [ "$commit_choice" = "y" ] || [ "$commit_choice" = "Y" ]; then
        echo ""
        read -p "Enter commit message (or press Enter for default): " commit_msg
        
        if [ -z "$commit_msg" ]; then
            commit_msg="Deploy Cafe Phoenicia offline site to AWS Amplify"
        fi
        
        echo "📦 Staging all files..."
        git add .
        
        echo "💾 Committing changes..."
        git commit -m "$commit_msg"
        
        echo "✅ Changes committed"
        echo ""
    else
        echo "⚠️  Skipping commit. You can commit later with:"
        echo "   git add ."
        echo "   git commit -m 'Your message'"
        echo ""
    fi
else
    echo "✅ No uncommitted changes"
    echo ""
fi

# Check if main/master branch exists
current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [ -z "$current_branch" ]; then
    echo "📦 Creating main branch..."
    git checkout -b main
    echo "✅ Main branch created"
    echo ""
elif [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    echo "⚠️  Current branch: $current_branch"
    read -p "Switch to main branch? (y/n): " switch_choice
    
    if [ "$switch_choice" = "y" ] || [ "$switch_choice" = "Y" ]; then
        git checkout -b main 2>/dev/null || git checkout main
        echo "✅ Switched to main branch"
        echo ""
    fi
else
    echo "✅ On $current_branch branch"
    echo ""
fi

# Ask if user wants to push
if git remote | grep -q origin; then
    echo "🚀 Ready to push to remote repository"
    echo ""
    read -p "Do you want to push now? (y/n): " push_choice
    
    if [ "$push_choice" = "y" ] || [ "$push_choice" = "Y" ]; then
        echo ""
        echo "📤 Pushing to remote..."
        
        # Try to push, set upstream if needed
        if git push -u origin $(git rev-parse --abbrev-ref HEAD); then
            echo "✅ Successfully pushed to remote"
            echo ""
        else
            echo "⚠️  Push failed. You may need to:"
            echo "   1. Authenticate with your Git provider"
            echo "   2. Check your repository URL"
            echo "   3. Ensure you have push permissions"
            echo ""
        fi
    else
        echo "⚠️  Skipping push. You can push later with:"
        echo "   git push -u origin main"
        echo ""
    fi
fi

echo "=========================================="
echo "📋 NEXT STEPS"
echo "=========================================="
echo ""
echo "1. Go to AWS Amplify Console:"
echo "   https://console.aws.amazon.com/amplify/"
echo ""
echo "2. Click 'New app' → 'Host web app'"
echo ""
echo "3. Connect your Git repository"
echo ""
echo "4. Amplify will auto-detect amplify.yml"
echo ""
echo "5. Review and deploy!"
echo ""
echo "📖 For detailed instructions, see:"
echo "   AWS_AMPLIFY_SETUP.md"
echo ""
echo "=========================================="
echo "✅ PREPARATION COMPLETE!"
echo "=========================================="
echo ""

#!/bin/bash

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install git and try again."
    exit 1
fi

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "Git repository initialized."
fi

# Add all files to git
git add .

# Commit changes
echo "Enter commit message:"
read commit_message
git commit -m "$commit_message"

# Check if remote origin exists
if ! git remote | grep -q "origin"; then
    echo "Enter your GitHub repository URL (e.g. https://github.com/username/repo.git):"
    read repo_url
    git remote add origin $repo_url
    echo "Remote origin added."
fi

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main || git push -u origin master

echo "===================="
echo "Deployment completed!"
echo "===================="
echo "Next steps:"
echo "1. Go to https://streamlit.io/cloud"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New app' and select this repository"
echo "4. Set the main file path to 'Home.py'"
echo "5. Click 'Deploy!'"
echo "====================" 
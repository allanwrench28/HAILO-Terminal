#!/bin/bash
# Quick GitHub setup for HAILO-Terminal

echo "🚀 Setting up HAILO-Terminal GitHub Repository"
echo ""

# Add the remote repository
echo "Adding GitHub remote..."
git remote add origin https://github.com/allanwrench28/HAILO-Terminal.git

# Rename branch to main (modern convention)
echo "Setting main branch..."
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository successfully pushed to GitHub!"
echo "🔗 View at: https://github.com/allanwrench28/HAILO-Terminal"
echo ""
echo "Next steps:"
echo "1. Go to your repository on GitHub"
echo "2. Add topics: home-assistant, hailo, ai, automation, hacs"
echo "3. Enable GitHub Pages in Settings if desired"
echo "4. Your repository is HACS-ready for community sharing!"
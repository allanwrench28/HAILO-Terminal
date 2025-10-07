# GitHub Repository Setup Script for HAILO-Terminal
# This script helps you complete the GitHub repository setup

Write-Host "=== HAILO-Terminal GitHub Setup ===" -ForegroundColor Green
Write-Host ""

# Check if git is available
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git for Windows from: https://git-scm.com/download/win"
    exit 1
}

Write-Host "✅ Git is available" -ForegroundColor Green

# Check current git status
Write-Host ""
Write-Host "Current Git Status:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "📋 Next Steps to Complete GitHub Setup:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  Create GitHub Repository:" -ForegroundColor White
Write-Host "   • Go to: https://github.com/new" -ForegroundColor Gray
Write-Host "   • Repository name: HAILO-Terminal" -ForegroundColor Gray
Write-Host "   • Description: AI-powered Home Assistant terminal with Hailo integration" -ForegroundColor Gray
Write-Host "   • Make it Public" -ForegroundColor Gray
Write-Host "   • DO NOT initialize with README (we already have one)" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  After creating the repository, run these commands:" -ForegroundColor White
Write-Host ""
$username = Read-Host "Enter your GitHub username"
Write-Host ""
Write-Host "Copy and paste these commands:" -ForegroundColor Cyan
Write-Host "git remote add origin https://github.com/$username/HAILO-Terminal.git" -ForegroundColor Green
Write-Host "git branch -M main" -ForegroundColor Green
Write-Host "git push -u origin main" -ForegroundColor Green

Write-Host ""
Write-Host "3️⃣  Repository Configuration (after push):" -ForegroundColor White
Write-Host "   • Go to Settings -> Pages" -ForegroundColor Gray
Write-Host "   • Source: Deploy from a branch" -ForegroundColor Gray
Write-Host "   • Branch: main / (root)" -ForegroundColor Gray
Write-Host "   • Add topics: home-assistant, hailo, ai, automation, hacs" -ForegroundColor Gray

Write-Host ""
Write-Host "4️⃣  HACS Integration:" -ForegroundColor White
Write-Host "   • Your repository will be HACS-ready!" -ForegroundColor Gray
Write-Host "   • Users can install via HACS -> Integrations -> Custom Repositories" -ForegroundColor Gray

Write-Host ""
Write-Host "🚀 Ready for GitHub! Your repository contains:" -ForegroundColor Green
Write-Host "   ✅ Complete Hailo AI Terminal add-on" -ForegroundColor White
Write-Host "   ✅ Enhanced entity discovery system" -ForegroundColor White
Write-Host "   ✅ Smart automation recommendations" -ForegroundColor White
Write-Host "   ✅ Automated PowerShell installer" -ForegroundColor White
Write-Host "   ✅ Comprehensive documentation" -ForegroundColor White
Write-Host "   ✅ HACS compatibility" -ForegroundColor White

Write-Host ""
Write-Host "Press Enter to continue or Ctrl+C to exit..."
Read-Host
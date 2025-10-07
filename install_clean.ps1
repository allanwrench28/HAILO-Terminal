# Hailo AI Terminal - Automated Installation Script
# Run this in Windows PowerShell as Administrator

param(
    [string]$HomeAssistantIP = "192.168.0.143",
    [string]$HAToken = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "HAILO AI TERMINAL - AUTOMATED INSTALLER" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Green
    Write-Host "    Run in Windows PowerShell AS ADMINISTRATOR:" -ForegroundColor White
    Write-Host "    .\install.ps1 -HomeAssistantIP 192.168.0.143 -HAToken your_token_here" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "PARAMETERS:" -ForegroundColor Green
    Write-Host "    -HomeAssistantIP    Your Home Assistant IP address" -ForegroundColor White
    Write-Host "    -HAToken           Your Home Assistant Long-Lived Access Token (REQUIRED)" -ForegroundColor White
    Write-Host "    -Help              Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "GET YOUR TOKEN:" -ForegroundColor Green
    Write-Host "    1. Open Home Assistant web interface" -ForegroundColor White
    Write-Host "    2. Click your profile (bottom left)" -ForegroundColor White
    Write-Host "    3. Scroll down to 'Long-lived access tokens'" -ForegroundColor White
    Write-Host "    4. Click 'Create Token'" -ForegroundColor White
    Write-Host "    5. Copy the token and use it with -HAToken parameter" -ForegroundColor White
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host "HAILO AI TERMINAL - AUTOMATED INSTALLER" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Validate parameters
if ([string]::IsNullOrEmpty($HAToken)) {
    Write-Host "ERROR: HAToken parameter is required!" -ForegroundColor Red
    Write-Host "Use: .\install.ps1 -HAToken your_token_here" -ForegroundColor Yellow
    Write-Host "Run: .\install.ps1 -Help for more information" -ForegroundColor Yellow
    exit 1
}

Write-Host "Installation Parameters:" -ForegroundColor Green
Write-Host "  Home Assistant IP: $HomeAssistantIP" -ForegroundColor White
Write-Host "  Token: $($HAToken.Substring(0,10))..." -ForegroundColor White

# Step 1: Test Home Assistant Connection
Write-Host "" 
Write-Host "Step 1: Testing Home Assistant Connection..." -ForegroundColor Yellow
try {
    $testUrl = "http://$HomeAssistantIP`:8123/api/"
    $headers = @{ "Authorization" = "Bearer $HAToken" }
    $response = Invoke-RestMethod -Uri $testUrl -Headers $headers -TimeoutSec 10
    Write-Host "SUCCESS: Home Assistant connection successful!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to connect to Home Assistant!" -ForegroundColor Red
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  - Home Assistant is running at http://$HomeAssistantIP`:8123" -ForegroundColor Yellow
    Write-Host "  - Your token is valid and not expired" -ForegroundColor Yellow
    Write-Host "  - Your firewall allows the connection" -ForegroundColor Yellow
    exit 1
}

# Step 2: Create local add-on structure
Write-Host ""
Write-Host "Step 2: Creating add-on directory structure..." -ForegroundColor Yellow
$addonPath = ".\hailo-terminal-addon"
if (Test-Path $addonPath) {
    Write-Host "  Removing existing directory..." -ForegroundColor White
    Remove-Item $addonPath -Recurse -Force
}
New-Item -ItemType Directory -Path $addonPath -Force | Out-Null
Write-Host "SUCCESS: Directory structure created!" -ForegroundColor Green

# Step 3: Copy add-on files
Write-Host ""
Write-Host "Step 3: Copying add-on files..." -ForegroundColor Yellow
$sourceFiles = @(
    "addons\hailo-terminal\config.yaml",
    "addons\hailo-terminal\Dockerfile", 
    "addons\hailo-terminal\README.md",
    "addons\hailo-terminal\src\*"
)

foreach ($file in $sourceFiles) {
    if ($file -like "*\*") {
        $sourcePath = $file
        $destPath = "$addonPath\src"
        New-Item -ItemType Directory -Path $destPath -Force | Out-Null
        Copy-Item $sourcePath $destPath -Recurse -Force
    } else {
        Copy-Item $file $addonPath -Force
    }
}
Write-Host "SUCCESS: Add-on files copied!" -ForegroundColor Green

# Step 4: Update configuration
Write-Host ""
Write-Host "Step 4: Configuring add-on settings..." -ForegroundColor Yellow
$configPath = "$addonPath\config.yaml"
$config = Get-Content $configPath -Raw

# Update configuration
$config = $config -replace 'ha_url: "http://192\.168\.0\.143:8123"', "ha_url: `"http://$HomeAssistantIP`:8123`""
$config = $config -replace 'ha_token: ""', "ha_token: `"$HAToken`""

Set-Content -Path $configPath -Value $config -Encoding UTF8
Write-Host "SUCCESS: Configuration updated!" -ForegroundColor Green

# Step 5: Create installation package
Write-Host ""
Write-Host "Step 5: Creating installation package..." -ForegroundColor Yellow
$packagePath = "hailo-terminal-addon.zip"
if (Test-Path $packagePath) {
    Remove-Item $packagePath -Force
}
Compress-Archive -Path "$addonPath\*" -DestinationPath $packagePath -Force
Write-Host "SUCCESS: Installation package created: $packagePath" -ForegroundColor Green

# Step 6: Generate instructions
Write-Host ""
Write-Host "Step 6: Generating installation instructions..." -ForegroundColor Yellow
$instructions = @"
HAILO AI TERMINAL - MANUAL INSTALLATION STEPS
============================================

AUTOMATED SETUP COMPLETE! Now follow these steps:

METHOD 1: SAMBA UPLOAD (EASIEST)
-------------------------------
1. Install Samba add-on in Home Assistant:
   - Go to Settings -> Add-ons -> Add-on Store
   - Search for "Samba share" 
   - Install and start it

2. Open Windows File Explorer
   - Press Windows + R
   - Type: \\$HomeAssistantIP
   - Press Enter
   - Enter your Home Assistant credentials

3. Navigate to the addons folder:
   - Double-click "addons" folder
   - Create new folder: "hailo-terminal"
   - Copy contents of "hailo-terminal-addon" folder into it

4. Restart Home Assistant:
   - Settings -> System -> Restart

AFTER INSTALLATION:
-----------------
1. Go to Settings -> Add-ons
2. Find "Hailo AI Terminal" 
3. Click Install
4. Start the add-on
5. Open Web UI
6. Test AI functionality

Your installation package: $packagePath
"@

Set-Content -Path "INSTALLATION_INSTRUCTIONS.txt" -Value $instructions -Encoding UTF8
Write-Host "SUCCESS: Instructions saved to: INSTALLATION_INSTRUCTIONS.txt" -ForegroundColor Green

# Final summary
Write-Host ""
Write-Host "INSTALLATION PREPARATION COMPLETE!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "FILES CREATED:" -ForegroundColor Cyan
Write-Host "  $packagePath - Ready to upload to Home Assistant" -ForegroundColor White
Write-Host "  INSTALLATION_INSTRUCTIONS.txt - Step-by-step guide" -ForegroundColor White
Write-Host "  hailo-terminal-addon\ - Add-on source files" -ForegroundColor White
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  1. Read INSTALLATION_INSTRUCTIONS.txt" -ForegroundColor White
Write-Host "  2. Upload files to Home Assistant using Samba" -ForegroundColor White
Write-Host "  3. Restart Home Assistant" -ForegroundColor White
Write-Host "  4. Install the add-on from Settings -> Add-ons" -ForegroundColor White
Write-Host ""
Write-Host "Ready to deploy your AI-powered Home Assistant add-on!" -ForegroundColor Green
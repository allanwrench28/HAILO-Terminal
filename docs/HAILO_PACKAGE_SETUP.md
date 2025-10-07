# 📦 Hailo Package Setup Guide

This comprehensive guide walks you through obtaining and installing the required Hailo packages for the AI Terminal Add-on.

## 🎯 Overview

The Hailo AI Terminal requires proprietary software packages from Hailo Technologies. This guide provides:

- ✅ **Step-by-step** account creation process
- ✅ **Exact package** identification and download
- ✅ **Automated verification** tools  
- ✅ **Clear error messages** with solutions
- ✅ **Troubleshooting** for common issues

**⏱️ Estimated Time**: 15-20 minutes  
**📋 Requirements**: Valid email address, internet connection

---

## 🔐 Step 1: Create Hailo Developer Account

### 1.1 Navigate to Hailo Developer Zone

1. **Open** your web browser
2. **Go to**: [https://hailo.ai/developer-zone/](https://hailo.ai/developer-zone/)
3. **Look for** the "Sign up" or "Register" button (usually top-right corner)

> **💡 Tip**: If you see "Login" instead, click it first - there's usually a "Create Account" link on the login page.

### 1.2 Complete Registration Form

Fill out the registration form with these details:

| Field | What to Enter | Example |
|-------|---------------|---------|
| **First Name** | Your first name | John |
| **Last Name** | Your last name | Smith |
| **Email** | Valid email address | john.smith@example.com |
| **Company** | Your organization or "Personal" | Personal / Acme Corp |
| **Country** | Your country | United States |
| **Use Case** | Select "Home Automation" or "AI Development" | Home Automation |
| **Password** | Strong password (8+ chars, mixed case, numbers) | MySecure123! |

> **⚠️ Important**: Use a **real email address** - you'll need to verify it!

### 1.3 Verify Your Email

1. **Check** your email inbox (including spam/junk folders)
2. **Look for** email from "Hailo Technologies" or "noreply@hailo.ai"
3. **Click** the verification link in the email
4. **Return** to the Hailo Developer Zone website

> **🔄 Not received email?** Wait 5-10 minutes, then check spam folder. Still nothing? Try the "Resend verification" option.

### 1.4 Complete Profile Setup

After email verification:

1. **Login** with your new credentials
2. **Complete** any additional profile questions
3. **Accept** the Terms of Service and Privacy Policy
4. **Submit** your profile

> **✅ Success Indicator**: You should see a dashboard or welcome message saying "Welcome to Hailo Developer Zone"

---

## 📥 Step 2: Download Required Packages

### 2.1 Navigate to Downloads Section

1. **Login** to your Hailo Developer Zone account
2. **Look for** "Downloads", "Software", or "SDK" section (usually in main navigation)
3. **Click** on the downloads area

> **🔍 Can't find downloads?** Look for sections labeled: "Resources", "Tools", "SDK", or "Software Suite"

### 2.2 Locate Required Packages

You need these **4 specific packages** for ARM64 architecture:

| Package Name | Purpose | File Pattern |
|--------------|---------|--------------|
| **HailoRT** | Runtime library | `hailort_*_arm64.deb` |
| **AI Software Suite** | Core AI tools | `hailo_ai_sw_suite_*_arm64.deb` |
| **Model Zoo** | Pre-trained models | `hailo_model_zoo_*_arm64.deb` |
| **Dataflow Compiler** | Model compilation | `hailo_dataflow_compiler_*_arm64.deb` |

### 2.3 Download Process

For **each package**:

1. **Find** the package in the downloads list
2. **Verify** it shows "ARM64" or "aarch64" architecture
3. **Check** the version (should be 2023.10+ or newer)
4. **Click** "Download" button
5. **Save** to a dedicated folder on your computer

> **📁 Organization Tip**: Create a folder called `hailo-packages` on your desktop to keep everything organized.

### 2.4 Version Compatibility Check

**Current Compatible Versions** (as of October 2025):

| Package | Minimum Version | Recommended |
|---------|----------------|-------------|
| HailoRT | 4.23.0 | 4.28.0+ |
| AI Software Suite | 2023.10 | 2024.04+ |
| Model Zoo | 2.12.0 | 2.15.0+ |
| Dataflow Compiler | 3.27.0 | 3.35.0+ |

> **⚠️ Version Warning**: Older versions may not work properly. Always download the **latest available** versions.

---

## ✅ Step 3: Verify Downloaded Packages

### 3.1 Manual Verification Checklist

**Check these items** for each downloaded file:

- [ ] **File extension** is `.deb`
- [ ] **Architecture** contains `arm64` or `aarch64`
- [ ] **File size** is reasonable (each should be 50MB-2GB)
- [ ] **No browser errors** during download
- [ ] **Files are not corrupted** (can be opened/inspected)

### 3.2 Automated Verification Script

Create this PowerShell script to verify your packages:

```powershell
# Save as: verify-hailo-packages.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$PackageFolder
)

Write-Host "🔍 Hailo Package Verification Tool" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if folder exists
if (-not (Test-Path $PackageFolder)) {
    Write-Host "❌ ERROR: Package folder not found: $PackageFolder" -ForegroundColor Red
    Write-Host "💡 Solution: Create the folder and place your .deb files there" -ForegroundColor Yellow
    exit 1
}

# Required packages
$RequiredPackages = @(
    @{Name="HailoRT"; Pattern="hailort_*_arm64.deb"},
    @{Name="AI Software Suite"; Pattern="hailo_ai_sw_suite_*_arm64.deb"},
    @{Name="Model Zoo"; Pattern="hailo_model_zoo_*_arm64.deb"},
    @{Name="Dataflow Compiler"; Pattern="hailo_dataflow_compiler_*_arm64.deb"}
)

$AllFound = $true
$FoundFiles = @()

foreach ($pkg in $RequiredPackages) {
    $files = Get-ChildItem -Path $PackageFolder -Name $pkg.Pattern
    
    if ($files.Count -eq 0) {
        Write-Host "❌ MISSING: $($pkg.Name)" -ForegroundColor Red
        Write-Host "   Looking for: $($pkg.Pattern)" -ForegroundColor Gray
        $AllFound = $false
    } elseif ($files.Count -eq 1) {
        Write-Host "✅ FOUND: $($pkg.Name) -> $files" -ForegroundColor Green
        $FoundFiles += Join-Path $PackageFolder $files
    } else {
        Write-Host "⚠️  MULTIPLE: $($pkg.Name) -> $($files -join ', ')" -ForegroundColor Yellow
        Write-Host "   Using: $($files[0])" -ForegroundColor Gray
        $FoundFiles += Join-Path $PackageFolder $files[0]
    }
}

if (-not $AllFound) {
    Write-Host ""
    Write-Host "❌ VERIFICATION FAILED" -ForegroundColor Red
    Write-Host "📋 Missing packages must be downloaded from:" -ForegroundColor Yellow
    Write-Host "   https://hailo.ai/developer-zone/" -ForegroundColor White
    exit 1
}

# Check file sizes
Write-Host ""
Write-Host "📊 File Size Verification:" -ForegroundColor Cyan
foreach ($file in $FoundFiles) {
    $size = (Get-Item $file).Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    
    if ($sizeMB -lt 10) {
        Write-Host "⚠️  $($file | Split-Path -Leaf): ${sizeMB}MB (unusually small)" -ForegroundColor Yellow
    } elseif ($sizeMB -gt 3000) {
        Write-Host "⚠️  $($file | Split-Path -Leaf): ${sizeMB}MB (unusually large)" -ForegroundColor Yellow
    } else {
        Write-Host "✅ $($file | Split-Path -Leaf): ${sizeMB}MB" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 VERIFICATION COMPLETE" -ForegroundColor Green
Write-Host "📁 Ready to copy to Home Assistant: /share/hailo/packages/" -ForegroundColor White
```

**Run the verification**:
```powershell
# Navigate to where you saved the script
cd C:\path\to\script

# Run verification (replace with your actual folder path)
.\verify-hailo-packages.ps1 -PackageFolder "C:\Users\YourName\Desktop\hailo-packages"
```

### 3.3 Expected Output

**✅ Successful verification looks like this**:
```
🔍 Hailo Package Verification Tool
=================================
✅ FOUND: HailoRT -> hailort_4.28.0_arm64.deb
✅ FOUND: AI Software Suite -> hailo_ai_sw_suite_2024.04_arm64.deb
✅ FOUND: Model Zoo -> hailo_model_zoo_2.15.0_arm64.deb
✅ FOUND: Dataflow Compiler -> hailo_dataflow_compiler_3.35.0_arm64.deb

📊 File Size Verification:
✅ hailort_4.28.0_arm64.deb: 156.42MB
✅ hailo_ai_sw_suite_2024.04_arm64.deb: 1247.83MB
✅ hailo_model_zoo_2.15.0_arm64.deb: 891.24MB
✅ hailo_dataflow_compiler_3.35.0_arm64.deb: 523.67MB

🎉 VERIFICATION COMPLETE
📁 Ready to copy to Home Assistant: /share/hailo/packages/
```

---

## 📂 Step 4: Transfer to Home Assistant

### 4.1 Create Package Directory

**SSH Method**:
```bash
# Connect to your Home Assistant
ssh root@YOUR_HA_IP

# Create the directory
mkdir -p /share/hailo/packages

# Set permissions
chmod 755 /share/hailo/packages

# Verify creation
ls -la /share/hailo/
```

**File Editor Method**:
1. Install **File Editor** add-on from HA store
2. Navigate to `/share/`
3. Create folder: `hailo` 
4. Inside `hailo`, create folder: `packages`

### 4.2 Transfer Files

Choose your preferred method:

#### Option A: SCP Transfer (Recommended)
```bash
# From your computer (replace paths with actual paths)
scp C:\Users\YourName\Desktop\hailo-packages\*.deb root@YOUR_HA_IP:/share/hailo/packages/
```

#### Option B: Samba Share
1. Enable **Samba** add-on in Home Assistant
2. Access `\\YOUR_HA_IP\share\hailo\packages\` from Windows Explorer
3. Copy all 4 `.deb` files to this location

#### Option C: File Editor Upload
1. Open File Editor add-on
2. Navigate to `/share/hailo/packages/`
3. Upload each `.deb` file individually
4. Wait for each upload to complete before starting next

### 4.3 Verify Transfer

**Check via SSH**:
```bash
# List files with details
ls -la /share/hailo/packages/

# Count files (should be 4)
ls /share/hailo/packages/*.deb | wc -l

# Check total size
du -sh /share/hailo/packages/
```

**Expected output**:
```
-rw-r--r-- 1 root root 164M Oct  5 10:30 hailort_4.28.0_arm64.deb
-rw-r--r-- 1 root root 1.3G Oct  5 10:31 hailo_ai_sw_suite_2024.04_arm64.deb
-rw-r--r-- 1 root root 892M Oct  5 10:32 hailo_model_zoo_2.15.0_arm64.deb
-rw-r--r-- 1 root root 524M Oct  5 10:33 hailo_dataflow_compiler_3.35.0_arm64.deb

4
2.8G    /share/hailo/packages/
```

---

## 🔧 Step 5: Install Hailo AI Terminal Add-on

Now that packages are ready, install the add-on:

**Note**: This is a Home Assistant **Add-on**, not a HACS integration. Add-ons are installed through Home Assistant's Add-on Store.

### 5.1 Add Add-on Repository

1. **Open** Home Assistant
2. **Navigate to** Settings → Add-ons
3. **Click** Add-on Store (bottom right)
4. **Click** ⋮ menu (top right) → "Repositories"
5. **Add** repository: `https://github.com/allanwrench28/HAILO-Terminal`
6. **Click** "Add" → "Close"

### 5.2 Install Add-on

1. **Refresh** the Add-on Store page
2. **Find** "Hailo AI Terminal" in the list
3. **Click** on it
4. **Click** "Install"
5. **Wait** for installation to complete

### 5.3 Pre-Start Verification

Before starting the add-on, run this final check:

**SSH into Home Assistant**:
```bash
# Final package verification
echo "🔍 Final Pre-Installation Check"
echo "==============================="

# Check package directory
if [ -d "/share/hailo/packages" ]; then
    echo "✅ Package directory exists"
else
    echo "❌ Package directory missing"
    exit 1
fi

# Count packages
PKG_COUNT=$(ls /share/hailo/packages/*.deb 2>/dev/null | wc -l)
echo "📦 Found $PKG_COUNT packages"

if [ "$PKG_COUNT" -ne 4 ]; then
    echo "❌ Expected 4 packages, found $PKG_COUNT"
    echo "📋 Missing packages:"
    ls /share/hailo/packages/
    exit 1
fi

# Check each required package
REQUIRED=("hailort" "hailo_ai_sw_suite" "hailo_model_zoo" "hailo_dataflow_compiler")
for pkg in "${REQUIRED[@]}"; do
    if ls /share/hailo/packages/${pkg}_*_arm64.deb 1> /dev/null 2>&1; then
        echo "✅ Found: $pkg"
    else
        echo "❌ Missing: $pkg"
    fi
done

echo ""
echo "🎉 Pre-installation check complete!"
echo "🚀 Ready to start Hailo AI Terminal add-on"
```

---

## 🐛 Troubleshooting Common Issues

### Issue: "Can't access Hailo Developer Zone"

**Symptoms**:
- Website won't load
- "Access denied" messages
- Account creation fails

**Solutions**:
1. **Check internet connection**
2. **Try different browser** (Chrome, Firefox, Edge)
3. **Disable VPN** if using one
4. **Clear browser cache** and cookies
5. **Try incognito/private mode**
6. **Contact Hailo support** if issue persists

### Issue: "Email verification not received"

**Symptoms**:
- No verification email after 10+ minutes
- Can't complete registration

**Solutions**:
1. **Check spam/junk** folder thoroughly
2. **Add hailo.ai to safe senders** list
3. **Try different email provider** (Gmail, Outlook)
4. **Wait 30 minutes** then try "Resend verification"
5. **Contact support** with registered email address

### Issue: "Can't find the right packages"

**Symptoms**:
- Only x86/AMD64 packages available
- Version numbers don't match
- Download links broken

**Solutions**:
1. **Look for "ARM64" or "aarch64"** specifically
2. **Try different download section** (SDK vs Tools vs Resources)
3. **Contact Hailo support** for ARM64 package access
4. **Verify account permissions** (some packages need approval)

### Issue: "Package verification fails"

**Symptoms**:
- Files are 0 bytes or very small
- "Corrupted file" errors
- Verification script shows missing packages

**Solutions**:
1. **Re-download** suspected corrupted files
2. **Try different browser** for download
3. **Disable antivirus** temporarily during download
4. **Check disk space** on download location
5. **Use download manager** for large files

### Issue: "Transfer to Home Assistant fails"

**Symptoms**:
- SCP connection refused
- Samba share not accessible
- File Editor upload times out

**Solutions**:
1. **Verify SSH access**: `ssh root@YOUR_HA_IP`
2. **Check Samba configuration** and restart add-on
3. **Upload files one at a time** in File Editor
4. **Use smaller chunks** if files are very large
5. **Verify disk space**: `df -h /share`

### Issue: "Add-on won't start after package installation"

**Symptoms**:
- Add-on starts then immediately stops
- "Package installation failed" in logs
- Hailo device not detected

**Solutions**:
1. **Check logs**: `ha addons logs hailo_ai_terminal`
2. **Verify all 4 packages** are present and correct
3. **Check file permissions**: `chmod 644 /share/hailo/packages/*.deb`
4. **Restart Home Assistant** completely
5. **Check Hailo hardware** is properly connected

---

## 📞 Getting Help

### Self-Help Resources
1. **Add-on logs**: Settings → Add-ons → Hailo AI Terminal → Log tab
2. **System logs**: Settings → System → Logs
3. **Package verification script** (above)
4. **Home Assistant community forums**

### Contact Information
- **GitHub Issues**: Technical problems with the add-on
- **Hailo Support**: Package download and account issues
- **Home Assistant Community**: General Home Assistant questions

### Information to Include When Asking for Help
1. **Home Assistant version**: Settings → About
2. **Add-on version**: From add-on info page
3. **Architecture**: Usually ARM64 for most modern systems
4. **Error messages**: Copy exact text from logs
5. **Steps taken**: What you tried before asking for help

---

## ✅ Success! What's Next?

Once everything is working:

1. **Access web interface**: `http://YOUR_HA_IP:8080`
2. **Try a test query**: "How is my Home Assistant performing?"
3. **Explore monitoring**: Check resource usage graphs
4. **Customize settings**: Adjust AI model and monitoring intervals
5. **Set up automations**: Let the AI suggest optimizations

**Welcome to the future of Home Assistant management!** 🚀

---

*Last updated: October 2025 | Version 1.0*
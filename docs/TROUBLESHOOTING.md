# 🛠️ Hailo Package Troubleshooting Guide

Quick solutions for common Hailo package installation issues.

## 🚨 Common Error Messages & Solutions

### ❌ "Docker build failed" with "File format not recognized"
```
xz: (stdin): File format not recognized
tar: Child returned status 1
tar: Error is not recoverable: exiting now
ERROR: failed to build: process "/bin/bash -o pipefail -c ..." did not complete successfully: exit code: 2
```

**This error occurs during S6-Overlay installation in the Docker build process.**

**Root Cause:**
The curl command was piping directly to tar, which could fail silently during network issues, rate limiting, or redirect problems, causing tar to receive invalid data.

**Solution:**
✅ **This issue has been fixed in version 1.0.1+**

The Dockerfiles have been updated to:
1. Download S6-Overlay files to temporary location first
2. Verify the download completed successfully
3. Then extract the files
4. Clean up temporary files

**If you're still experiencing this:**
1. **Update to the latest version** of the add-on
2. **Clear Docker build cache**: Go to Home Assistant → Settings → Add-ons → (Three dots) → Rebuild
3. **Check network connectivity** to github.com
4. **Wait a few minutes** if GitHub rate limiting is in effect

**For developers:** The fix changes from:
```dockerfile
# Old (problematic):
curl -L -f -s "URL" | tar Jxvf - -C /

# New (reliable):
curl -L -f -o /tmp/file.tar.xz "URL" \
    && tar -C / -Jxpf /tmp/file.tar.xz \
    && rm -f /tmp/file.tar.xz
```

### ❌ "Package directory not found"
```
ERROR: Package directory not found: /share/hailo/packages
```

**Solution:**
```bash
# Create the directory
mkdir -p /share/hailo/packages

# Set permissions  
chmod 755 /share/hailo/packages

# Verify creation
ls -la /share/hailo/
```

### ❌ "Required package not found"
```
ERROR: Required package not found: hailort_*_arm64.deb
```

**This means packages haven't been downloaded yet.**

**Solution:**
1. 📥 **[Download packages using our comprehensive guide](HAILO_PACKAGE_SETUP.md)**
2. 🔍 **Verify with:** `/share/hailo-terminal-addon/scripts/verify-hailo-packages.sh`

### ❌ "No Hailo devices detected via PCI scan"
```
WARNING: No Hailo hardware detected via PCI scan
```

**Possible Causes:**
- Hailo device not connected
- Device drivers not loaded
- Running in virtualized environment

**Solution:**
```bash
# Check PCI devices
lspci | grep -i hailo

# Check device files
ls -la /dev/hailo*

# Check system messages
dmesg | grep -i hailo
```

### ❌ "Failed to install package"
```
ERROR: Failed to install: hailort_4.28.0_arm64.deb
```

**Solution:**
```bash
# Check disk space
df -h /usr

# Try manual installation for detailed error
dpkg -i /share/hailo/packages/hailort_*_arm64.deb

# Fix broken dependencies
apt-get install -f
```

### ❌ "Architecture mismatch"
```
WARNING: Architecture mismatch: Package=amd64, System=arm64
```

**Solution:**
You downloaded the wrong architecture packages.
1. **Delete wrong packages:** `rm /share/hailo/packages/*amd64*`
2. **[Re-download ARM64 packages](HAILO_PACKAGE_SETUP.md)**
3. **Verify:** Look for `arm64` or `aarch64` in filenames

### ❌ "Package may be corrupted"
```
WARNING: Package may be corrupted: hailort_4.28.0_arm64.deb
```

**Solution:**
```bash
# Check file integrity
dpkg --info /share/hailo/packages/suspicious_package.deb

# If corrupted, re-download the package
# Use verification tool to check all packages
/share/hailo-terminal-addon/scripts/verify-hailo-packages.sh
```

## 🔍 Diagnostic Commands

### Check Package Status
```bash
# List all files in package directory
ls -la /share/hailo/packages/

# Count packages (should be 4)
ls /share/hailo/packages/*.deb | wc -l

# Check total size
du -sh /share/hailo/packages/

# Verify each package
for pkg in /share/hailo/packages/*.deb; do
    echo "Checking: $(basename "$pkg")"
    dpkg --info "$pkg" | grep -E "Package|Version|Architecture"
    echo "---"
done
```

### Check System Compatibility
```bash
# Check system architecture
uname -m
dpkg --print-architecture

# Check available memory
free -h

# Check disk space
df -h

# Check Home Assistant version
ha info
```

### Check Hailo Hardware
```bash
# Check PCI devices
lspci -v | grep -A 10 -i hailo

# Check device files
ls -la /dev/hailo*

# Check kernel modules
lsmod | grep hailo

# Check system messages
dmesg | tail -50 | grep -i hailo
```

## 📋 Pre-Installation Checklist

Before installing the add-on, verify:

- [ ] **Package directory exists:** `/share/hailo/packages/`
- [ ] **All 4 packages present:** `ls /share/hailo/packages/*.deb | wc -l` returns `4`
- [ ] **Correct architecture:** All files contain `arm64` or `aarch64`
- [ ] **Reasonable file sizes:** Each package 50MB-1.5GB
- [ ] **Files not corrupted:** `dpkg --info` works for each
- [ ] **Sufficient disk space:** At least 5GB free in `/usr`
- [ ] **Sufficient memory:** At least 4GB total RAM
- [ ] **Hailo hardware connected:** `lspci | grep -i hailo` shows device

## 🔧 Quick Fixes

### Reset Everything
If you're having persistent issues:

```bash
# Remove all packages and start over
rm -rf /share/hailo/packages/*

# Re-create directory
mkdir -p /share/hailo/packages
chmod 755 /share/hailo/packages

# Re-download packages using the guide
# Then verify with the verification tool
```

### Test Without Hailo Hardware
The add-on can run in CPU-only mode for testing:

```bash
# Set CPU-only mode (for testing)
export HAILO_MODE="cpu"

# Start add-on normally
# AI will work but without Hailo acceleration
```

### Clean Package Cache
If getting dependency errors:

```bash
# Clean package cache
apt-get clean
apt-get update

# Fix broken packages  
apt-get install -f

# Try installation again
```

## 📞 Getting More Help

### Information to Gather
When asking for help, include:

```bash
# System information
echo "=== SYSTEM INFO ==="
uname -a
ha info | head -10

echo "=== PACKAGE STATUS ==="
ls -la /share/hailo/packages/
du -sh /share/hailo/packages/

echo "=== HAILO HARDWARE ==="
lspci | grep -i hailo
ls -la /dev/hailo* 2>/dev/null || echo "No Hailo devices"

echo "=== DISK SPACE ==="
df -h /usr | tail -1

echo "=== MEMORY ==="
free -h | head -2
```

### Support Channels
- **GitHub Issues:** Technical problems with the add-on
- **Home Assistant Community:** General Home Assistant questions  
- **Hailo Support:** Package download and hardware issues

### Useful Log Commands
```bash
# Add-on logs
ha addons logs hailo_ai_terminal

# System logs
journalctl -u home-assistant -f

# Package installation logs
tail -f /var/log/hailo_terminal_setup.log
```

---

## ✅ Success Indicators

When everything is working correctly, you should see:

- **Package verification:** All packages found and verified ✅
- **Installation logs:** "All packages installed successfully" ✅  
- **Device detection:** Hailo device detected via PCI scan ✅
- **Add-on startup:** Web interface accessible at port 8080 ✅
- **AI responses:** Terminal responds to queries ✅

**🎉 If you see all these, your Hailo AI Terminal is ready to use!**

---

*Need the complete setup guide? See [HAILO_PACKAGE_SETUP.md](HAILO_PACKAGE_SETUP.md)*
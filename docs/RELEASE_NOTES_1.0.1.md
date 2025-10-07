# Release Notes - Version 1.0.1

## 🐛 Bug Fix Release

**Release Date:** October 7, 2024

### Critical Fix: Docker Build Failure

This release addresses a critical issue that prevented the add-on from being installed successfully.

#### Problem
Users encountered the following error when attempting to install the add-on:
```
xz: (stdin): File format not recognized
tar: Child returned status 1
tar: Error is not recoverable: exiting now
ERROR: failed to build: exit code 2
```

#### Root Cause
The issue was in the S6-Overlay installation step of the Dockerfile. The previous implementation used a pattern that piped curl output directly to tar:

```dockerfile
curl -L -f -s "URL" | tar Jxvf - -C /
```

This approach had several problems:
- **Silent failures**: When curl failed (network issues, rate limiting, redirects), it could output HTML error pages or empty data
- **No validation**: tar received whatever curl output, even if it wasn't a valid archive
- **Poor error reporting**: The `-s` (silent) flag hid helpful error messages

#### Solution
The Dockerfiles have been updated to use a more reliable two-step approach:

```dockerfile
# Step 1: Download to temporary file
curl -L -f -o /tmp/s6-overlay-arch.tar.xz "URL"

# Step 2: Extract from verified file
tar -C / -Jxpf /tmp/s6-overlay-arch.tar.xz

# Step 3: Clean up
rm -f /tmp/s6-overlay-arch.tar.xz
```

This ensures:
- ✅ Download completes successfully before extraction
- ✅ Better error messages if download fails
- ✅ Validation that the file exists before extraction
- ✅ Proper cleanup of temporary files

### Files Changed

1. **`addons/hailo-terminal/Dockerfile`**
   - Fixed S6-Overlay installation (lines 56-70)
   - Updated version label to 1.0.1

2. **`templates/hailo-base-addon/Dockerfile`**
   - Applied the same fix for template consistency

3. **`addons/hailo-terminal/config.yaml`**
   - Bumped version to 1.0.1

4. **`docs/TROUBLESHOOTING.md`**
   - Added new section for Docker build failures
   - Provided clear explanation and solution

5. **`docs/addon-development-guide.md`**
   - Updated example code with the correct pattern

6. **`CHANGELOG.md`**
   - Documented the fix

### Upgrade Instructions

**For existing users who couldn't install:**
1. Navigate to Home Assistant → Settings → Add-ons → Add-on Store
2. Find "Hailo AI Terminal" in your repository list
3. Click on it and you should see version 1.0.1
4. Click "Install"
5. The installation should now complete successfully

**For developers maintaining the template:**
- Pull the latest changes from the repository
- The template Dockerfile now includes the fix

### Verification

The fix has been validated with:
- ✅ Docker syntax checking (`docker build --check`)
- ✅ Manual testing of the download and extraction process
- ✅ Review of Docker best practices for reliable builds

### Impact

- **Before**: Add-on installation failed immediately during Docker build
- **After**: Add-on installs successfully and is ready to use

### Technical Details

For developers interested in the technical details:

**Why the pipe pattern failed:**
- GitHub's CDN sometimes returns HTTP 429 (rate limit) or 503 (service unavailable)
- curl with `-f` flag exits on HTTP errors, but the pipe continues
- tar receives empty input or HTML error page
- tar fails with "File format not recognized"

**Why the new pattern works:**
- curl downloads the file and verifies the HTTP response
- File is saved to disk only if download succeeds
- tar extracts from a verified file
- Both steps have clear success/failure conditions

### Additional Resources

- [Troubleshooting Guide](TROUBLESHOOTING.md) - Now includes Docker build error solutions
- [Development Guide](addon-development-guide.md) - Updated with best practices
- [GitHub Issue](https://github.com/allanwrench28/HAILO-Terminal/issues/) - Original bug report

---

**Full Changelog:** [v1.0.0...v1.0.1](https://github.com/allanwrench28/HAILO-Terminal/compare/v1.0.0...v1.0.1)

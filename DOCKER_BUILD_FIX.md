# Docker Build Fix - s6-overlay Architecture Mapping

## Problem

The Docker build for the Home Assistant add-on was failing with a 404 error when trying to download s6-overlay:

```
curl: (22) The requested URL returned error: 404
https://github.com/just-containers/s6-overlay/releases/download/v3.2.1.0/s6-overlay-arm64.tar.xz
```

## Root Cause

The Dockerfile was using `dpkg --print-architecture` directly to determine the architecture for downloading s6-overlay files. However, the architecture naming conventions differ between Debian/dpkg and s6-overlay:

| System Type | dpkg Output | s6-overlay Filename |
|-------------|-------------|---------------------|
| ARM64       | `arm64`     | `aarch64`           |
| AMD64       | `amd64`     | `x86_64`            |
| i386        | `i386`      | `i686`              |
| ARM (EABI)  | `armel`     | `arm`               |
| ARM (Hard Float) | `armhf` | `armhf`             |

When building for ARM64 (aarch64) architecture, dpkg returns `arm64`, but s6-overlay expects `aarch64`, causing the download to fail with a 404 error.

## Solution

Added architecture mapping logic to convert dpkg architecture names to s6-overlay architecture names:

```dockerfile
RUN ARCH=$(dpkg --print-architecture) \
    && S6_ARCH=${ARCH} \
    && if [ "${ARCH}" = "amd64" ]; then S6_ARCH="x86_64"; fi \
    && if [ "${ARCH}" = "arm64" ]; then S6_ARCH="aarch64"; fi \
    && if [ "${ARCH}" = "armel" ]; then S6_ARCH="arm"; fi \
    && if [ "${ARCH}" = "i386" ]; then S6_ARCH="i686"; fi \
    && curl -L -f -o /tmp/s6-overlay-arch.tar.xz \
        "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
    && tar -C / -Jxpf /tmp/s6-overlay-arch.tar.xz \
    && rm -f /tmp/s6-overlay-arch.tar.xz
```

## Files Changed

1. **`addons/hailo-terminal/Dockerfile`** - Main add-on Dockerfile
2. **`templates/hailo-base-addon/Dockerfile`** - Template for new add-ons
3. **`docs/addon-development-guide.md`** - Documentation with examples

## Testing

Verified that all mapped architectures have valid s6-overlay downloads:
- ✓ x86_64 (from amd64)
- ✓ aarch64 (from arm64) - **This was the failing one**
- ✓ armhf (unchanged)
- ✓ arm (from armel)
- ✓ i686 (from i386)

## Impact

- **Before**: Docker build fails with 404 error on ARM64 systems
- **After**: Docker build succeeds on all supported architectures

This fix ensures the add-on can be built successfully on Home Assistant systems running on ARM64 hardware (like Raspberry Pi 4/5, ODROID, and other ARM-based systems).

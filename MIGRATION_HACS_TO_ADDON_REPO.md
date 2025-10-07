# Migration: HACS Configuration to Add-on Repository

## Issue Summary

The repository was incorrectly configured for HACS (Home Assistant Community Store) distribution. However, **HACS does NOT support add-ons** - it only supports integrations, themes, plugins, and Python scripts.

Home Assistant add-ons must be distributed through **add-on repositories** that users add directly to Home Assistant's Add-on Store.

## Changes Made

### Files Removed
- ❌ `hacs.json` - HACS metadata file (not applicable for add-ons)

### Files Updated

#### Repository Configuration
- ✅ `repository.yaml` - Updated from HACS format to Home Assistant add-on repository format
  - Changed comments and documentation links
  - Updated structure to match add-on repository specifications
- ✅ `repository.json` - Maintained as add-on repository metadata

#### Documentation Files
- ✅ `README.md` 
  - Added prominent notice: "This is a Home Assistant Add-on (not a HACS integration)"
  - Replaced HACS installation instructions with add-on repository installation
  - Updated installation steps to match actual Home Assistant UI

- ✅ `docs/INSTALLATION.md`
  - Removed HACS prerequisites
  - Rewrote installation section for add-on repository
  - Added clear distinction between add-ons and integrations

- ✅ `docs/HACS_DISTRIBUTION.md` → Renamed purpose
  - Updated title to "Home Assistant Add-on Distribution Guide"
  - Added warning that HACS doesn't support add-ons
  - Replaced HACS submission process with add-on distribution info

- ✅ `HACS_README.md`
  - Removed HACS badge
  - Updated installation instructions for add-on repository

- ✅ `HACS_PUBLICATION_GUIDE.md`
  - Completely rewritten to explain add-on distribution
  - Removed HACS submission instructions
  - Added section on why HACS doesn't support add-ons

- ✅ `docs/HAILO_PACKAGE_SETUP.md`
  - Updated installation section from HACS to add-on repository

- ✅ `REPOSITORY_READY.md`
  - Removed HACS compatibility claims
  - Updated to reference add-on repository configuration

- ✅ `CHANGELOG.md`
  - Changed "HACS integration" to "Add-on repository configuration"
  - Updated installation requirements

- ✅ `FEATURE_SUMMARY.md`
  - Changed "HACS compatibility" to "Add-on repository configuration"
  - Updated installation methods

- ✅ `GITHUB_SETUP_GUIDE.md`
  - Removed HACS badge from example README
  - Updated repository visibility note
  - Changed "Test HACS integration" to "Test add-on installation"
  - Updated file structure to show `repository.yaml` instead of `hacs.json`

- ✅ `INSTALLATION_GUIDE.md`
  - Replaced "HACS Installation" section with "Add-on Store Installation"
  - Added proper add-on repository installation steps

- ✅ `CREATE_GITHUB_REPO.md`
  - Changed "HACS compatibility" to "Add-on repository"

#### Workflow Files
- ✅ `.github/workflows/ci.yml`
  - Renamed from "HACS Validation & Build" to "Add-on CI/CD"
  - Removed HACS validation job (not applicable)
  - Removed dependency on HACS validation

### Files Added
- ✅ `docs/ADDON_VS_INTEGRATION.md` - Comprehensive guide explaining:
  - Difference between add-ons and integrations
  - Why HACS doesn't support add-ons
  - How users install add-ons vs integrations
  - Proper repository configuration for each type

## How Users Install This Add-on

### Before (Incorrect)
```
1. Open HACS
2. Add custom repository
3. Install through HACS
```
❌ This doesn't work for add-ons!

### After (Correct)
```
1. Settings → Add-ons → Add-on Store
2. ⋮ menu → Repositories
3. Add: https://github.com/allanwrench28/HAILO-Terminal
4. Find "Hailo AI Terminal" and install
```
✅ This is the correct way to install add-ons!

## Technical Background

### What HACS Supports
- ✅ Integrations (custom_components)
- ✅ Themes
- ✅ Plugins (Lovelace cards)
- ✅ Python scripts

### What HACS Does NOT Support
- ❌ Add-ons
- ❌ Add-on repositories

### Why This Matters
- **Add-ons** are containerized applications running alongside Home Assistant
- **Integrations** are Python code extending Home Assistant's core functionality
- They have completely different:
  - Installation methods
  - Distribution channels
  - Repository structures
  - File requirements

## Repository Configuration

### Before
```yaml
# hacs.json
{
  "name": "Hailo AI Terminal",
  "content_in_root": false,
  "filename": "hailo-terminal",
  "homeassistant": "2023.9.0"
}
```

### After
```yaml
# repository.yaml
name: "Hailo AI Terminal Add-on Repository"
description: "AI-powered terminal and resource monitor for Home Assistant with Hailo hardware acceleration"
url: "https://github.com/allanwrench28/HAILO-Terminal"
maintainer: "WrenchWorks3D"
```

## Verification

To verify the changes are correct:

1. ✅ `hacs.json` file removed
2. ✅ `repository.yaml` uses add-on repository format
3. ✅ No misleading HACS installation instructions
4. ✅ Clear notices that this is an add-on, not integration
5. ✅ CI/CD workflow doesn't reference HACS
6. ✅ Documentation explains add-on vs integration difference

## Impact

### For Users
- 🎯 Clear, correct installation instructions
- 📚 Understanding of add-on vs integration
- ✅ Proper expectations about installation process

### For Repository
- ✅ Correctly configured as add-on repository
- ✅ Follows Home Assistant add-on specifications
- ✅ No misleading HACS references
- ✅ Accurate documentation throughout

## References

- [Home Assistant Add-on Documentation](https://developers.home-assistant.io/docs/add-ons)
- [Home Assistant Add-on Repository](https://developers.home-assistant.io/docs/add-ons/repository)
- [HACS Documentation](https://hacs.xyz/docs/categories/integration) (for integrations only)

---

**Migration completed**: All HACS references removed or corrected. Repository now properly configured as Home Assistant Add-on Repository.

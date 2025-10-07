# Add-ons vs Integrations in Home Assistant

## Important Distinction

This repository contains a **Home Assistant Add-on**, not an integration. Understanding the difference is crucial for distribution and installation.

## What's the Difference?

### Home Assistant Add-ons (This Repository)
- **What they are**: Containerized applications that run alongside Home Assistant
- **Examples**: File editors, databases, monitoring tools, custom services
- **Installation**: Through Home Assistant's Add-on Store
- **Distribution**: Via add-on repositories (like this one)
- **HACS Support**: ❌ **NO** - HACS does not support add-ons
- **Repository Type**: Add-on repository with `repository.yaml` and `repository.json`
- **Directory Structure**: `addons/[addon-name]/config.yaml`

### Home Assistant Integrations
- **What they are**: Python code that extends Home Assistant's core functionality
- **Examples**: Smart device integrations, weather services, custom sensors
- **Installation**: Through Home Assistant's Integrations page or config files
- **Distribution**: Via HACS or manual installation
- **HACS Support**: ✅ **YES** - Primary distribution method
- **Repository Type**: Custom component with `hacs.json`
- **Directory Structure**: `custom_components/[integration-name]/`

## HACS (Home Assistant Community Store)

HACS **only supports**:
- ✅ Integrations (custom components)
- ✅ Themes
- ✅ Plugins (Lovelace cards)
- ✅ Python scripts

HACS **does NOT support**:
- ❌ Add-ons
- ❌ Add-on repositories

## How Users Install This Add-on

Since this is an add-on, users install it through Home Assistant directly:

1. **Settings** → **Add-ons** → **Add-on Store**
2. Click **⋮** (three dots) → **Repositories**
3. Add: `https://github.com/allanwrench28/HAILO-Terminal`
4. Find "Hailo AI Terminal" in the store
5. Click **Install**

## Why This Matters

### For Developers
- Don't try to submit add-ons to HACS - it won't work
- Use `repository.yaml` and `repository.json` for add-on repositories
- Don't use `hacs.json` for add-ons
- Follow Home Assistant add-on structure guidelines

### For Users
- Add-ons require Home Assistant OS or Supervised
- Add-ons run in separate containers with their own resources
- Add-ons can access hardware devices and system resources
- Add-ons are managed through the Add-on Store, not HACS

## This Repository Configuration

✅ **Correctly configured as**:
- Home Assistant Add-on Repository
- `repository.yaml` - Add-on repository configuration
- `repository.json` - Add-on repository metadata
- `addons/hailo-terminal/config.yaml` - Add-on configuration

❌ **Not configured for**:
- HACS distribution
- Custom component/integration

## References

- [Home Assistant Add-on Documentation](https://developers.home-assistant.io/docs/add-ons)
- [Home Assistant Add-on Repository Structure](https://developers.home-assistant.io/docs/add-ons/repository)
- [HACS Documentation](https://hacs.xyz/docs/categories/integration)

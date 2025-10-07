# Hailo Packages Directory

This directory is intentionally empty in the repository. **Do NOT place Hailo packages here during development.**

## For Users Installing the Add-on

The Hailo packages (.deb and .whl files) should be placed in one of these locations on your Home Assistant system:

1. **Recommended**: `/addons/` folder (accessible via Samba share)
2. `/config/addons_config/hailo_ai_terminal/`
3. `/share/hailo/packages/`

The add-on will automatically detect and install packages from these locations when it starts.

## Why is this directory empty?

- Hailo packages are large (800MB-1.5GB) and should not be committed to Git
- Users download packages directly from Hailo's Developer Zone
- The add-on copies packages from user-accessible locations at runtime

## Installation Guide

See the main repository documentation for detailed installation instructions:
- `SIMPLE_INSTALL_GUIDE.md` - Step-by-step user guide
- `docs/HAILO_PACKAGE_SETUP.md` - Package setup details

## For Developers

If you're testing the add-on locally, you can place packages here temporarily for development purposes, but they will be ignored by Git.

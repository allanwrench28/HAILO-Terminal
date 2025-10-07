#!/bin/bash
# ==============================================================================
# Home Assistant Add-on Build Script
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ADDON_NAME=""
ADDON_VERSION=""
ARCHITECTURE="aarch64"
BUILD_FROM="ubuntu:22.04"

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS] ADDON_PATH"
    echo ""
    echo "Build a Home Assistant add-on"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -a, --arch ARCH         Target architecture (default: aarch64)"
    echo "  -v, --version VERSION   Add-on version"
    echo "  -n, --name NAME         Add-on name"
    echo "  --no-cache             Build without cache"
    echo ""
    echo "Examples:"
    echo "  $0 ./addons/my-hailo-addon"
    echo "  $0 -a amd64 -v 1.0.1 ./addons/my-hailo-addon"
}

# Parse command line arguments
ADDON_PATH=""
NO_CACHE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--arch)
            ARCHITECTURE="$2"
            shift 2
            ;;
        -v|--version)
            ADDON_VERSION="$2"
            shift 2
            ;;
        -n|--name)
            ADDON_NAME="$2"
            shift 2
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        *)
            if [[ -z "$ADDON_PATH" ]]; then
                ADDON_PATH="$1"
            else
                echo -e "${RED}Error: Unknown option $1${NC}"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate addon path
if [[ -z "$ADDON_PATH" ]]; then
    echo -e "${RED}Error: Add-on path is required${NC}"
    show_help
    exit 1
fi

if [[ ! -d "$ADDON_PATH" ]]; then
    echo -e "${RED}Error: Add-on directory not found: $ADDON_PATH${NC}"
    exit 1
fi

# Check for required files
if [[ ! -f "$ADDON_PATH/config.yaml" ]]; then
    echo -e "${RED}Error: config.yaml not found in $ADDON_PATH${NC}"
    exit 1
fi

if [[ ! -f "$ADDON_PATH/Dockerfile" ]]; then
    echo -e "${RED}Error: Dockerfile not found in $ADDON_PATH${NC}"
    exit 1
fi

# Extract addon info from config.yaml if not provided
if [[ -z "$ADDON_NAME" ]]; then
    ADDON_NAME=$(grep "^name:" "$ADDON_PATH/config.yaml" | cut -d'"' -f2 | cut -d"'" -f2 | xargs)
fi

if [[ -z "$ADDON_VERSION" ]]; then
    ADDON_VERSION=$(grep "^version:" "$ADDON_PATH/config.yaml" | cut -d'"' -f2 | cut -d"'" -f2 | xargs)
fi

# Generate image tag
IMAGE_TAG="local/${ARCHITECTURE}-addon-$(echo "$ADDON_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_'):${ADDON_VERSION}"

echo -e "${BLUE}Building Home Assistant Add-on${NC}"
echo -e "${BLUE}===============================${NC}"
echo "Add-on: $ADDON_NAME"
echo "Version: $ADDON_VERSION"
echo "Architecture: $ARCHITECTURE"
echo "Path: $ADDON_PATH"
echo "Image: $IMAGE_TAG"
echo ""

# Build the add-on
echo -e "${YELLOW}Starting build...${NC}"
cd "$ADDON_PATH"

BUILD_CMD="docker build $NO_CACHE --platform linux/$ARCHITECTURE -t $IMAGE_TAG ."

echo "Running: $BUILD_CMD"
echo ""

if eval "$BUILD_CMD"; then
    echo ""
    echo -e "${GREEN}✓ Build completed successfully!${NC}"
    echo -e "${GREEN}Image: $IMAGE_TAG${NC}"
    
    # Show image size
    IMAGE_SIZE=$(docker images --format "table {{.Size}}" "$IMAGE_TAG" | tail -n 1)
    echo -e "${GREEN}Size: $IMAGE_SIZE${NC}"
else
    echo ""
    echo -e "${RED}✗ Build failed!${NC}"
    exit 1
fi
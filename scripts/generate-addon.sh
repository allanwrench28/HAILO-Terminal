#!/bin/bash
# ==============================================================================
# Home Assistant Add-on Generator Script
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$WORKSPACE_DIR/templates/hailo-base-addon"
ADDONS_DIR="$WORKSPACE_DIR/addons"

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS] ADDON_NAME"
    echo ""
    echo "Generate a new Home Assistant Hailo add-on from template"
    echo ""
    echo "Options:"
    echo "  -h, --help              Show this help message"
    echo "  -d, --description DESC  Add-on description"
    echo "  -v, --version VERSION   Initial version (default: 1.0.0)"
    echo "  -a, --author AUTHOR     Add-on author"
    echo "  --url URL              Repository URL"
    echo ""
    echo "Examples:"
    echo "  $0 my-hailo-detector"
    echo "  $0 -d 'Object detection with Hailo' -v 0.1.0 my-detector"
}

# Default values
ADDON_NAME=""
ADDON_DESCRIPTION=""
ADDON_VERSION="1.0.0"
ADDON_AUTHOR=""
ADDON_URL=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--description)
            ADDON_DESCRIPTION="$2"
            shift 2
            ;;
        -v|--version)
            ADDON_VERSION="$2"
            shift 2
            ;;
        -a|--author)
            ADDON_AUTHOR="$2"
            shift 2
            ;;
        --url)
            ADDON_URL="$2"
            shift 2
            ;;
        *)
            if [[ -z "$ADDON_NAME" ]]; then
                ADDON_NAME="$1"
            else
                echo -e "${RED}Error: Unknown option $1${NC}"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate addon name
if [[ -z "$ADDON_NAME" ]]; then
    echo -e "${RED}Error: Add-on name is required${NC}"
    show_help
    exit 1
fi

# Clean addon name for directory/slug
ADDON_SLUG=$(echo "$ADDON_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
ADDON_DIR="$ADDONS_DIR/$ADDON_SLUG"

# Check if addon already exists
if [[ -d "$ADDON_DIR" ]]; then
    echo -e "${RED}Error: Add-on directory already exists: $ADDON_DIR${NC}"
    exit 1
fi

# Set default description if not provided
if [[ -z "$ADDON_DESCRIPTION" ]]; then
    ADDON_DESCRIPTION="Custom Hailo AI add-on: $ADDON_NAME"
fi

echo -e "${BLUE}Generating Home Assistant Hailo Add-on${NC}"
echo -e "${BLUE}=====================================${NC}"
echo "Name: $ADDON_NAME"
echo "Slug: $ADDON_SLUG"
echo "Description: $ADDON_DESCRIPTION"
echo "Version: $ADDON_VERSION"
echo "Directory: $ADDON_DIR"
echo ""

# Create addon directory
echo -e "${YELLOW}Creating add-on directory...${NC}"
mkdir -p "$ADDON_DIR"

# Copy template files
echo -e "${YELLOW}Copying template files...${NC}"
cp -r "$TEMPLATE_DIR"/* "$ADDON_DIR/"

# Update config.yaml with addon-specific values
echo -e "${YELLOW}Updating configuration...${NC}"
sed -i.bak "s/name: Hailo AI Add-on Template/name: $ADDON_NAME/" "$ADDON_DIR/config.yaml"
sed -i.bak "s/version: \"1.0.0\"/version: \"$ADDON_VERSION\"/" "$ADDON_DIR/config.yaml"
sed -i.bak "s/slug: hailo_ai_addon_template/slug: $ADDON_SLUG/" "$ADDON_DIR/config.yaml"
sed -i.bak "s/description: Template for building custom Hailo AI add-ons/description: $ADDON_DESCRIPTION/" "$ADDON_DIR/config.yaml"

if [[ -n "$ADDON_URL" ]]; then
    sed -i.bak "s|url: \"https://github.com/your-repo/hailo-addon\"|url: \"$ADDON_URL\"|" "$ADDON_DIR/config.yaml"
fi

# Update Dockerfile labels
sed -i.bak "s/io.hass.name=\"Hailo AI Add-on Template\"/io.hass.name=\"$ADDON_NAME\"/" "$ADDON_DIR/Dockerfile"
sed -i.bak "s/io.hass.description=\"Template for building custom Hailo AI add-ons\"/io.hass.description=\"$ADDON_DESCRIPTION\"/" "$ADDON_DIR/Dockerfile"
sed -i.bak "s/io.hass.version=\"1.0.0\"/io.hass.version=\"$ADDON_VERSION\"/" "$ADDON_DIR/Dockerfile"

# Clean up backup files
rm -f "$ADDON_DIR/config.yaml.bak" "$ADDON_DIR/Dockerfile.bak"

# Create addon-specific README
cat > "$ADDON_DIR/README.md" << EOF
# $ADDON_NAME

$ADDON_DESCRIPTION

## Features

- Hailo AI hardware acceleration
- Home Assistant integration
- RESTful API interface
- Configurable model loading
- Real-time inference

## Installation

1. Copy this add-on to your Home Assistant addons directory
2. Place your Hailo packages in the \`hailo_packages/\` directory
3. Install through Home Assistant Add-on Store

## Configuration

\`\`\`yaml
model_path: "/share/hailo/models"
device_id: "0000:03:00.0"
log_level: "info"
enable_api: true
api_port: 8080
\`\`\`

## Development

This add-on was generated from the Home Assistant Hailo Add-on template.

### Building

\`\`\`bash
# From workspace root
./scripts/build-addon.sh ./addons/$ADDON_SLUG
\`\`\`

### Testing

\`\`\`bash
# Run locally
docker run --rm -it --device=/dev/hailo0 local/aarch64-addon-${ADDON_SLUG}:${ADDON_VERSION}
\`\`\`

## API Endpoints

- \`GET /health\` - Health check
- \`GET /models\` - List available models
- \`POST /inference\` - Run inference

## Support

For support and development, see the main workspace documentation.
EOF

echo ""
echo -e "${GREEN}✓ Add-on generated successfully!${NC}"
echo -e "${GREEN}Location: $ADDON_DIR${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Add your Hailo packages to: ${ADDON_DIR}/hailo_packages/"
echo "2. Modify the source code in: ${ADDON_DIR}/src/"
echo "3. Build the add-on: ./scripts/build-addon.sh ./addons/$ADDON_SLUG"
echo "4. Install in Home Assistant"
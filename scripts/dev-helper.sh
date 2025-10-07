#!/bin/bash
# ==============================================================================
# Home Assistant Add-on Development Helper
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

show_help() {
    echo -e "${BLUE}Home Assistant Hailo Add-on Development Helper${NC}"
    echo -e "${BLUE}==============================================${NC}"
    echo ""
    echo "Usage: $0 COMMAND [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  generate ADDON_NAME        Generate new add-on from template"
    echo "  build ADDON_PATH           Build an add-on"
    echo "  list                       List all add-ons in workspace"
    echo "  clean                      Clean build artifacts"
    echo "  validate ADDON_PATH        Validate add-on configuration"
    echo ""
    echo "Examples:"
    echo "  $0 generate my-hailo-detector"
    echo "  $0 build ./addons/my-hailo-detector"
    echo "  $0 list"
    echo "  $0 validate ./addons/my-hailo-detector"
}

list_addons() {
    echo -e "${BLUE}Available Add-ons${NC}"
    echo -e "${BLUE}=================${NC}"
    
    if [[ ! -d "$WORKSPACE_DIR/addons" ]]; then
        echo "No add-ons directory found."
        return
    fi
    
    found_addons=false
    for addon_dir in "$WORKSPACE_DIR/addons"/*; do
        if [[ -d "$addon_dir" && -f "$addon_dir/config.yaml" ]]; then
            found_addons=true
            addon_name=$(basename "$addon_dir")
            
            # Extract info from config.yaml
            name=$(grep "^name:" "$addon_dir/config.yaml" 2>/dev/null | cut -d'"' -f2 | cut -d"'" -f2 | xargs || echo "Unknown")
            version=$(grep "^version:" "$addon_dir/config.yaml" 2>/dev/null | cut -d'"' -f2 | cut -d"'" -f2 | xargs || echo "Unknown")
            description=$(grep "^description:" "$addon_dir/config.yaml" 2>/dev/null | cut -d'"' -f2 | cut -d"'" -f2 | xargs || echo "No description")
            
            echo -e "${GREEN}$addon_name${NC}"
            echo "  Name: $name"
            echo "  Version: $version"
            echo "  Description: $description"
            echo "  Path: $addon_dir"
            echo ""
        fi
    done
    
    if [[ "$found_addons" == false ]]; then
        echo "No add-ons found in workspace."
        echo ""
        echo "To create a new add-on:"
        echo "  $0 generate my-addon-name"
    fi
}

validate_addon() {
    local addon_path="$1"
    
    if [[ -z "$addon_path" ]]; then
        echo -e "${RED}Error: Add-on path required for validation${NC}"
        return 1
    fi
    
    if [[ ! -d "$addon_path" ]]; then
        echo -e "${RED}Error: Add-on directory not found: $addon_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Validating Add-on: $addon_path${NC}"
    echo -e "${BLUE}==========================${NC}"
    
    local errors=0
    
    # Check required files
    required_files=("config.yaml" "Dockerfile" "run.sh")
    for file in "${required_files[@]}"; do
        if [[ -f "$addon_path/$file" ]]; then
            echo -e "${GREEN}✓${NC} $file exists"
        else
            echo -e "${RED}✗${NC} $file missing"
            ((errors++))
        fi
    done
    
    # Check config.yaml syntax
    if [[ -f "$addon_path/config.yaml" ]]; then
        if python3 -c "import yaml; yaml.safe_load(open('$addon_path/config.yaml'))" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} config.yaml syntax valid"
        else
            echo -e "${RED}✗${NC} config.yaml syntax invalid"
            ((errors++))
        fi
    fi
    
    # Check Dockerfile
    if [[ -f "$addon_path/Dockerfile" ]]; then
        if grep -q "FROM " "$addon_path/Dockerfile"; then
            echo -e "${GREEN}✓${NC} Dockerfile has FROM instruction"
        else
            echo -e "${RED}✗${NC} Dockerfile missing FROM instruction"
            ((errors++))
        fi
    fi
    
    # Check run.sh permissions
    if [[ -f "$addon_path/run.sh" ]]; then
        if [[ -x "$addon_path/run.sh" ]]; then
            echo -e "${GREEN}✓${NC} run.sh is executable"
        else
            echo -e "${YELLOW}!${NC} run.sh is not executable (will be fixed during build)"
        fi
    fi
    
    # Check hailo_packages directory
    if [[ -d "$addon_path/hailo_packages" ]]; then
        hef_count=$(find "$addon_path/hailo_packages" -name "*.hef" | wc -l)
        deb_count=$(find "$addon_path/hailo_packages" -name "*_arm64.deb" | wc -l)
        whl_count=$(find "$addon_path/hailo_packages" -name "*-linux_aarch64.whl" | wc -l)
        
        echo -e "${GREEN}✓${NC} hailo_packages directory exists"
        echo "  HEF models: $hef_count"
        echo "  DEB packages: $deb_count"
        echo "  Python wheels: $whl_count"
        
        if [[ $hef_count -eq 0 ]]; then
            echo -e "${YELLOW}!${NC} No HEF model files found"
        fi
    else
        echo -e "${YELLOW}!${NC} hailo_packages directory not found"
    fi
    
    echo ""
    if [[ $errors -eq 0 ]]; then
        echo -e "${GREEN}✓ Validation passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ Validation failed with $errors errors${NC}"
        return 1
    fi
}

clean_artifacts() {
    echo -e "${BLUE}Cleaning Build Artifacts${NC}"
    echo -e "${BLUE}========================${NC}"
    
    # Clean Docker images
    echo "Cleaning Docker images..."
    docker images --format "table {{.Repository}}:{{.Tag}}" | grep "local/.*-addon-" | while read image; do
        if [[ -n "$image" && "$image" != "REPOSITORY:TAG" ]]; then
            echo "Removing: $image"
            docker rmi "$image" 2>/dev/null || true
        fi
    done
    
    # Clean build cache
    echo "Cleaning Docker build cache..."
    docker builder prune -f 2>/dev/null || true
    
    echo -e "${GREEN}✓ Cleanup completed${NC}"
}

# Main command processing
case "${1:-help}" in
    generate)
        shift
        exec "$SCRIPT_DIR/generate-addon.sh" "$@"
        ;;
    build)
        shift
        exec "$SCRIPT_DIR/build-addon.sh" "$@"
        ;;
    list)
        list_addons
        ;;
    validate)
        validate_addon "$2"
        ;;
    clean)
        clean_artifacts
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
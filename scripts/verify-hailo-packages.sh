#!/bin/bash
# ==============================================================================
# 🔍 Hailo Package Verification Tool
# ==============================================================================
# Standalone script to verify Hailo packages before installation
# Provides detailed guidance and helpful error messages
# ==============================================================================

set -e

# Configuration
PACKAGES_DIR="${1:-/share/hailo/packages}"
SCRIPT_NAME="$(basename "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Required packages with detailed information
declare -A PACKAGE_INFO=(
    ["hailort_*_arm64.deb"]="HailoRT Runtime Library|Runtime for Hailo hardware acceleration|50-200MB"
    ["hailo_ai_sw_suite_*_arm64.deb"]="Hailo AI Software Suite|Core AI processing tools and libraries|800-1500MB" 
    ["hailo_model_zoo_*_arm64.deb"]="Hailo Model Zoo|Pre-trained AI models for various tasks|500-1000MB"
    ["hailo_dataflow_compiler_*_arm64.deb"]="Hailo Dataflow Compiler|Tool for optimizing models for Hailo hardware|300-600MB"
)

# Alternative patterns (Python wheels, etc.)
declare -A ALT_PATTERNS=(
    ["hailort-*-cp*-linux_aarch64.whl"]="HailoRT Python SDK|Python bindings for HailoRT|10-50MB"
    ["hailo_platform-*-py3-none-linux_aarch64.whl"]="Hailo Platform Python Package|High-level Python API|5-20MB"
)

# Display header
display_header() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "┌────────────────────────────────────────────────────────────────────────┐"
    echo "│                    🔍 Hailo Package Verification Tool                   │"
    echo "│                                                                        │"
    echo "│  This tool helps you verify that all required Hailo packages are      │"
    echo "│  properly downloaded and ready for installation.                      │"
    echo "│                                                                        │"
    echo "│  If packages are missing, you'll get step-by-step instructions to     │"
    echo "│  download them from the official Hailo Developer Zone.               │"
    echo "└────────────────────────────────────────────────────────────────────────┘"
    echo -e "${NC}"
    echo ""
}

# Show usage information
show_usage() {
    echo -e "${BOLD}Usage:${NC}"
    echo "  $SCRIPT_NAME [package_directory]"
    echo ""
    echo -e "${BOLD}Examples:${NC}"
    echo "  $SCRIPT_NAME                              # Use default: /share/hailo/packages"
    echo "  $SCRIPT_NAME /home/user/hailo-downloads   # Use custom directory"
    echo ""
    echo -e "${BOLD}What this tool checks:${NC}"
    echo "  ✓ Package directory exists and is accessible"
    echo "  ✓ All required .deb packages are present"
    echo "  ✓ Package file sizes are reasonable"
    echo "  ✓ Files are not corrupted"
    echo "  ✓ Architecture matches (ARM64/aarch64)"
    echo ""
}

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo ""
    echo -e "${CYAN}${BOLD}=== $1 ===${NC}"
    echo ""
}

# Check if directory exists and is accessible
check_directory() {
    log_header "Directory Check"
    
    if [[ ! -d "$PACKAGES_DIR" ]]; then
        log_error "Package directory does not exist: $PACKAGES_DIR"
        echo ""
        echo -e "${YELLOW}💡 SOLUTION - Create Package Directory:${NC}"
        echo ""
        echo "1. Create the directory:"
        echo -e "   ${CYAN}mkdir -p \"$PACKAGES_DIR\"${NC}"
        echo ""
        echo "2. Set proper permissions:"
        echo -e "   ${CYAN}chmod 755 \"$PACKAGES_DIR\"${NC}"
        echo ""
        echo "3. Download Hailo packages from:"
        echo -e "   ${BLUE}https://hailo.ai/developer-zone/${NC}"
        echo ""
        echo "4. Copy all .deb files to the directory"
        echo ""
        echo "5. Run this verification tool again"
        echo ""
        return 1
    fi
    
    if [[ ! -r "$PACKAGES_DIR" ]]; then
        log_error "Package directory is not readable: $PACKAGES_DIR"
        echo ""
        echo -e "${YELLOW}💡 SOLUTION - Fix Permissions:${NC}"
        echo -e "   ${CYAN}chmod 755 \"$PACKAGES_DIR\"${NC}"
        echo ""
        return 1
    fi
    
    log_success "Package directory exists and is accessible ✓"
    log_info "Directory: $PACKAGES_DIR"
    
    # Show directory contents summary
    local total_files=$(find "$PACKAGES_DIR" -type f | wc -l)
    local deb_files=$(find "$PACKAGES_DIR" -name "*.deb" | wc -l)
    local whl_files=$(find "$PACKAGES_DIR" -name "*.whl" | wc -l)
    
    log_info "Contents: $total_files total files ($deb_files .deb, $whl_files .whl)"
    
    return 0
}

# Verify required packages
verify_packages() {
    log_header "Package Verification"
    
    local missing_packages=()
    local found_packages=()
    local package_details=()
    
    echo -e "${BLUE}Checking required packages...${NC}"
    echo ""
    
    # Check each required package
    for pattern in "${!PACKAGE_INFO[@]}"; do
        local info="${PACKAGE_INFO[$pattern]}"
        local name=$(echo "$info" | cut -d'|' -f1)
        local description=$(echo "$info" | cut -d'|' -f2)
        local size_range=$(echo "$info" | cut -d'|' -f3)
        
        local found_files=($(find "$PACKAGES_DIR" -name "$pattern" 2>/dev/null))
        
        printf "%-40s " "$name:"
        
        if [[ ${#found_files[@]} -eq 0 ]]; then
            echo -e "${RED}❌ MISSING${NC}"
            missing_packages+=("$pattern|$name|$description")
        elif [[ ${#found_files[@]} -eq 1 ]]; then
            local filename=$(basename "${found_files[0]}")
            echo -e "${GREEN}✅ FOUND${NC} → $filename"
            found_packages+=("${found_files[0]}")
            package_details+=("$filename|$name|$description|$size_range")
        else
            local filename=$(basename "${found_files[0]}")
            echo -e "${YELLOW}⚠️  MULTIPLE${NC} → Using $filename"
            log_warning "   Found ${#found_files[@]} files matching $pattern"
            found_packages+=("${found_files[0]}")
            package_details+=("$filename|$name|$description|$size_range")
        fi
    done
    
    echo ""
    
    # Handle missing packages
    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        log_error "Missing ${#missing_packages[@]} required package(s)"
        echo ""
        echo -e "${RED}${BOLD}MISSING PACKAGES:${NC}"
        
        for missing in "${missing_packages[@]}"; do
            local pattern=$(echo "$missing" | cut -d'|' -f1)
            local name=$(echo "$missing" | cut -d'|' -f2) 
            local description=$(echo "$missing" | cut -d'|' -f3)
            
            echo ""
            echo -e "${YELLOW}📦 $name${NC}"
            echo "   Description: $description"
            echo "   File pattern: $pattern"
            echo "   Download from: Hailo Developer Zone"
        done
        
        echo ""
        show_download_instructions
        return 1
    fi
    
    # Verify found packages
    log_success "All required packages found! ✓"
    echo ""
    
    verify_package_integrity "${found_packages[@]}"
    show_package_summary "${package_details[@]}"
    
    return 0
}

# Verify package file integrity
verify_package_integrity() {
    local packages=("$@")
    
    log_header "Package Integrity Check"
    
    local integrity_issues=()
    
    for package_file in "${packages[@]}"; do
        local filename=$(basename "$package_file")
        local size_mb=$(du -m "$package_file" | cut -f1)
        
        printf "%-50s " "$filename:"
        
        # Check file size (basic sanity check)
        if [[ $size_mb -lt 5 ]]; then
            echo -e "${RED}❌ TOO SMALL${NC} (${size_mb}MB - likely corrupted)"
            integrity_issues+=("$filename: File too small ($size_mb MB)")
        elif [[ $size_mb -gt 5000 ]]; then
            echo -e "${YELLOW}⚠️  VERY LARGE${NC} (${size_mb}MB - verify correct file)"
            integrity_issues+=("$filename: Unusually large ($size_mb MB)")
        else
            echo -e "${GREEN}✅ SIZE OK${NC} (${size_mb}MB)"
        fi
        
        # Check if file is readable and not corrupted
        if ! file "$package_file" | grep -q "Debian binary package"; then
            integrity_issues+=("$filename: Not a valid Debian package")
        fi
        
        # Check architecture
        if ! dpkg --info "$package_file" 2>/dev/null | grep -q "arm64\|aarch64"; then
            integrity_issues+=("$filename: Wrong architecture (not ARM64)")
        fi
    done
    
    echo ""
    
    if [[ ${#integrity_issues[@]} -gt 0 ]]; then
        log_warning "Found ${#integrity_issues[@]} integrity issue(s):"
        for issue in "${integrity_issues[@]}"; do
            log_warning "   • $issue"
        done
        echo ""
        echo -e "${YELLOW}💡 RECOMMENDATIONS:${NC}"
        echo "1. Re-download any corrupted or wrong-architecture packages"
        echo "2. Verify downloads completed successfully"
        echo "3. Check available disk space during download"
        echo "4. Use a reliable internet connection for large files"
        echo ""
    else
        log_success "All packages passed integrity checks ✓"
    fi
}

# Show package summary
show_package_summary() {
    local details=("$@")
    
    log_header "Package Summary"
    
    local total_size=0
    
    echo -e "${BOLD}Found Packages:${NC}"
    echo ""
    
    for detail in "${details[@]}"; do
        local filename=$(echo "$detail" | cut -d'|' -f1)
        local name=$(echo "$detail" | cut -d'|' -f2)
        local description=$(echo "$detail" | cut -d'|' -f3)
        local size_range=$(echo "$detail" | cut -d'|' -f4)
        
        local actual_size=$(du -m "$PACKAGES_DIR/$filename" | cut -f1)
        total_size=$((total_size + actual_size))
        
        echo -e "${GREEN}✅${NC} ${BOLD}$name${NC}"
        echo "   File: $filename"
        echo "   Size: ${actual_size}MB (expected: $size_range)"
        echo "   Description: $description"
        echo ""
    done
    
    echo -e "${CYAN}📊 Total package size: ${total_size}MB${NC}"
    
    # Check available disk space
    local available_space=$(df -m /usr | tail -1 | awk '{print $4}')
    local required_space=$((total_size * 3))  # Need 3x space for installation
    
    if [[ $available_space -lt $required_space ]]; then
        log_warning "Low disk space: ${available_space}MB available, ${required_space}MB recommended"
        echo -e "${YELLOW}💡 Free up disk space before installation${NC}"
    else
        log_success "Sufficient disk space: ${available_space}MB available ✓"
    fi
}

# Show download instructions for missing packages
show_download_instructions() {
    echo -e "${CYAN}${BOLD}📥 HOW TO DOWNLOAD HAILO PACKAGES${NC}"
    echo ""
    echo -e "${YELLOW}Step 1: Create Hailo Developer Account${NC}"
    echo "1. Visit: https://hailo.ai/developer-zone/"
    echo "2. Click 'Sign Up' or 'Register'"
    echo "3. Fill out registration form with valid email"
    echo "4. Verify your email address"
    echo "5. Complete profile setup"
    echo ""
    
    echo -e "${YELLOW}Step 2: Access Downloads Section${NC}"
    echo "1. Login to your Hailo Developer Zone account"
    echo "2. Navigate to 'Downloads', 'Software', or 'SDK' section"
    echo "3. Look for the latest software release"
    echo ""
    
    echo -e "${YELLOW}Step 3: Download Required Files${NC}"
    echo "Download these specific files for ARM64 architecture:"
    echo ""
    
    for pattern in "${!PACKAGE_INFO[@]}"; do
        local info="${PACKAGE_INFO[$pattern]}"
        local name=$(echo "$info" | cut -d'|' -f1)
        local description=$(echo "$info" | cut -d'|' -f2)
        
        echo -e "   ${BOLD}$name${NC}"
        echo "   • File pattern: $pattern"
        echo "   • Purpose: $description"
        echo "   • ⚠️  Must be ARM64/aarch64 version"
        echo ""
    done
    
    echo -e "${YELLOW}Step 4: Transfer to Home Assistant${NC}"
    echo "1. Copy all downloaded .deb files to: $PACKAGES_DIR"
    echo "2. Ensure proper permissions: chmod 644 *.deb"
    echo "3. Run this verification tool again"
    echo ""
    
    echo -e "${BLUE}💡 TIPS:${NC}"
    echo "• Create a dedicated folder for downloads to stay organized"
    echo "• Double-check architecture (ARM64/aarch64) before downloading"
    echo "• Download the latest available versions for best compatibility"
    echo "• Keep packages for future reinstallations"
    echo ""
}

# Show next steps after successful verification
show_next_steps() {
    log_header "🎉 Verification Complete!"
    
    echo -e "${GREEN}${BOLD}All Hailo packages are ready for installation!${NC}"
    echo ""
    
    echo -e "${CYAN}📋 Next Steps:${NC}"
    echo "1. Install the Hailo AI Terminal add-on from HACS"
    echo "2. Configure the add-on settings"
    echo "3. Start the add-on (packages will be installed automatically)"
    echo "4. Access the web interface: http://your-ha-ip:8080"
    echo ""
    
    echo -e "${BLUE}🔧 Add-on Configuration Tips:${NC}"
    echo "• Set model_path: /share/hailo/models"
    echo "• Check device_id matches your Hailo hardware"
    echo "• Enable monitoring for resource tracking"
    echo "• Start with log_level: info for detailed startup logs"
    echo ""
    
    echo -e "${YELLOW}⚠️  Important Notes:${NC}"
    echo "• First startup will take longer due to package installation"
    echo "• Monitor add-on logs during initial setup"
    echo "• Ensure Hailo hardware is properly connected"
    echo "• Have at least 4GB RAM available for AI models"
    echo ""
}

# Main execution function
main() {
    display_header
    
    # Show usage if help requested
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    echo -e "${BOLD}Package Directory:${NC} $PACKAGES_DIR"
    echo ""
    
    # Run verification steps
    if check_directory; then
        if verify_packages; then
            show_next_steps
            echo -e "${GREEN}${BOLD}✅ VERIFICATION SUCCESSFUL!${NC}"
            exit 0
        else
            echo -e "${RED}${BOLD}❌ VERIFICATION FAILED${NC}"
            echo ""
            echo -e "${YELLOW}Please download missing packages and run verification again.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}${BOLD}❌ DIRECTORY CHECK FAILED${NC}"
        exit 1
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
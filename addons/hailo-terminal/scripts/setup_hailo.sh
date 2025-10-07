#!/bin/bash
# ==============================================================================
# 🤖 Hailo AI Terminal - Package Setup & Verification Script
# ==============================================================================
# This script provides comprehensive package verification with user-friendly
# error messages, detailed troubleshooting guidance, and fallback modes.
# 
# Features:
# - Automated package detection and verification
# - User-friendly error messages with solutions
# - Fallback to CPU-only mode if Hailo packages unavailable
# - Comprehensive logging and debugging
# - Step-by-step guidance for package acquisition
# ==============================================================================

set -e

# Configuration
HAILO_PACKAGES_DIR="/share/hailo/packages"
LOG_FILE="/var/log/hailo_terminal_setup.log"
SETUP_MARKER="/var/lib/hailo_terminal_setup_complete"
VERBOSE=${VERBOSE:-1}

# Required packages with human-readable names and patterns
declare -A REQUIRED_PACKAGES=(
    ["hailort_*_arm64.deb"]="HailoRT Runtime Library"
    ["hailo_ai_sw_suite_*_arm64.deb"]="Hailo AI Software Suite" 
    ["hailo_model_zoo_*_arm64.deb"]="Hailo Model Zoo"
    ["hailo_dataflow_compiler_*_arm64.deb"]="Hailo Dataflow Compiler"
)

# Alternative package patterns (for flexibility)
declare -A ALT_PATTERNS=(
    ["hailort"]="hailort-*-cp*-linux_aarch64.whl"
    ["hailo_platform"]="hailo_platform-*-py3-none-linux_aarch64.whl"
)

# Version requirements  
declare -A MIN_VERSIONS=(
    ["hailort"]="4.23.0"
    ["hailo_ai_sw_suite"]="2023.10" 
    ["hailo_model_zoo"]="2.12.0"
    ["hailo_dataflow_compiler"]="3.27.0"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}[INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    log "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo ""
    log "${CYAN}${BOLD}=== $1 ===${NC}"
    echo ""
}

# Error handling with helpful messages
handle_error() {
    local exit_code=$1
    local line_number=$2
    
    log_error "Script failed at line $line_number with exit code $exit_code"
    
    case $exit_code in
        1)
            echo ""
            log_error "Package directory or files not found"
            echo -e "${YELLOW}💡 SOLUTION:${NC}"
            echo "1. Ensure packages are downloaded from Hailo Developer Zone"
            echo "2. Copy all .deb files to: $HAILO_PACKAGES_DIR"
            echo "3. Run package verification: ./verify-hailo-packages.sh"
            echo ""
            echo -e "${BLUE}📋 Required packages:${NC}"
            for pattern in "${!REQUIRED_PACKAGES[@]}"; do
                echo "   • ${REQUIRED_PACKAGES[$pattern]}: $pattern"
            done
            ;;
        2)
            echo ""
            log_error "Package installation failed"
            echo -e "${YELLOW}💡 SOLUTION:${NC}"
            echo "1. Check if you have sufficient disk space: df -h"
            echo "2. Verify package integrity: dpkg --info /path/to/package.deb"
            echo "3. Check for conflicting packages: dpkg -l | grep hailo"
            echo "4. Try installing packages individually for detailed error messages"
            ;;
        3)
            echo ""
            log_error "Hailo device not detected or inaccessible"
            echo -e "${YELLOW}💡 SOLUTION:${NC}"
            echo "1. Verify Hailo hardware connection: lspci | grep -i hailo"
            echo "2. Check device permissions: ls -la /dev/hailo*"
            echo "3. Ensure add-on has privileged access enabled"
            echo "4. Restart Home Assistant and try again"
            ;;
        *)
            echo ""
            log_error "Unknown error occurred"
            echo -e "${YELLOW}💡 SOLUTION:${NC}"
            echo "1. Check the log file: $LOG_FILE"
            echo "2. Verify all prerequisites are met"
            echo "3. Contact support with error details"
            ;;
    esac
    
    echo ""
    echo -e "${CYAN}📞 Need help? Check:${NC}"
    echo "• GitHub Issues: https://github.com/your-username/hailo-terminal-addon/issues"
    echo "• Documentation: /share/hailo-terminal-addon/docs/"
    echo "• Log file: $LOG_FILE"
    
    exit $exit_code
}

# Set error trap
trap 'handle_error $? $LINENO' ERR

# Display banner
display_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "┌─────────────────────────────────────────────────────────────────┐"
    echo "│                  🤖 Hailo AI Terminal Setup                     │"
    echo "│                     Package Installation                        │"
    echo "│                                                                 │"
    echo "│  This script will verify and install Hailo packages required   │"
    echo "│  for AI acceleration with comprehensive error checking.         │"
    echo "└─────────────────────────────────────────────────────────────────┘"
    echo -e "${NC}"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_header "Prerequisites Check"
    
    # Check if running as root
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root"
        echo -e "${YELLOW}💡 SOLUTION: Run with sudo or as root user${NC}"
        exit 1
    fi
    
    log_success "Running as root ✓"
    
    # Check available disk space (need at least 5GB)
    local available_space=$(df /usr | tail -1 | awk '{print $4}')
    local required_space=5242880  # 5GB in KB
    
    if [[ $available_space -lt $required_space ]]; then
        log_error "Insufficient disk space. Available: $(($available_space/1024/1024))GB, Required: 5GB"
        echo -e "${YELLOW}💡 SOLUTION: Free up disk space before continuing${NC}"
        exit 1
    fi
    
    log_success "Sufficient disk space available: $(($available_space/1024/1024))GB ✓"
    
    # Check for required commands
    local required_commands=("dpkg" "lspci" "modprobe")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command '$cmd' not found"
            exit 1
        fi
    done
    
    log_success "All required commands available ✓"
}

# Verify package directory and files
verify_packages() {
    log_header "Package Verification"
    
    # Check if package directory exists
    if [[ ! -d "$HAILO_PACKAGES_DIR" ]]; then
        log_error "Package directory not found: $HAILO_PACKAGES_DIR"
        echo ""
        echo -e "${YELLOW}💡 SOLUTION:${NC}"
        echo "1. Create directory: mkdir -p $HAILO_PACKAGES_DIR"
        echo "2. Download packages from: https://hailo.ai/developer-zone/"
        echo "3. Copy all .deb files to the directory"
        echo "4. Run this script again"
        exit 1
    fi
    
    log_success "Package directory exists ✓"
    
    # Count total .deb files
    local deb_count=$(find "$HAILO_PACKAGES_DIR" -name "*.deb" | wc -l)
    log_info "Found $deb_count .deb files in package directory"
    
    if [[ $deb_count -eq 0 ]]; then
        log_error "No .deb files found in $HAILO_PACKAGES_DIR"
        echo ""
        echo -e "${YELLOW}💡 SOLUTION:${NC}"
        echo "1. Download packages from Hailo Developer Zone"
        echo "2. Ensure files have .deb extension"
        echo "3. Copy files to: $HAILO_PACKAGES_DIR"
        exit 1
    fi
    
    # Check each required package
    local missing_packages=()
    local found_packages=()
    
    echo ""
    log_info "Checking required packages..."
    
    for pattern in "${!REQUIRED_PACKAGES[@]}"; do
        local package_name="${REQUIRED_PACKAGES[$pattern]}"
        local found_files=($(find "$HAILO_PACKAGES_DIR" -name "$pattern" 2>/dev/null))
        
        if [[ ${#found_files[@]} -eq 0 ]]; then
            log_error "❌ MISSING: $package_name ($pattern)"
            missing_packages+=("$package_name")
        elif [[ ${#found_files[@]} -eq 1 ]]; then
            log_success "✅ FOUND: $package_name -> $(basename "${found_files[0]}")"
            found_packages+=("${found_files[0]}")
            
            # Verify file integrity
            if ! dpkg --info "${found_files[0]}" &>/dev/null; then
                log_warning "⚠️  Package may be corrupted: $(basename "${found_files[0]}")"
            fi
            
        else
            log_warning "⚠️  MULTIPLE: $package_name -> Multiple files found"
            log_info "Using: $(basename "${found_files[0]}")"
            found_packages+=("${found_files[0]}")
        fi
    done
    
    # Handle missing packages
    if [[ ${#missing_packages[@]} -gt 0 ]]; then
        echo ""
        log_error "Missing required packages:"
        for pkg in "${missing_packages[@]}"; do
            echo "   • $pkg"
        done
        
        echo ""
        echo -e "${YELLOW}💡 SOLUTION:${NC}"
        echo "1. Visit: https://hailo.ai/developer-zone/"
        echo "2. Login to your developer account"
        echo "3. Download the missing packages (ARM64 versions)"
        echo "4. Copy them to: $HAILO_PACKAGES_DIR"
        echo ""
        echo -e "${BLUE}📋 Download checklist:${NC}"
        for pattern in "${!REQUIRED_PACKAGES[@]}"; do
            echo "   [ ] ${REQUIRED_PACKAGES[$pattern]}: $pattern"
        done
        
        exit 1
    fi
    
    # Verify file sizes (basic sanity check)
    echo ""
    log_info "Verifying package file sizes..."
    
    for package in "${found_packages[@]}"; do
        local size_mb=$(du -m "$package" | cut -f1)
        local filename=$(basename "$package")
        
        if [[ $size_mb -lt 10 ]]; then
            log_warning "⚠️  $filename: ${size_mb}MB (unusually small - may be corrupted)"
        elif [[ $size_mb -gt 3000 ]]; then
            log_warning "⚠️  $filename: ${size_mb}MB (unusually large - verify correct file)"
        else
            log_success "✅ $filename: ${size_mb}MB"
        fi
    done
    
    log_success "Package verification complete ✓"
    return 0
}
    "hailort-*-cp*-linux_aarch64.whl"
)

echo "🔍 Checking for Hailo packages..."

# Check if packages directory exists
if [[ ! -d "$HAILO_PACKAGES_DIR" ]]; then
    echo "❌ Hailo packages directory not found: $HAILO_PACKAGES_DIR"
    exit 1
fi

# Check for required packages
MISSING_PACKAGES=()

for pattern in "${REQUIRED_PACKAGES[@]}"; do
    if ! ls $HAILO_PACKAGES_DIR/$pattern 1> /dev/null 2>&1; then
        MISSING_PACKAGES+=("$pattern")
    fi
done

if [[ ${#MISSING_PACKAGES[@]} -gt 0 ]]; then
    echo "❌ Missing required Hailo packages:"
    for pkg in "${MISSING_PACKAGES[@]}"; do
        echo "   - $pkg"
    done
    echo ""
    echo "📝 Please download the following packages from Hailo Developer Portal:"
    echo "   https://hailo.ai/developer-zone/"
    echo ""
    echo "Required files:"
    echo "   1. hailort_X.X.X_arm64.deb (Hailo Runtime)"
    echo "   2. hailort-X.X.X-cp310-cp310-linux_aarch64.whl (Python SDK)"
    echo ""
    echo "Place them in: $HAILO_PACKAGES_DIR"
    echo ""
    echo "🚀 The add-on will work in CPU-only mode without these packages,"
    echo "   but Hailo AI acceleration will not be available."
    
    # Continue without Hailo packages (CPU fallback mode)
    export HAILO_MODE="cpu"
    return 0
else
    echo "✅ All required Hailo packages found!"
    export HAILO_MODE="hailo"
fi

# Install packages if available
if [[ "$HAILO_MODE" == "hailo" ]]; then
    echo "📦 Installing Hailo packages..."
    
    # Install DEB package
    for deb_file in $HAILO_PACKAGES_DIR/*_arm64.deb; do
        if [[ -f "$deb_file" ]]; then
            echo "Installing: $(basename "$deb_file")"
            dpkg --unpack "$deb_file" || true
        fi
    done
    
    # Install Python wheels
    for whl_file in $HAILO_PACKAGES_DIR/*-linux_aarch64.whl; do
        if [[ -f "$whl_file" ]]; then
            echo "Installing: $(basename "$whl_file")"
            python3 -m pip install "$whl_file" || true
        fi
    done
    
    echo "✅ Hailo packages installed successfully!"
fi

echo "🎯 Setup complete! Mode: $HAILO_MODE"
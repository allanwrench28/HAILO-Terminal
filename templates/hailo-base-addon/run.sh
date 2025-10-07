#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Hailo AI Add-on
# Runs the Hailo AI application
# ==============================================================================

# Get configuration from Home Assistant
MODEL_PATH=$(bashio::config 'model_path')
DEVICE_ID=$(bashio::config 'device_id')
LOG_LEVEL=$(bashio::config 'log_level')
ENABLE_API=$(bashio::config 'enable_api')
API_PORT=$(bashio::config 'api_port')

# Log configuration
bashio::log.blue "Starting Hailo AI Add-on..."
bashio::log.info "Model path: ${MODEL_PATH}"
bashio::log.info "Device ID: ${DEVICE_ID}"
bashio::log.info "Log level: ${LOG_LEVEL}"
bashio::log.info "API enabled: ${ENABLE_API}"

# Create model directory if it doesn't exist
if [[ ! -d "${MODEL_PATH}" ]]; then
    bashio::log.info "Creating model directory: ${MODEL_PATH}"
    mkdir -p "${MODEL_PATH}"
fi

# Check if Hailo device is available
if [[ ! -e "/dev/hailo0" ]]; then
    bashio::log.warning "Hailo device not found at /dev/hailo0"
    bashio::log.warning "Make sure the Hailo device is properly connected"
fi

# Export environment variables for the application
export MODEL_PATH="${MODEL_PATH}"
export DEVICE_ID="${DEVICE_ID}"
export LOG_LEVEL="${LOG_LEVEL}"
export ENABLE_API="${ENABLE_API}"
export API_PORT="${API_PORT}"

# Start the main application
bashio::log.info "Starting Hailo AI application..."
cd /app/src
exec python3 main.py
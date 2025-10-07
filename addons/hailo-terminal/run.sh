#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Hailo AI Terminal
# Runs the Hailo AI Terminal application
# ==============================================================================

# Get configuration from Home Assistant
# Hardware Configuration
MODEL_PATH=$(bashio::config 'model_path')
DEVICE_ID=$(bashio::config 'device_id')

# AI Backend Configuration
AI_BACKEND=$(bashio::config 'ai_backend')
AI_MODEL=$(bashio::config 'ai_model')
OPENAI_API_KEY=$(bashio::config 'openai_api_key')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key')
CUSTOM_API_URL=$(bashio::config 'custom_api_url')

# Performance Settings
MAX_CONTEXT_LENGTH=$(bashio::config 'max_context_length')
TEMPERATURE=$(bashio::config 'temperature')
MAX_TOKENS=$(bashio::config 'max_tokens')

# Application Settings
LOG_LEVEL=$(bashio::config 'log_level')
ENABLE_TERMINAL=$(bashio::config 'enable_terminal')
TERMINAL_PORT=$(bashio::config 'terminal_port')
ENABLE_MONITORING=$(bashio::config 'enable_monitoring')
MONITOR_INTERVAL=$(bashio::config 'monitor_interval')

# Log configuration
bashio::log.blue "Starting Hailo AI Terminal..."
bashio::log.info "Model path: ${MODEL_PATH}"
bashio::log.info "Device ID: ${DEVICE_ID}"
bashio::log.info "AI Backend: ${AI_BACKEND}"
bashio::log.info "AI Model: ${AI_MODEL}"
bashio::log.info "Log level: ${LOG_LEVEL}"
bashio::log.info "Terminal enabled: ${ENABLE_TERMINAL}"
bashio::log.info "Terminal port: ${TERMINAL_PORT}"
bashio::log.info "Monitoring enabled: ${ENABLE_MONITORING}"

# Log API key status (without revealing keys)
if [[ -n "${OPENAI_API_KEY}" ]]; then
    bashio::log.info "OpenAI API key configured"
fi
if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    bashio::log.info "Anthropic API key configured"
fi
if [[ -n "${CUSTOM_API_URL}" ]]; then
    bashio::log.info "Custom API URL configured: ${CUSTOM_API_URL}"
fi

# Create model directory if it doesn't exist
if [[ ! -d "${MODEL_PATH}" ]]; then
    bashio::log.info "Creating model directory: ${MODEL_PATH}"
    mkdir -p "${MODEL_PATH}"
fi

# Check if Hailo device is available
if [[ -e "/dev/hailo0" ]]; then
    bashio::log.info "Hailo device found at /dev/hailo0"
else
    bashio::log.warning "Hailo device not found at /dev/hailo0"
    bashio::log.warning "AI features will use CPU fallback"
fi

# Export environment variables for the application
# Hardware settings
export MODEL_PATH="${MODEL_PATH}"
export DEVICE_ID="${DEVICE_ID}"

# AI Backend settings
export AI_BACKEND="${AI_BACKEND}"
export AI_MODEL="${AI_MODEL}"
export OPENAI_API_KEY="${OPENAI_API_KEY}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}"
export CUSTOM_API_URL="${CUSTOM_API_URL}"

# Performance settings
export MAX_CONTEXT_LENGTH="${MAX_CONTEXT_LENGTH}"
export TEMPERATURE="${TEMPERATURE}"
export MAX_TOKENS="${MAX_TOKENS}"

# Application settings
export LOG_LEVEL="${LOG_LEVEL}"
export ENABLE_TERMINAL="${ENABLE_TERMINAL}"
export TERMINAL_PORT="${TERMINAL_PORT}"
export ENABLE_MONITORING="${ENABLE_MONITORING}"
export MONITOR_INTERVAL="${MONITOR_INTERVAL}"

# Set Python path
export PYTHONPATH="/home/hailo_terminal/src:$PYTHONPATH"

# Start the main application
bashio::log.info "Starting Hailo AI Terminal application..."
cd /home/hailo_terminal/src
exec python3 hailo_terminal.py
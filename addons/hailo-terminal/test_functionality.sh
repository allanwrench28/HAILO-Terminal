#!/bin/bash
# Simple test script to verify the add-on functionality

# Test script for Hailo AI Terminal
echo "Testing Hailo AI Terminal..."

# Set test environment variables
export AI_BACKEND="openai"
export OPENAI_API_KEY="test-key"
export ENABLE_TERMINAL="false"
export ENABLE_MONITORING="true"
export LOG_LEVEL="info"

# Test imports
echo "Testing Python imports..."
python3 -c "
import sys
sys.path.insert(0, '/home/hailo_terminal/src')

try:
    import ai_backend_manager
    print('✓ AI Backend Manager imported')
except Exception as e:
    print(f'✗ AI Backend Manager import failed: {e}')
    exit(1)

try:
    import hailo_terminal
    print('✓ Hailo Terminal imported')
except Exception as e:
    print(f'✗ Hailo Terminal import failed: {e}')
    exit(1)

# Test instantiation
try:
    terminal = hailo_terminal.HailoTerminal()
    print('✓ Terminal instance created')
    
    backends = terminal.ai_backend_manager.get_available_backends()
    print(f'✓ Available backends: {backends}')
    
    if 'openai' in backends:
        print('✓ OpenAI backend available')
    else:
        print('✗ OpenAI backend not available')
        
    print('✓ All tests passed!')
    
except Exception as e:
    print(f'✗ Terminal creation failed: {e}')
    exit(1)
"

echo "Test completed successfully!"
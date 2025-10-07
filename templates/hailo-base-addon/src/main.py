#!/usr/bin/env python3
"""
Hailo AI Add-on Template - Main Application
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Optional

# Configure logging
def setup_logging():
    """Setup logging configuration."""
    log_level = os.getenv('LOG_LEVEL', 'info').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class HailoAIAddon:
    """Main Hailo AI Add-on class."""
    
    def __init__(self):
        """Initialize the add-on."""
        self.model_path = Path(os.getenv('MODEL_PATH', '/share/hailo/models'))
        self.device_id = os.getenv('DEVICE_ID', '0000:03:00.0')
        self.enable_api = os.getenv('ENABLE_API', 'true').lower() == 'true'
        self.api_port = int(os.getenv('API_PORT', '8080'))
        
        logger.info(f"Initialized Hailo AI Add-on")
        logger.info(f"Model path: {self.model_path}")
        logger.info(f"Device ID: {self.device_id}")
        logger.info(f"API enabled: {self.enable_api}")
    
    def check_hailo_device(self) -> bool:
        """Check if Hailo device is available."""
        hailo_device = Path('/dev/hailo0')
        if hailo_device.exists():
            logger.info("Hailo device found at /dev/hailo0")
            return True
        else:
            logger.warning("Hailo device not found at /dev/hailo0")
            return False
    
    def load_models(self) -> list:
        """Load available Hailo models."""
        models = []
        if self.model_path.exists():
            hef_files = list(self.model_path.glob('*.hef'))
            for hef_file in hef_files:
                models.append({
                    'name': hef_file.stem,
                    'path': str(hef_file),
                    'size': hef_file.stat().st_size
                })
                logger.info(f"Found model: {hef_file.name}")
        else:
            logger.warning(f"Model directory not found: {self.model_path}")
        
        return models
    
    def initialize_hailo_runtime(self):
        """Initialize Hailo runtime."""
        try:
            # This is where you would initialize HailoRT
            # import hailo_platform
            # self.hailo_device = hailo_platform.Device()
            logger.info("Hailo runtime initialized (placeholder)")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Hailo runtime: {e}")
            return False
    
    def start_api_server(self):
        """Start API server if enabled."""
        if not self.enable_api:
            logger.info("API server disabled")
            return
        
        try:
            from flask import Flask, jsonify
            
            app = Flask(__name__)
            
            @app.route('/health')
            def health():
                return jsonify({'status': 'healthy', 'device': self.device_id})
            
            @app.route('/models')
            def models():
                available_models = self.load_models()
                return jsonify({'models': available_models})
            
            @app.route('/inference', methods=['POST'])
            def inference():
                # Placeholder for inference endpoint
                return jsonify({'message': 'Inference endpoint placeholder'})
            
            logger.info(f"Starting API server on port {self.api_port}")
            app.run(host='0.0.0.0', port=self.api_port, debug=False)
            
        except ImportError:
            logger.error("Flask not installed. API server disabled.")
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
    
    def run(self):
        """Main run method."""
        logger.info("Starting Hailo AI Add-on...")
        
        # Check device availability
        device_available = self.check_hailo_device()
        
        # Load available models
        models = self.load_models()
        logger.info(f"Loaded {len(models)} models")
        
        # Initialize runtime
        if device_available:
            runtime_ready = self.initialize_hailo_runtime()
            if not runtime_ready:
                logger.error("Failed to initialize Hailo runtime")
                return False
        
        # Start API server (blocking)
        if self.enable_api:
            self.start_api_server()
        else:
            # Keep running without API
            logger.info("Add-on running without API server")
            import time
            try:
                while True:
                    time.sleep(60)
                    logger.debug("Add-on heartbeat")
            except KeyboardInterrupt:
                logger.info("Add-on stopped")
        
        return True

def main():
    """Main entry point."""
    try:
        addon = HailoAIAddon()
        success = addon.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Add-on interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Add-on crashed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
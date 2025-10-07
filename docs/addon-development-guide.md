# Home Assistant Add-on Development Guide

This guide covers the essentials of developing Home Assistant add-ons with focus on Hailo AI integration.

## Add-on Architecture

### Core Components

#### 1. Configuration (`config.yaml`)
The add-on manifest defining metadata, options, and system requirements:

```yaml
# Basic metadata
name: My Hailo Add-on
version: "1.0.0"
slug: my_hailo_addon
description: Custom Hailo AI add-on
url: "https://github.com/user/repo"

# Architecture support
arch:
  - aarch64  # Primary for Hailo hardware
  - amd64    # For development/testing

# System integration
map:
  - "share:rw"     # Access to /share directory
  - "ssl"          # SSL certificates
  - "media:rw"     # Media files

# Hardware access
privileged:
  - SYS_ADMIN      # Required for some Hailo operations
devices:
  - "/dev/hailo0:/dev/hailo0:rwm"
udev: true         # Access to udev for device detection

# User configuration
options:
  model_path: "/share/hailo/models"
  log_level: "info"
  api_port: 8080
```

#### 2. Container (`Dockerfile`)
Multi-stage build optimized for Home Assistant:

```dockerfile
FROM ubuntu:22.04

# Metadata for Home Assistant
LABEL \
    io.hass.name="My Hailo Add-on" \
    io.hass.description="Custom Hailo AI add-on" \
    io.hass.arch="aarch64|amd64" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

# Environment setup
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# System dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential pkg-config \
    libffi-dev libjpeg-dev libpng-dev \
    ffmpeg curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# S6-Overlay for proper process management
ARG S6_OVERLAY_VERSION=3.1.6.2
RUN ARCH=$(dpkg --print-architecture) \
    && curl -L -f -o /tmp/s6-overlay-arch.tar.xz \
        "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${ARCH}.tar.xz" \
    && tar -C / -Jxpf /tmp/s6-overlay-arch.tar.xz \
    && rm -f /tmp/s6-overlay-arch.tar.xz

RUN curl -L -f -o /tmp/s6-overlay-noarch.tar.xz \
        "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" \
    && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz \
    && rm -f /tmp/s6-overlay-noarch.tar.xz

# Application setup
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

# Hailo packages (architecture-specific)
RUN ARCH=$(dpkg --print-architecture) \
    && if [ "${ARCH}" = "aarch64" ]; then \
        dpkg --unpack hailo_packages/*_arm64.deb || true; \
        pip3 install hailo_packages/*-linux_aarch64.whl; \
    fi

ENTRYPOINT ["/init"]
CMD ["/run.sh"]
```

#### 3. Startup Script (`run.sh`)
Bashio-integrated startup with configuration handling:

```bash
#!/usr/bin/with-contenv bashio

# Configuration extraction
MODEL_PATH=$(bashio::config 'model_path')
LOG_LEVEL=$(bashio::config 'log_level')
API_PORT=$(bashio::config 'api_port')

# Logging
bashio::log.info "Starting My Hailo Add-on..."
bashio::log.info "Model path: ${MODEL_PATH}"
bashio::log.info "API port: ${API_PORT}"

# Validation
if [[ ! -d "${MODEL_PATH}" ]]; then
    bashio::log.warning "Model directory not found, creating: ${MODEL_PATH}"
    mkdir -p "${MODEL_PATH}"
fi

# Environment export
export MODEL_PATH LOG_LEVEL API_PORT

# Start application
exec python3 src/main.py
```

## Integration Patterns

### Configuration Management
```python
import os
import yaml
from pathlib import Path

class AddonConfig:
    """Home Assistant add-on configuration manager."""
    
    def __init__(self, config_path="/data/options.json"):
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self):
        """Load configuration from Home Assistant."""
        if self.config_path.exists():
            import json
            with open(self.config_path) as f:
                return json.load(f)
        else:
            # Fallback to environment variables
            return {
                'model_path': os.getenv('MODEL_PATH', '/share/hailo/models'),
                'log_level': os.getenv('LOG_LEVEL', 'info'),
                'api_port': int(os.getenv('API_PORT', '8080'))
            }
    
    def get(self, key, default=None):
        """Get configuration value."""
        return self._config.get(key, default)
    
    @property
    def model_path(self):
        return Path(self.get('model_path'))
    
    @property
    def log_level(self):
        return self.get('log_level', 'info').upper()
    
    @property
    def api_port(self):
        return int(self.get('api_port', 8080))
```

### Service Discovery
```python
import requests
import json

class HomeAssistantAPI:
    """Home Assistant API integration."""
    
    def __init__(self):
        self.supervisor_token = os.getenv('SUPERVISOR_TOKEN')
        self.ha_token = os.getenv('HOME_ASSISTANT_TOKEN')
        self.base_url = "http://supervisor"
    
    def get_addon_info(self):
        """Get current add-on information."""
        headers = {"Authorization": f"Bearer {self.supervisor_token}"}
        response = requests.get(f"{self.base_url}/addons/self/info", headers=headers)
        return response.json()
    
    def send_persistent_notification(self, message, title="Hailo Add-on"):
        """Send notification to Home Assistant."""
        if not self.ha_token:
            return False
        
        headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "message": message,
            "title": title,
            "notification_id": "hailo_addon_notification"
        }
        
        response = requests.post(
            "http://supervisor/core/api/services/persistent_notification/create",
            headers=headers,
            json=data
        )
        
        return response.status_code == 200
    
    def register_sensor(self, entity_id, state, attributes=None):
        """Register a sensor entity."""
        if not self.ha_token:
            return False
        
        headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "state": state,
            "attributes": attributes or {}
        }
        
        response = requests.post(
            f"http://supervisor/core/api/states/{entity_id}",
            headers=headers,
            json=data
        )
        
        return response.status_code in [200, 201]
```

### Health Monitoring
```python
from flask import Flask, jsonify
import psutil
import threading
import time

class HealthMonitor:
    """Add-on health monitoring system."""
    
    def __init__(self, hailo_manager, ha_api):
        self.hailo_manager = hailo_manager
        self.ha_api = ha_api
        self.stats = {
            'startup_time': time.time(),
            'inference_count': 0,
            'error_count': 0,
            'last_inference': None
        }
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while True:
            try:
                # Update system stats
                self._update_system_stats()
                
                # Check Hailo device health
                device_healthy = self._check_device_health()
                
                # Update Home Assistant sensors
                self._update_ha_sensors(device_healthy)
                
                time.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                time.sleep(60)  # Longer delay on error
    
    def _update_system_stats(self):
        """Update system resource statistics."""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        self.stats.update({
            'memory_percent': memory.percent,
            'memory_available_mb': memory.available // (1024 * 1024),
            'cpu_percent': cpu,
            'uptime_hours': (time.time() - self.stats['startup_time']) / 3600
        })
    
    def _check_device_health(self):
        """Check Hailo device health."""
        try:
            return self.hailo_manager.is_device_available()
        except Exception as e:
            logger.error(f"Device health check failed: {e}")
            return False
    
    def _update_ha_sensors(self, device_healthy):
        """Update Home Assistant sensor entities."""
        # Device status sensor
        self.ha_api.register_sensor(
            "sensor.hailo_addon_device_status",
            "online" if device_healthy else "offline",
            {
                "device_class": "connectivity",
                "friendly_name": "Hailo Device Status"
            }
        )
        
        # Performance sensors
        self.ha_api.register_sensor(
            "sensor.hailo_addon_memory_usage",
            self.stats['memory_percent'],
            {
                "unit_of_measurement": "%",
                "device_class": "memory",
                "friendly_name": "Hailo Add-on Memory Usage"
            }
        )
        
        self.ha_api.register_sensor(
            "sensor.hailo_addon_inference_count",
            self.stats['inference_count'],
            {
                "friendly_name": "Hailo Inference Count",
                "icon": "mdi:brain"
            }
        )
    
    def record_inference(self, success=True):
        """Record inference attempt."""
        self.stats['inference_count'] += 1
        self.stats['last_inference'] = time.time()
        
        if not success:
            self.stats['error_count'] += 1
    
    def get_health_status(self):
        """Get comprehensive health status."""
        device_healthy = self._check_device_health()
        
        return {
            'healthy': device_healthy and (self.stats['error_count'] / max(self.stats['inference_count'], 1)) < 0.1,
            'device_status': 'online' if device_healthy else 'offline',
            'stats': self.stats.copy(),
            'system': {
                'memory_percent': self.stats['memory_percent'],
                'cpu_percent': self.stats['cpu_percent'],
                'uptime_hours': round(self.stats['uptime_hours'], 2)
            }
        }
```

## Advanced Patterns

### WebSocket Integration
```python
import asyncio
import websockets
import json

class WebSocketServer:
    """WebSocket server for real-time communication."""
    
    def __init__(self, port=8765, hailo_manager=None):
        self.port = port
        self.hailo_manager = hailo_manager
        self.clients = set()
    
    async def register_client(self, websocket, path):
        """Register new WebSocket client."""
        self.clients.add(websocket)
        logger.info(f"Client connected: {websocket.remote_address}")
        
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            logger.info(f"Client disconnected: {websocket.remote_address}")
    
    async def broadcast_message(self, message):
        """Broadcast message to all connected clients."""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )
    
    async def handle_inference_result(self, model_name, result):
        """Handle and broadcast inference results."""
        message = {
            'type': 'inference_result',
            'model': model_name,
            'timestamp': time.time(),
            'result': result
        }
        
        await self.broadcast_message(message)
    
    def start_server(self):
        """Start WebSocket server."""
        return websockets.serve(
            self.register_client,
            "0.0.0.0",
            self.port
        )
```

### Configuration Schema Validation
```python
from jsonschema import validate, ValidationError

class ConfigValidator:
    """Configuration validation using JSON Schema."""
    
    SCHEMA = {
        "type": "object",
        "properties": {
            "model_path": {
                "type": "string",
                "pattern": "^/.*"  # Must be absolute path
            },
            "device_id": {
                "type": "string",
                "pattern": "^[0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\\.[0-9a-fA-F]$"
            },
            "log_level": {
                "type": "string",
                "enum": ["debug", "info", "warning", "error"]
            },
            "api_port": {
                "type": "integer",
                "minimum": 1024,
                "maximum": 65535
            },
            "max_concurrent_inferences": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10
            }
        },
        "required": ["model_path", "device_id"],
        "additionalProperties": True
    }
    
    @classmethod
    def validate_config(cls, config):
        """Validate configuration against schema."""
        try:
            validate(instance=config, schema=cls.SCHEMA)
            return True, None
        except ValidationError as e:
            return False, str(e)
```

## Testing Strategies

### Unit Testing
```python
import unittest
from unittest.mock import Mock, patch
import tempfile
import shutil

class TestHailoAddon(unittest.TestCase):
    """Unit tests for Hailo add-on components."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {
            'model_path': self.temp_dir,
            'log_level': 'debug',
            'api_port': 8080
        }
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    @patch('hailo_platform.Device')
    def test_hailo_manager_initialization(self, mock_device):
        """Test Hailo manager initialization."""
        from src.hailo_manager import HailoManager
        
        manager = HailoManager(device_id="test:device")
        mock_device.assert_called_once_with("test:device")
        self.assertIsNotNone(manager.device)
    
    def test_config_validation(self):
        """Test configuration validation."""
        from src.config import ConfigValidator
        
        valid, error = ConfigValidator.validate_config(self.config)
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test invalid config
        invalid_config = {'model_path': 'relative/path'}  # Should be absolute
        valid, error = ConfigValidator.validate_config(invalid_config)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_health_check(self):
        """Test health check functionality."""
        from src.health import HealthMonitor
        
        mock_hailo_manager = Mock()
        mock_hailo_manager.is_device_available.return_value = True
        
        mock_ha_api = Mock()
        
        health_monitor = HealthMonitor(mock_hailo_manager, mock_ha_api)
        status = health_monitor.get_health_status()
        
        self.assertIn('healthy', status)
        self.assertIn('device_status', status)
        self.assertEqual(status['device_status'], 'online')
```

### Integration Testing
```python
import docker
import requests
import time

class TestAddonIntegration:
    """Integration tests for full add-on functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.client = docker.from_env()
        self.container = None
    
    def teardown_method(self):
        """Clean up test environment."""
        if self.container:
            try:
                self.container.stop()
                self.container.remove()
            except:
                pass
    
    def test_addon_startup(self):
        """Test add-on container startup."""
        # Build test image
        image, _ = self.client.images.build(
            path=".",
            tag="test-hailo-addon:latest"
        )
        
        # Run container
        self.container = self.client.containers.run(
            image.id,
            detach=True,
            ports={'8080/tcp': 8080},
            environment={
                'MODEL_PATH': '/tmp/models',
                'LOG_LEVEL': 'debug'
            }
        )
        
        # Wait for startup
        time.sleep(10)
        
        # Test health endpoint
        response = requests.get('http://localhost:8080/health', timeout=30)
        assert response.status_code == 200
        
        health_data = response.json()
        assert 'healthy' in health_data
    
    def test_model_loading(self):
        """Test model loading functionality."""
        # This would require actual HEF files for full testing
        # Mock or use test models
        pass
```

This development guide provides the foundation for building robust, well-integrated Home Assistant add-ons with Hailo AI capabilities!
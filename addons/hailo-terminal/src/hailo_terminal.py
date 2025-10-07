#!/usr/bin/env python3
"""
Hailo AI Terminal - Intelligent Home Assistant Assistant

This application provides:
1. Real-time resource monitoring of Home Assistant
2. AI-powered assistance for configurations and automations
3. Performance optimization recommendations
4. Interactive terminal interface
"""

import os
import sys
import logging
import asyncio
import psutil
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import threading
import time
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit

        @self.app.route('/api/entities/discovery')
        def get_entity_discovery():
            \"\"\"Get comprehensive entity discovery information.\"\"\"
            try:
                if self.ha_client:
                    import asyncio
                    discovery_data = asyncio.run(self.ha_client.get_discovery_summary())
                    
                    return jsonify({
                        'success': True,
                        'discovery': discovery_data
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Home Assistant client not available'
                    }), 503
                    
            except Exception as e:
                logger.error(f\"Error getting entity discovery: {e}\")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/entities/by-domain/<domain>')
        def get_entities_by_domain(domain):
            \"\"\"Get entities filtered by domain.\"\"\"
            try:
                if self.ha_client:
                    import asyncio
                    entities = asyncio.run(self.ha_client.get_entities_by_domain(domain))
                    
                    return jsonify({
                        'success': True,
                        'domain': domain,
                        'entities': entities,
                        'count': len(entities)
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Home Assistant client not available'
                    }), 503
                    
            except Exception as e:
                logger.error(f\"Error getting entities for domain {domain}: {e}\")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/automation/relevant-entities/<template_id>')
        def get_relevant_entities(template_id):
            \"\"\"Get entities relevant to a specific automation template.\"\"\"
            try:
                import asyncio
                relevant_entities = asyncio.run(
                    self.automation_manager.get_relevant_entities_for_automation(template_id)
                )
                
                return jsonify({
                    'success': True,
                    'template_id': template_id,
                    'relevant_entities': relevant_entities
                })
                
            except Exception as e:
                logger.error(f\"Error getting relevant entities for {template_id}: {e}\")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    late
from flask_socketio import SocketIO, emit

# Import our AI backend manager
from ai_backend_manager import AIBackendManager


def setup_logging() -> logging.Logger:
    """Setup logging configuration."""
    log_level = os.getenv('LOG_LEVEL', 'info').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


logger = setup_logging()


class HomeAssistantAPI:
    """Home Assistant API client for supervisor and core integration."""
    
    def __init__(self):
        self.supervisor_token = os.getenv('SUPERVISOR_TOKEN', '')
        self.ha_token = os.getenv('HA_TOKEN', '')
        self.supervisor_url = 'http://supervisor'
        self.ha_url = 'http://homeassistant:8123'
        self.session = requests.Session()
        
        # Set up authentication headers
        if self.supervisor_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.supervisor_token}',
                'Content-Type': 'application/json'
            })
    
    def get_supervisor_stats(self) -> Optional[Dict[str, Any]]:
        """Get Home Assistant Supervisor statistics."""
        try:
            response = self.session.get(
                f'{self.supervisor_url}/supervisor/stats',
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.debug(f"Could not fetch supervisor stats: {e}")
        return None
    
    def get_addon_stats(self) -> Optional[Dict[str, Any]]:
        """Get statistics for all add-ons."""
        try:
            response = self.session.get(
                f'{self.supervisor_url}/addons',
                timeout=10
            )
            if response.status_code == 200:
                addons_data = response.json()
                addon_stats = {}
                
                for addon in addons_data.get('data', {}).get('addons', []):
                    addon_slug = addon.get('slug', 'unknown')
                    addon_stats[addon_slug] = {
                        'name': addon.get('name', 'Unknown'),
                        'state': addon.get('state', 'unknown'),
                        'version': addon.get('version', 'unknown'),
                        'cpu_percent': addon.get('cpu_percent', 0),
                        'memory_usage': addon.get('memory_usage', 0),
                        'memory_limit': addon.get('memory_limit', 0)
                    }
                
                return addon_stats
        except Exception as e:
            logger.debug(f"Could not fetch addon stats: {e}")
        return None
    
    def get_ha_info(self) -> Optional[Dict[str, Any]]:
        """Get Home Assistant core information."""
        try:
            ha_session = requests.Session()
            if self.ha_token:
                ha_session.headers.update({
                    'Authorization': f'Bearer {self.ha_token}',
                    'Content-Type': 'application/json'
                })
            
            response = ha_session.get(
                f'{self.ha_url}/api/',
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.debug(f"Could not fetch HA info: {e}")
        return None


class ResourceMonitor:
    """Monitor system and Home Assistant resource usage."""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.ha_api = HomeAssistantAPI()
        self.data = {
            'cpu_percent': 0,
            'memory_usage': 0,
            'memory_total': 0,
            'disk_usage': 0,
            'disk_total': 0,
            'network_io': {'bytes_sent': 0, 'bytes_recv': 0},
            'addons': {},
            'ha_info': {},
            'supervisor_stats': {},
            'last_update': None,
            'hailo_device': self._check_hailo_device()
        }
    
    def _check_hailo_device(self) -> Dict[str, Any]:
        """Check Hailo device status."""
        hailo_info = {
            'available': False,
            'device_path': '/dev/hailo0',
            'temperature': None,
            'utilization': None
        }
        
        try:
            import os
            if os.path.exists('/dev/hailo0'):
                hailo_info['available'] = True
                logger.info("Hailo device detected")
                
                # Try to get device temperature if available
                temp_path = '/sys/class/thermal/thermal_zone0/temp'
                if os.path.exists(temp_path):
                    with open(temp_path, 'r') as f:
                        temp_raw = int(f.read().strip())
                        hailo_info['temperature'] = temp_raw / 1000.0
        except Exception as e:
            logger.debug(f"Error checking Hailo device: {e}")
        
        return hailo_info
    
    def start_monitoring(self, interval: int = 5):
        """Start resource monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, args=(interval,)
        )
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Resource monitoring started")
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Resource monitoring stopped")
    
    def _monitor_loop(self, interval: int):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._collect_system_metrics()
                self._collect_ha_metrics()
                self._update_hailo_metrics()
                self.data['last_update'] = datetime.now().isoformat()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self):
        """Collect system resource metrics."""
        try:
            # CPU usage
            self.data['cpu_percent'] = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.data['memory_usage'] = memory.percent
            self.data['memory_total'] = memory.total
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.data['disk_usage'] = disk.percent
            self.data['disk_total'] = disk.total
            
            # Network I/O
            net_io = psutil.net_io_counters()
            self.data['network_io'] = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv
            }
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def _collect_ha_metrics(self):
        """Collect Home Assistant specific metrics."""
        try:
            # Get supervisor statistics
            supervisor_stats = self.ha_api.get_supervisor_stats()
            if supervisor_stats:
                self.data['supervisor_stats'] = supervisor_stats
            
            # Get add-on statistics
            addon_stats = self.ha_api.get_addon_stats()
            if addon_stats:
                self.data['addons'] = addon_stats
            else:
                # Fallback to simulated data if API unavailable
                self.data['addons'] = {
                    'hailo_ai_terminal': {
                        'name': 'Hailo AI Terminal',
                        'state': 'started',
                        'cpu_percent': psutil.Process().cpu_percent(),
                        'memory_usage': psutil.Process().memory_info().rss,
                        'memory_limit': 1024 * 1024 * 1024  # 1GB
                    }
                }
            
            # Get Home Assistant core info
            ha_info = self.ha_api.get_ha_info()
            if ha_info:
                self.data['ha_info'] = ha_info
                
        except Exception as e:
            logger.error(f"Error collecting HA metrics: {e}")
    
    def _update_hailo_metrics(self):
        """Update Hailo device specific metrics."""
        try:
            if self.data['hailo_device']['available']:
                # Update temperature if available
                temp_path = '/sys/class/thermal/thermal_zone0/temp'
                if os.path.exists(temp_path):
                    with open(temp_path, 'r') as f:
                        temp_raw = int(f.read().strip())
                        self.data['hailo_device']['temperature'] = temp_raw / 1000.0
                
                # Try to get utilization from Hailo runtime if available
                try:
                    # This would require Hailo runtime to be properly integrated
                    pass
                except:
                    pass
                    
        except Exception as e:
            logger.debug(f"Error updating Hailo metrics: {e}")
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get current monitoring data."""
        return self.data.copy()


# Removed old HailoAIEngine class - now using AIBackendManager


class HailoTerminal:
    """Main Hailo AI Terminal application."""
    
    def __init__(self, config=None):
        """Initialize the terminal application.
        
        Args:
            config: Optional configuration dictionary. If None, loads from env.
        """
        # Load configuration from environment or use provided config
        self.config = config if config is not None else self._load_config()
        
        # Initialize components
        self.resource_monitor = ResourceMonitor()
        self.ai_backend_manager = AIBackendManager(self.config)
        
        # Initialize Home Assistant client if configured
        self.ha_client = None
        if self.config.get('ha_url') and self.config.get('ha_token'):
            from ha_client import HomeAssistantClient
            self.ha_client = HomeAssistantClient(
                self.config['ha_url'],
                self.config['ha_token']
            )
        
        # Initialize automation manager
        from automation_manager import AutomationManager
        self.automation_manager = AutomationManager(self.ha_client)
        
        # Flask app for web interface
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.app = Flask(__name__, template_folder=template_dir)
        self.app.config['SECRET_KEY'] = 'hailo-terminal-secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        self._setup_routes()
        self._setup_socket_handlers()
        
        logger.info("Hailo AI Terminal initialized")
        logger.info(f"AI Backend: {self.config.get('ai_backend', 'hailo')}")
        logger.info(f"AI Model: {self.config.get('ai_model', 'unknown')}")
        logger.info(
            f"Terminal enabled: {self.config.get('enable_terminal', True)}"
        )
        logger.info(
            f"Monitoring enabled: {self.config.get('enable_monitoring', True)}"
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            # Hardware settings
            'model_path': os.getenv('MODEL_PATH', '/share/hailo/models'),
            'device_id': os.getenv('DEVICE_ID', '0000:03:00.0'),
            
            # AI Backend settings
            'ai_backend': os.getenv('AI_BACKEND', 'hailo'),
            'ai_model': os.getenv('AI_MODEL', 'llama2-7b-chat'),
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
            'custom_api_url': os.getenv('CUSTOM_API_URL', ''),
            
            # Performance settings
            'max_context_length': int(os.getenv('MAX_CONTEXT_LENGTH', '4096')),
            'temperature': float(os.getenv('TEMPERATURE', '0.7')),
            'max_tokens': int(os.getenv('MAX_TOKENS', '512')),
            
            # Application settings
            'enable_terminal': (
                os.getenv('ENABLE_TERMINAL', 'true').lower() == 'true'
            ),
            'terminal_port': int(os.getenv('TERMINAL_PORT', '8080')),
            'enable_monitoring': (
                os.getenv('ENABLE_MONITORING', 'true').lower() == 'true'
            ),
            'monitor_interval': int(os.getenv('MONITOR_INTERVAL', '5')),
        }
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/health')
        def health():
            backend_status = self.ai_backend_manager.get_backend_status()
            return jsonify({
                'status': 'healthy',
                'ai_backends': backend_status,
                'monitoring': self.resource_monitor.monitoring,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/resources')
        def resources():
            # Get basic resource data
            resource_data = self.resource_monitor.get_current_data()
            
            # Add HA-specific data if client is available
            if self.ha_client:
                try:
                    from ha_client import get_system_resources_sync
                    ha_resources = get_system_resources_sync(self.ha_client)
                    resource_data.update(ha_resources)
                except Exception as e:
                    logger.error(f"Failed to get HA resources: {e}")
                    resource_data.update(self.ha_client.get_mock_system_info())
            
            return jsonify(resource_data)
        
        @self.app.route('/api/backends')
        def backends():
            """Get available AI backends."""
            return jsonify({
                'available': self.ai_backend_manager.get_available_backends(),
                'current': self.ai_backend_manager.current_backend,
                'status': self.ai_backend_manager.get_backend_status()
            })
        
        @self.app.route('/api/switch_backend', methods=['POST'])
        def switch_backend():
            """Switch AI backend."""
            data = request.get_json()
            backend_name = data.get('backend', '')
            
            if not backend_name:
                return jsonify({'error': 'No backend specified'}), 400
            
            success = self.ai_backend_manager.switch_backend(backend_name)
            if success:
                return jsonify({
                    'success': True,
                    'current_backend': backend_name
                })
            else:
                return jsonify({
                    'error': f'Backend {backend_name} not available'
                }), 400

        @self.app.route('/api/automation/recommendations', methods=['POST'])
        def get_automation_recommendations():
            """Get automation recommendations based on user request."""
            data = request.get_json()
            user_request = data.get('request', '')
            
            if not user_request:
                return jsonify({'error': 'No request provided'}), 400
            
            # Get available entities if HA client is available
            available_entities = []
            if self.ha_client:
                try:
                    # This would be implemented to get entity list
                    available_entities = []  # Placeholder
                except Exception as e:
                    logger.warning(f"Could not get entities: {e}")
            
            recommendations = self.automation_manager.get_automation_recommendations(
                user_request, available_entities
            )
            
            return jsonify({
                'recommendations': recommendations,
                'count': len(recommendations)
            })

        @self.app.route('/api/automation/generate', methods=['POST'])
        def generate_automation():
            """Generate automation YAML from template and parameters."""
            data = request.get_json()
            template_id = data.get('template_id', '')
            parameters = data.get('parameters', {})
            
            if not template_id:
                return jsonify({'error': 'No template ID provided'}), 400
            
            try:
                yaml_content, automation_dict = self.automation_manager.generate_automation_yaml(
                    template_id, parameters
                )
                
                return jsonify({
                    'success': True,
                    'yaml': yaml_content,
                    'automation': automation_dict
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 400

        @self.app.route('/api/automation/validate', methods=['POST'])
        def validate_automation():
            """Validate automation configuration."""
            data = request.get_json()
            automation_dict = data.get('automation', {})
            
            if not automation_dict:
                return jsonify({'error': 'No automation provided'}), 400
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                is_valid, errors = loop.run_until_complete(
                    self.automation_manager.validate_automation(automation_dict)
                )
                loop.close()
                
                return jsonify({
                    'valid': is_valid,
                    'errors': errors
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/automation/test', methods=['POST'])
        def test_automation():
            """Test automation configuration."""
            data = request.get_json()
            automation_dict = data.get('automation', {})
            
            if not automation_dict:
                return jsonify({'error': 'No automation provided'}), 400
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success, message = loop.run_until_complete(
                    self.automation_manager.test_automation(automation_dict)
                )
                loop.close()
                
                return jsonify({
                    'success': success,
                    'message': message
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/automation/save', methods=['POST'])
        def save_automation():
            """Save automation to Home Assistant."""
            data = request.get_json()
            automation_dict = data.get('automation', {})
            test_first = data.get('test_first', True)
            
            if not automation_dict:
                return jsonify({'error': 'No automation provided'}), 400
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success, message = loop.run_until_complete(
                    self.automation_manager.save_automation(automation_dict, test_first)
                )
                loop.close()
                
                return jsonify({
                    'success': success,
                    'message': message
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/automation/suggestions')
        def get_automation_suggestions():
            """Get automation suggestions for autocomplete."""
            query = request.args.get('q', '')
            suggestions = self.automation_manager.get_automation_suggestions(query)
            
            return jsonify({
                'suggestions': suggestions
            })
    
    def _setup_socket_handlers(self):
        """Setup WebSocket handlers."""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            # Send initial status
            backend_status = self.ai_backend_manager.get_backend_status()
            emit('status', {
                'message': 'Connected to Hailo AI Terminal',
                'backends': backend_status,
                'current_backend': self.ai_backend_manager.current_backend
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")
        
        @self.socketio.on('ai_query')
        def handle_ai_query(data):
            """Handle AI query via WebSocket with automation intelligence."""
            query = data.get('query', '')
            logger.info(f"Received AI query: {query}")
            
            if not query.strip():
                emit('ai_response', {
                    'error': 'Empty query received',
                    'timestamp': datetime.now().isoformat()
                })
                return
            
            # Process query asynchronously in background
            def process_query_async():
                try:
                    # Create event loop for this thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Check if this is an automation-related query
                    automation_keywords = [
                        'automation', 'automate', 'trigger', 'schedule', 
                        'turn on', 'turn off', 'when', 'if', 'notify',
                        'motion', 'sensor', 'light', 'door', 'temperature'
                    ]
                    
                    query_lower = query.lower()
                    is_automation_query = any(keyword in query_lower 
                                            for keyword in automation_keywords)
                    
                    # Generate AI response
                    response = loop.run_until_complete(
                        self.ai_backend_manager.generate_response(query)
                    )
                    
                    # If it's an automation query, also provide recommendations
                    automation_recommendations = []
                    if is_automation_query:
                        try:
                            recommendations = self.automation_manager.get_automation_recommendations(query)
                            automation_recommendations = recommendations[:3]  # Top 3
                        except Exception as e:
                            logger.warning(f"Could not get automation recommendations: {e}")
                    
                    # Enhanced response with automation features
                    enhanced_response = response.content
                    
                    if automation_recommendations:
                        enhanced_response += "\n\n🤖 **Automation Recommendations:**\n"
                        for i, rec in enumerate(automation_recommendations, 1):
                            enhanced_response += f"\n**{i}. {rec['name']}** ({rec['complexity']})\n"
                            enhanced_response += f"   {rec['description']}\n"
                            if rec.get('required_entities'):
                                entities = ', '.join(rec['required_entities'])
                                enhanced_response += f"   *Requires: {entities}*\n"
                        
                        enhanced_response += "\n💡 *Click 'Create Automation' below to build any of these!*"
                    
                    # Send response back
                    self.socketio.emit('ai_response', {
                        'query': query,
                        'response': enhanced_response,
                        'backend': response.backend,
                        'model': response.model,
                        'usage': response.usage,
                        'error': response.error,
                        'automation_suggestions': automation_recommendations,
                        'is_automation_query': is_automation_query,
                        'timestamp': datetime.now().isoformat()
                    }, room=request.sid)
                    
                    loop.close()
                    
                except Exception as e:
                    logger.error(f"Error processing AI query: {e}")
                    self.socketio.emit('ai_response', {
                        'query': query,
                        'error': f'Processing error: {str(e)}',
                        'timestamp': datetime.now().isoformat()
                    }, room=request.sid)
            
            # Start processing in background thread
            thread = threading.Thread(target=process_query_async)
            thread.daemon = True
            thread.start()
    
    def start_background_services(self):
        """Start background services."""
        # Log AI backend status
        available_backends = self.ai_backend_manager.get_available_backends()
        if available_backends:
            logger.info(f"Available AI backends: {', '.join(available_backends)}")
        else:
            logger.warning("No AI backends available!")
        
        # Start resource monitoring
        if self.config.get('enable_monitoring', True):
            self.resource_monitor.start_monitoring(
                self.config.get('monitor_interval', 5)
            )
        
        # Start real-time updates via WebSocket
        def send_periodic_updates():
            while True:
                try:
                    if self.config.get('enable_monitoring', True):
                        data = self.resource_monitor.get_current_data()
                        self.socketio.emit('resource_update', data, broadcast=True)
                    time.sleep(self.config.get('monitor_interval', 5))
                except Exception as e:
                    logger.error(f"Error in periodic updates: {e}")
                    time.sleep(10)  # Wait longer on error
        
        update_thread = threading.Thread(target=send_periodic_updates)
        update_thread.daemon = True
        update_thread.start()
    
    def create_app(self):
        """Return the Flask app instance for testing."""
        return self.app
    
    def run(self):
        """Main run method."""
        logger.info("Starting Hailo AI Terminal...")
        
        # Start background services
        self.start_background_services()
        
        if self.config.get('enable_terminal', True):
            port = self.config.get('terminal_port', 8080)
            logger.info(f"Starting web interface on port {port}")
            self.socketio.run(
                self.app,
                host='0.0.0.0',
                port=port,
                debug=False,
                allow_unsafe_werkzeug=True
            )
        else:
            logger.info("Terminal disabled, running background services only")
            try:
                while True:
                    time.sleep(60)
                    logger.debug("Terminal heartbeat")
            except KeyboardInterrupt:
                logger.info("Terminal stopped")
        
        return True


def main():
    """Main entry point."""
    try:
        terminal = HailoTerminal()
        success = terminal.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Terminal interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Terminal crashed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
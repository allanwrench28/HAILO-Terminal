"""
Home Assistant API Client for Hailo Terminal Add-on.

This module provides a client for interacting with the Home Assistant API
to retrieve system information, entities, and states.
"""

import logging
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class HomeAssistantClient:
    """Client for Home Assistant API integration."""
    
    def __init__(self, ha_url: str, ha_token: str):
        """Initialize the Home Assistant client.
        
        Args:
            ha_url: Home Assistant URL (e.g., http://192.168.0.143:8123)
            ha_token: Long-lived access token for authentication
        """
        self.ha_url = ha_url.rstrip('/')
        self.ha_token = ha_token
        self.headers = {
            'Authorization': f'Bearer {ha_token}',
            'Content-Type': 'application/json'
        }
        self._session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=self.headers
            )
        return self._session
    
    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def test_connection(self) -> bool:
        """Test connection to Home Assistant."""
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/') as response:
                if response.status == 200:
                    data = await response.json()
                    message = data.get('message', 'API available')
                    logger.info(f"Connected to Home Assistant: {message}")
                    return True
                else:
                    logger.error(f"HA connection failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Failed to connect to Home Assistant: {e}")
            return False
    
    async def get_config(self) -> Optional[Dict[str, Any]]:
        """Get Home Assistant configuration."""
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/config') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get HA config: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error getting HA config: {e}")
            return None
    
    async def get_states(self) -> List[Dict[str, Any]]:
        """Get all entity states from Home Assistant."""
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/states') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get HA states: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting HA states: {e}")
            return []
    
    async def get_entity_state(self, entity_id: str
                               ) -> Optional[Dict[str, Any]]:
        """Get state of a specific entity.
        
        Args:
            entity_id: Entity ID (e.g., 'sensor.cpu_percent')
            
        Returns:
            Entity state dictionary or None if not found
        """
        try:
            session = await self._get_session()
            url = f'{self.ha_url}/api/states/{entity_id}'
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logger.warning(f"Entity not found: {entity_id}")
                    return None
                else:
                    logger.error(
                        f"Failed to get entity {entity_id}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error getting entity {entity_id}: {e}")
            return None
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information from Home Assistant."""
        try:
            # Get basic system info
            system_info = {}
            
            # Get HA config for version info
            config = await self.get_config()
            if config:
                system_info.update({
                    'ha_version': config.get('version', 'unknown'),
                    'location_name': config.get('location_name', 'Home'),
                    'time_zone': config.get('time_zone', 'UTC'),
                    'unit_system': config.get('unit_system', {}),
                })
            
            # Get system sensors if available
            states = await self.get_states()
            system_sensors = {}
            
            for state in states:
                entity_id = state.get('entity_id', '')
                
                # Look for common system sensors
                if any(sensor in entity_id for sensor in [
                    'sensor.processor_use',
                    'sensor.cpu_percent',
                    'sensor.memory_use_percent',
                    'sensor.disk_use_percent',
                    'sensor.load_1m',
                    'sensor.load_5m',
                    'sensor.load_15m'
                ]):
                    try:
                        value = float(state.get('state', 0))
                        system_sensors[entity_id] = {
                            'value': value,
                            'unit': state.get('attributes', {}).get(
                                'unit_of_measurement', ''),
                            'friendly_name': state.get('attributes', {}).get(
                                'friendly_name', entity_id)
                        }
                    except (ValueError, TypeError):
                        # Skip sensors with non-numeric values
                        continue
            
            system_info['sensors'] = system_sensors
            return system_info
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    async def create_automation(self, automation_config: Dict[str, Any]) -> bool:
        """Create a new automation in Home Assistant.
        
        Args:
            automation_config: Automation configuration dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.session:
                await self.connect()
            
            if self.session:
                url = f"{self.ha_url}/api/config/automation/config"
                headers = {
                    'Authorization': f'Bearer {self.ha_token}',
                    'Content-Type': 'application/json'
                }
                
                async with self.session.post(url, json=automation_config,
                                           headers=headers) as response:
                    if response.status == 200:
                        logger.info(f"Created automation: {automation_config.get('alias', 'Unknown')}")
                        return True
                    else:
                        logger.error(f"Failed to create automation: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error creating automation: {e}")
            return False
    
    async def delete_automation(self, automation_id: str) -> bool:
        """Delete an automation from Home Assistant.
        
        Args:
            automation_id: ID of the automation to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.session:
                await self.connect()
            
            if self.session:
                url = f"{self.ha_url}/api/config/automation/config/{automation_id}"
                headers = {
                    'Authorization': f'Bearer {self.ha_token}',
                    'Content-Type': 'application/json'
                }
                
                async with self.session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        logger.info(f"Deleted automation: {automation_id}")
                        return True
                    else:
                        logger.error(f"Failed to delete automation: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error deleting automation: {e}")
            return False
    
    async def list_automations(self) -> List[Dict[str, Any]]:
        """List all automations in Home Assistant.
        
        Returns:
            List of automation configurations
        """
        try:
            if not self.session:
                await self.connect()
            
            if self.session:
                url = f"{self.ha_url}/api/config/automation/config"
                headers = {
                    'Authorization': f'Bearer {self.ha_token}'
                }
                
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data if isinstance(data, list) else []
                    else:
                        logger.error(f"Failed to list automations: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error listing automations: {e}")
            return []

    async def call_service(self, domain: str, service: str,
                           service_data: Optional[Dict[str, Any]] = None,
                           target: Optional[Dict[str, Any]] = None) -> bool:
        """Call a Home Assistant service.
        
        Args:
            domain: Service domain (e.g., 'light', 'switch')
            service: Service name (e.g., 'turn_on', 'turn_off')
            service_data: Optional service data
            target: Optional target specification
            
        Returns:
            True if service call was successful
        """
        try:
            session = await self._get_session()
            url = f'{self.ha_url}/api/services/{domain}/{service}'
            
            payload = {}
            if service_data:
                payload.update(service_data)
            if target:
                payload['target'] = target
            
            async with session.post(url, json=payload) as response:
                if response.status in [200, 201]:
                    logger.info(f"Service call successful: {domain}.{service}")
                    return True
                else:
                    logger.error(f"Service call failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error calling service {domain}.{service}: {e}")
            return False
    
    async def get_automations(self) -> List[Dict[str, Any]]:
        """Get list of automations."""
        try:
            states = await self.get_states()
            automations = [
                state for state in states 
                if state.get('entity_id', '').startswith('automation.')
            ]
            return automations
        except Exception as e:
            logger.error(f"Error getting automations: {e}")
            return []
    
    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get list of devices."""
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/config/device_registry') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get devices: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return []

    async def get_all_entities(self) -> Dict[str, List[Dict]]:
        """Get all entities organized by domain.
        
        Returns:
            Dictionary with domain as key and list of entities as value
        """
        try:
            states = await self.get_states()
            entities_by_domain = {}
            
            for entity in states:
                entity_id = entity.get('entity_id', '')
                domain = entity_id.split('.')[0] if '.' in entity_id else 'unknown'
                
                if domain not in entities_by_domain:
                    entities_by_domain[domain] = []
                
                entities_by_domain[domain].append({
                    'entity_id': entity_id,
                    'friendly_name': entity.get('attributes', {}).get('friendly_name', entity_id),
                    'state': entity.get('state'),
                    'attributes': entity.get('attributes', {}),
                    'device_class': entity.get('attributes', {}).get('device_class'),
                    'unit_of_measurement': entity.get('attributes', {}).get('unit_of_measurement')
                })
            
            return entities_by_domain
        except Exception as e:
            logger.error(f"Failed to get entities: {e}")
            return {}

    async def get_integrations(self) -> List[Dict]:
        """Get all installed integrations.
        
        Returns:
            List of integration information
        """
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/config/config_entries') as response:
                if response.status == 200:
                    data = await response.json()
                    integrations = []
                    
                    for entry in data:
                        integrations.append({
                            'domain': entry.get('domain'),
                            'title': entry.get('title'),
                            'entry_id': entry.get('entry_id'),
                            'state': entry.get('state'),
                            'source': entry.get('source')
                        })
                    
                    return integrations
                else:
                    logger.error(f"Failed to get integrations: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Failed to get integrations: {e}")
            return []

    async def get_addons(self) -> List[Dict]:
        """Get all installed add-ons.
        
        Returns:
            List of add-on information
        """
        try:
            session = await self._get_session()
            # Try to get add-ons from supervisor API
            async with session.get(f'{self.ha_url}/api/supervisor/addons') as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data and 'addons' in data['data']:
                        return data['data']['addons']
                    return data.get('addons', [])
                else:
                    logger.warning(f"Could not get add-ons: {response.status}")
                    return []
        except Exception as e:
            logger.warning(f"Could not get add-ons (may not be supervisor): {e}")
            return []

    async def get_areas(self) -> List[Dict]:
        """Get all areas defined in Home Assistant.
        
        Returns:
            List of area information
        """
        try:
            session = await self._get_session()
            async with session.get(f'{self.ha_url}/api/config/area_registry') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get areas: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Failed to get areas: {e}")
            return []

    async def get_entities_by_domain(self, domain: str) -> List[Dict]:
        """Get entities filtered by domain.
        
        Args:
            domain: Entity domain (e.g., 'light', 'sensor', 'switch')
            
        Returns:
            List of entities in the specified domain
        """
        all_entities = await self.get_all_entities()
        return all_entities.get(domain, [])

    async def get_entities_by_device_class(self, device_class: str) -> List[Dict]:
        """Get entities filtered by device class.
        
        Args:
            device_class: Device class (e.g., 'motion', 'temperature', 'illuminance')
            
        Returns:
            List of entities with the specified device class
        """
        try:
            all_entities = await self.get_all_entities()
            filtered_entities = []
            
            for domain_entities in all_entities.values():
                for entity in domain_entities:
                    if entity.get('device_class') == device_class:
                        filtered_entities.append(entity)
            
            return filtered_entities
        except Exception as e:
            logger.error(f"Failed to get entities by device class: {e}")
            return []

    async def get_discovery_summary(self) -> Dict:
        """Get comprehensive discovery summary for automation assistance.
        
        Returns:
            Summary of all discovered entities, integrations, and capabilities
        """
        try:
            # Get all discovery data in parallel
            import asyncio
            from datetime import datetime
            
            entities_task = self.get_all_entities()
            integrations_task = self.get_integrations()
            addons_task = self.get_addons()
            areas_task = self.get_areas()
            
            entities_by_domain, integrations, addons, areas = await asyncio.gather(
                entities_task, integrations_task, addons_task, areas_task,
                return_exceptions=True
            )
            
            # Handle exceptions in parallel results
            if isinstance(entities_by_domain, Exception):
                logger.error(f"Failed to get entities: {entities_by_domain}")
                entities_by_domain = {}
            if isinstance(integrations, Exception):
                logger.error(f"Failed to get integrations: {integrations}")
                integrations = []
            if isinstance(addons, Exception):
                logger.warning(f"Failed to get addons: {addons}")
                addons = []
            if isinstance(areas, Exception):
                logger.error(f"Failed to get areas: {areas}")
                areas = []
            
            # Get specific entity types for automation capabilities
            motion_sensors = await self.get_entities_by_device_class('motion')
            temperature_sensors = await self.get_entities_by_device_class('temperature')
            illuminance_sensors = await self.get_entities_by_device_class('illuminance')
            
            # Create summary with useful automation categories
            automation_capabilities = {
                'motion_sensors': len(motion_sensors),
                'temperature_sensors': len(temperature_sensors),
                'illuminance_sensors': len(illuminance_sensors),
                'lights': len(entities_by_domain.get('light', [])),
                'switches': len(entities_by_domain.get('switch', [])),
                'climate_devices': len(entities_by_domain.get('climate', [])),
                'media_players': len(entities_by_domain.get('media_player', [])),
                'cameras': len(entities_by_domain.get('camera', [])),
                'binary_sensors': len(entities_by_domain.get('binary_sensor', [])),
                'sensors': len(entities_by_domain.get('sensor', [])),
                'total_entities': sum(len(entities) for entities in entities_by_domain.values()),
                'available_domains': list(entities_by_domain.keys())
            }
            
            return {
                'entities_by_domain': entities_by_domain,
                'integrations': integrations,
                'addons': addons,
                'areas': areas,
                'automation_capabilities': automation_capabilities,
                'discovery_timestamp': datetime.now().isoformat(),
                'motion_sensors': motion_sensors,
                'temperature_sensors': temperature_sensors,
                'illuminance_sensors': illuminance_sensors
            }
            
        except Exception as e:
            logger.error(f"Failed to get discovery summary: {e}")
            return {
                'entities_by_domain': {},
                'integrations': [],
                'addons': [],
                'areas': [],
                'automation_capabilities': {},
                'discovery_timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_mock_system_info(self) -> Dict[str, Any]:
        """Get mock system information when HA is not available."""
        return {
            'ha_version': 'offline',
            'location_name': 'Home Assistant (Disconnected)',
            'time_zone': 'UTC',
            'unit_system': {'temperature': 'C', 'length': 'km', 'mass': 'kg'},
            'sensors': {
                'sensor.cpu_percent': {
                    'value': 0.0,
                    'unit': '%',
                    'friendly_name': 'CPU Usage (Offline)'
                },
                'sensor.memory_use_percent': {
                    'value': 0.0,
                    'unit': '%',
                    'friendly_name': 'Memory Usage (Offline)'
                },
                'sensor.disk_use_percent': {
                    'value': 0.0,
                    'unit': '%',
                    'friendly_name': 'Disk Usage (Offline)'
                }
            },
            'connection_status': 'offline'
        }


# Synchronous wrapper functions for use in Flask routes
def create_ha_client(ha_url: str, ha_token: str) -> HomeAssistantClient:
    """Create a Home Assistant client instance."""
    return HomeAssistantClient(ha_url, ha_token)


def get_system_resources_sync(ha_client: HomeAssistantClient) -> Dict[str, Any]:
    """Synchronous wrapper to get system resources."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Test connection first
            connected = loop.run_until_complete(ha_client.test_connection())
            if connected:
                return loop.run_until_complete(ha_client.get_system_info())
            else:
                return ha_client.get_mock_system_info()
        finally:
            loop.run_until_complete(ha_client.close())
            loop.close()
    except Exception as e:
        logger.error(f"Error in sync system resources: {e}")
        return ha_client.get_mock_system_info()


def test_ha_connection_sync(ha_client: HomeAssistantClient) -> bool:
    """Synchronous wrapper to test HA connection."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(ha_client.test_connection())
        finally:
            loop.run_until_complete(ha_client.close())
            loop.close()
    except Exception as e:
        logger.error(f"Error testing HA connection: {e}")
        return False
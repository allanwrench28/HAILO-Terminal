#!/usr/bin/env python3
"""
Automation Manager for Hailo AI Terminal
Handles automation recommendations, YAML generation, validation, and deployment
"""

import yaml
import logging
import asyncio
from typing import Dict, List, Tuple
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class AutomationManager:
    """Manages HA automation creation, validation, and deployment."""
    
    def __init__(self, ha_client=None):
        """Initialize the automation manager.
        
        Args:
            ha_client: Home Assistant client for API calls
        """
        self.ha_client = ha_client
        self.automation_templates = self._load_automation_templates()
        self.validation_cache = {}
        self._discovered_entities = None
        self._discovery_cache_time = None

    async def _get_discovered_entities(self) -> Dict:
        """Get discovered entities with caching.
        
        Returns:
            Dictionary containing discovered entities and capabilities
        """
        if (self._discovered_entities is None or 
            (self._discovery_cache_time and 
             (datetime.now() - self._discovery_cache_time).seconds > 300)):
            
            if self.ha_client:
                try:
                    self._discovered_entities = await self.ha_client.get_discovery_summary()
                    self._discovery_cache_time = datetime.now()
                except Exception as e:
                    print(f"Failed to discover entities: {e}")
                    self._discovered_entities = {}
            else:
                self._discovered_entities = {}
        
        return self._discovered_entities or {}

    async def get_relevant_entities_for_automation(
            self, template_id: str) -> Dict[str, List]:
        """Get relevant entities for a specific automation template.
        
        Args:
            template_id: Automation template identifier
            
        Returns:
            Dictionary with entity categories relevant to the automation
        """
        discovered = await self._get_discovered_entities()
        entities_by_domain = discovered.get('entities_by_domain', {})
        
        relevant_entities = {}
        
        if template_id == 'motion_light':
            relevant_entities = {
                'motion_sensors': [e for e in entities_by_domain.get(
                    'binary_sensor', []) if e.get('device_class') == 'motion'],
                'lights': entities_by_domain.get('light', []),
                'light_sensors': [e for e in entities_by_domain.get(
                    'sensor', []) if e.get('device_class') == 'illuminance'],
                'areas': discovered.get('areas', [])
            }
        elif template_id == 'schedule_thermostat':
            relevant_entities = {
                'climate_devices': entities_by_domain.get('climate', []),
                'temperature_sensors': [e for e in entities_by_domain.get(
                    'sensor', []) if e.get('device_class') == 'temperature'],
                'areas': discovered.get('areas', [])
            }
        elif template_id == 'security_lights':
            relevant_entities = {
                'motion_sensors': [e for e in entities_by_domain.get(
                    'binary_sensor', []) if e.get('device_class') == 'motion'],
                'lights': entities_by_domain.get('light', []),
                'switches': entities_by_domain.get('switch', []),
                'cameras': entities_by_domain.get('camera', []),
                'areas': discovered.get('areas', [])
            }
        elif template_id == 'energy_saver':
            relevant_entities = {
                'lights': entities_by_domain.get('light', []),
                'switches': entities_by_domain.get('switch', []),
                'media_players': entities_by_domain.get('media_player', []),
                'climate_devices': entities_by_domain.get('climate', []),
                'presence_sensors': [e for e in entities_by_domain.get(
                    'binary_sensor', []) if e.get('device_class') in 
                    ['occupancy', 'presence']],
                'areas': discovered.get('areas', [])
            }
        elif template_id == 'device_offline':
            relevant_entities = {
                'devices': [],
                'critical_entities': []
            }
            for domain, entities in entities_by_domain.items():
                if domain not in ['sun', 'weather']:
                    relevant_entities['devices'].extend(entities)
        
        return relevant_entities
        
    def _load_automation_templates(self) -> Dict[str, Dict]:
        """Load predefined automation templates."""
        return {
            "motion_light": {
                "name": "Motion-Activated Light",
                "description": "Turn on lights when motion is detected",
                "category": "lighting",
                "complexity": "beginner",
                "template": {
                    "alias": "Motion Light - {room}",
                    "description": "Turn on {light} when motion in {room}",
                    "trigger": [
                        {
                            "platform": "state",
                            "entity_id": "{motion_sensor}",
                            "from": "off",
                            "to": "on"
                        }
                    ],
                    "condition": [
                        {
                            "condition": "numeric_state",
                            "entity_id": "{light_sensor}",
                            "below": 50
                        }
                    ],
                    "action": [
                        {
                            "service": "light.turn_on",
                            "target": {
                                "entity_id": "{light}"
                            },
                            "data": {
                                "brightness_pct": 80
                            }
                        }
                    ],
                    "mode": "single"
                },
                "required_entities": ["motion_sensor", "light"],
                "optional_entities": ["light_sensor"]
            },
            
            "schedule_thermostat": {
                "name": "Scheduled Thermostat",
                "description": "Adjust thermostat based on schedule",
                "category": "climate",
                "complexity": "intermediate",
                "template": {
                    "alias": "Thermostat Schedule - {name}",
                    "description": "Set thermostat to {temperature}°F",
                    "trigger": [
                        {
                            "platform": "time",
                            "at": "{time}"
                        }
                    ],
                    "condition": [],
                    "action": [
                        {
                            "service": "climate.set_temperature",
                            "target": {
                                "entity_id": "{thermostat}"
                            },
                            "data": {
                                "temperature": "{temperature}"
                            }
                        }
                    ],
                    "mode": "single"
                },
                "required_entities": ["thermostat"],
                "optional_entities": []
            },
            
            "device_offline_notification": {
                "name": "Device Offline Alert",
                "description": "Send notification when device goes offline",
                "category": "monitoring",
                "complexity": "intermediate",
                "template": {
                    "alias": "Device Offline - {device_name}",
                    "description": "Alert when {device_name} unavailable",
                    "trigger": [
                        {
                            "platform": "state",
                            "entity_id": "{device_entity}",
                            "to": "unavailable",
                            "for": {
                                "minutes": 5
                            }
                        }
                    ],
                    "condition": [],
                    "action": [
                        {
                            "service": "notify.{notification_service}",
                            "data": {
                                "title": "Device Offline",
                                "message": "{device_name} offline for 5 min",
                                "data": {
                                    "priority": "high"
                                }
                            }
                        }
                    ],
                    "mode": "single"
                },
                "required_entities": ["device_entity"],
                "optional_entities": []
            },
            
            "security_lights": {
                "name": "Security Light System",
                "description": "Turn on all lights when security is triggered",
                "category": "security",
                "complexity": "advanced",
                "template": {
                    "alias": "Security Alert - All Lights",
                    "description": "Turn on lights when security triggered",
                    "trigger": [
                        {
                            "platform": "state",
                            "entity_id": "{security_sensor}",
                            "from": "off",
                            "to": "on"
                        }
                    ],
                    "condition": [
                        {
                            "condition": "time",
                            "after": "sunset",
                            "before": "sunrise"
                        }
                    ],
                    "action": [
                        {
                            "service": "light.turn_on",
                            "target": {
                                "area_id": "all"
                            },
                            "data": {
                                "brightness_pct": 100,
                                "color_name": "red"
                            }
                        },
                        {
                            "service": "notify.{notification_service}",
                            "data": {
                                "title": "Security Alert",
                                "message": "Security triggered - lights on"
                            }
                        }
                    ],
                    "mode": "single"
                },
                "required_entities": ["security_sensor"],
                "optional_entities": []
            },
            
            "energy_saver": {
                "name": "Energy Saver Mode",
                "description": "Turn off devices when away to save energy",
                "category": "energy",
                "complexity": "advanced",
                "template": {
                    "alias": "Energy Saver - Away Mode",
                    "description": "Turn off non-essential devices when away",
                    "trigger": [
                        {
                            "platform": "state",
                            "entity_id": "person.{person}",
                            "from": "home",
                            "to": "not_home",
                            "for": {
                                "minutes": 15
                            }
                        }
                    ],
                    "condition": [],
                    "action": [
                        {
                            "service": "light.turn_off",
                            "target": {
                                "area_id": ["living_room", "kitchen"]
                            }
                        },
                        {
                            "service": "climate.set_temperature",
                            "target": {
                                "entity_id": "{thermostat}"
                            },
                            "data": {
                                "temperature": 65
                            }
                        },
                        {
                            "service": "media_player.turn_off",
                            "target": {
                                "area_id": "all"
                            }
                        }
                    ],
                    "mode": "single"
                },
                "required_entities": ["person"],
                "optional_entities": ["thermostat"]
            }
        }
    
    async def get_automation_recommendations(self, user_request: str,
                                             available_entities: List[str] = None
                                             ) -> List[Dict]:
        """Get smart automation recommendations based on user request and discovered entities.
        
        Args:
            user_request: User's natural language request
            available_entities: List of available Home Assistant entities (legacy)
            
        Returns:
            List of recommended automation templates with feasibility scores
        """
        recommendations = []
        request_lower = user_request.lower()
        
        # Get discovered entities for smarter recommendations
        discovered = await self._get_discovered_entities()
        capabilities = discovered.get('automation_capabilities', {})
        
        # Keywords for different automation types
        keywords = {
            "lighting": ["light", "lamp", "brightness", "motion"],
            "climate": ["temperature", "thermostat", "heating", "hvac"],
            "security": ["security", "alarm", "door", "camera", "lock"],
            "energy": ["energy", "save", "power", "consumption"],
            "monitoring": ["monitor", "alert", "notification", "offline"]
        }
        
        # Score templates based on keyword matches
        for template_id, template in self.automation_templates.items():
            score = 0
            category = template["category"]
            
            # Check category keywords
            if category in keywords:
                for keyword in keywords[category]:
                    if keyword in request_lower:
                        score += 2
            
            # Check template description
            for word in template["description"].lower().split():
                if word in request_lower:
                    score += 1
            
            # Check if required entities are available
            entity_compatibility = 1.0
            if available_entities:
                required_entities = template.get("required_entities", [])
                matching_entities = sum(
                    1 for req in required_entities
                    if any(req in entity for entity in available_entities)
                )
                if required_entities:
                    entity_compatibility = (
                        matching_entities / len(required_entities)
                    )
            
            final_score = score * entity_compatibility
            
            if final_score > 0:
                recommendations.append({
                    "id": template_id,
                    "name": template["name"],
                    "description": template["description"],
                    "category": template["category"],
                    "complexity": template["complexity"],
                    "score": final_score,
                    "template": template["template"],
                    "required_entities": template.get("required_entities", []),
                    "optional_entities": template.get("optional_entities", [])
                })
        
        # Sort by score (descending)
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def generate_automation_yaml(self, template_id: str,
                                  parameters: Dict[str, str]
                                  ) -> Tuple[str, Dict]:
        """Generate automation YAML from template and parameters.
        
        Args:
            template_id: ID of the automation template
            parameters: Dictionary of parameter values
            
        Returns:
            Tuple of (YAML string, automation dictionary)
        """
        if template_id not in self.automation_templates:
            raise ValueError(f"Unknown template ID: {template_id}")
        
        template = self.automation_templates[template_id]["template"].copy()
        
        # Replace template variables with actual values
        def replace_variables(obj):
            if isinstance(obj, dict):
                return {k: replace_variables(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_variables(item) for item in obj]
            elif isinstance(obj, str):
                # Replace template variables like {variable}
                for param, value in parameters.items():
                    obj = obj.replace(f"{{{param}}}", str(value))
                return obj
            else:
                return obj
        
        automation_dict = replace_variables(template)
        
        # Generate unique ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        automation_dict["id"] = f"hailo_auto_{template_id}_{timestamp}"
        
        # Generate YAML
        yaml_content = yaml.dump(
            automation_dict, default_flow_style=False,
            allow_unicode=True, sort_keys=False
        )
        
        return yaml_content, automation_dict

    def suggest_automations_for_query(self, query: str) -> List[Dict]:
        """Suggest automations based on user query using keyword matching.
        
        Args:
            query: User's natural language query
            
        Returns:
            List of suggested automation templates
        """
        query_lower = query.lower()
        suggestions = []
        
        # Keywords mapping to templates
        keyword_map = {
            "motion_light": ["motion", "light", "turn on", "detect",
                             "movement"],
            "schedule_thermostat": ["schedule", "thermostat", "temperature",
                                    "morning", "evening", "time"],
            "device_offline": ["offline", "notify", "device", "down",
                               "unavailable"],
            "security_lights": ["security", "night", "protect", "alert",
                                "alarm"],
            "energy_saver": ["energy", "away", "save", "power", "efficiency"]
        }
        
        # Score each template based on keyword matches
        template_scores = {}
        for template_id, keywords in keyword_map.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                template_scores[template_id] = score
        
        # Sort by score and return matching templates
        sorted_templates = sorted(template_scores.items(),
                                  key=lambda x: x[1], reverse=True)
        
        for template_id, score in sorted_templates:
            if template_id in self.automation_templates:
                template_info = self.automation_templates[template_id].copy()
                template_info["match_score"] = score
                suggestions.append(template_info)
        
        # If no matches, return all templates
        if not suggestions:
            for template_id, template_info in (
                    self.automation_templates.items()):
                template_copy = template_info.copy()
                template_copy["match_score"] = 0
                suggestions.append(template_copy)
        
        return suggestions
    
    async def validate_automation(self, automation_dict: Dict
                                  ) -> Tuple[bool, List[str]]:
        """Validate automation configuration.
        
        Args:
            automation_dict: Automation configuration dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Basic structure validation
        required_keys = ["alias", "trigger", "action"]
        for key in required_keys:
            if key not in automation_dict:
                errors.append(f"Missing required key: {key}")
        
        # Validate triggers
        if "trigger" in automation_dict:
            triggers = automation_dict["trigger"]
            if not isinstance(triggers, list):
                triggers = [triggers]
            
            for i, trigger in enumerate(triggers):
                if not isinstance(trigger, dict):
                    errors.append(f"Trigger {i} must be a dictionary")
                    continue
                
                if "platform" not in trigger:
                    errors.append(f"Trigger {i} missing platform")
                
                # Validate specific trigger types
                platform = trigger.get("platform")
                if platform == "state" and "entity_id" not in trigger:
                    errors.append(f"State trigger {i} missing entity_id")
                elif platform == "time" and "at" not in trigger:
                    errors.append(f"Time trigger {i} missing 'at' field")
        
        # Validate actions
        if "action" in automation_dict:
            actions = automation_dict["action"]
            if not isinstance(actions, list):
                actions = [actions]
            
            for i, action in enumerate(actions):
                if not isinstance(action, dict):
                    errors.append(f"Action {i} must be a dictionary")
                    continue
                
                if "service" not in action:
                    errors.append(f"Action {i} missing service")
                else:
                    # Validate service format
                    service = action["service"]
                    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*$', service):
                        errors.append(f"Action {i} has invalid service format: {service}")
        
        # Check for entity existence if HA client available
        if self.ha_client and not errors:
            try:
                # Extract all entity references and check if they exist
                entity_refs = self._extract_entity_references(automation_dict)
                for entity_id in entity_refs:
                    if not await self._entity_exists(entity_id):
                        errors.append(f"Entity does not exist: {entity_id}")
            except Exception as e:
                logger.warning(f"Could not validate entities: {e}")
        
        return len(errors) == 0, errors
    
    def _extract_entity_references(self, automation_dict: Dict) -> List[str]:
        """Extract all entity IDs referenced in automation."""
        entities = []
        
        def extract_from_obj(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == "entity_id":
                        if isinstance(value, str):
                            entities.append(value)
                        elif isinstance(value, list):
                            entities.extend(value)
                    else:
                        extract_from_obj(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_from_obj(item)
        
        extract_from_obj(automation_dict)
        return list(set(entities))  # Remove duplicates
    
    async def _entity_exists(self, entity_id: str) -> bool:
        """Check if entity exists in Home Assistant."""
        if not self.ha_client:
            return True  # Assume valid if no client
        
        try:
            state = await self.ha_client.get_entity_state(entity_id)
            return state is not None
        except Exception:
            return False
    
    async def test_automation(self, automation_dict: Dict) -> Tuple[bool, str]:
        """Test automation by creating a temporary version.
        
        Args:
            automation_dict: Automation configuration
            
        Returns:
            Tuple of (success, message)
        """
        if not self.ha_client:
            return False, "No Home Assistant connection available for testing"
        
        try:
            # First validate the automation
            is_valid, errors = await self.validate_automation(automation_dict)
            if not is_valid:
                return False, f"Validation failed: {'; '.join(errors)}"
            
            # Create a test automation with disabled mode
            test_automation = automation_dict.copy()
            test_automation["id"] = f"test_{test_automation.get('id', 'automation')}"
            test_automation["alias"] = f"TEST - {test_automation.get('alias', 'Test Automation')}"
            test_automation["mode"] = "single"
            
            # Try to create the automation via HA API
            success = await self.ha_client.create_automation(test_automation)
            
            if success:
                # Clean up test automation
                await asyncio.sleep(1)  # Give HA time to process
                await self.ha_client.delete_automation(test_automation["id"])
                return True, "Automation test passed successfully"
            else:
                return False, "Failed to create test automation"
                
        except Exception as e:
            logger.error(f"Error testing automation: {e}")
            return False, f"Test error: {str(e)}"
    
    async def save_automation(self, automation_dict: Dict, 
                            test_first: bool = True) -> Tuple[bool, str]:
        """Save automation to Home Assistant.
        
        Args:
            automation_dict: Automation configuration
            test_first: Whether to test automation before saving
            
        Returns:
            Tuple of (success, message)
        """
        if not self.ha_client:
            return False, "No Home Assistant connection available"
        
        try:
            # Test automation first if requested
            if test_first:
                test_success, test_message = await self.test_automation(automation_dict)
                if not test_success:
                    return False, f"Test failed: {test_message}"
            
            # Save the automation
            success = await self.ha_client.create_automation(automation_dict)
            
            if success:
                automation_name = automation_dict.get("alias", "Unnamed Automation")
                return True, f"Automation '{automation_name}' saved successfully"
            else:
                return False, "Failed to save automation to Home Assistant"
                
        except Exception as e:
            logger.error(f"Error saving automation: {e}")
            return False, f"Save error: {str(e)}"
    
    def export_automation_yaml(self, automation_dict: Dict) -> str:
        """Export automation as clean YAML for manual use."""
        # Remove ID for manual installations
        clean_automation = automation_dict.copy()
        if "id" in clean_automation:
            del clean_automation["id"]
        
        return yaml.dump(clean_automation, default_flow_style=False,
                        allow_unicode=True, sort_keys=False)
    
    def get_automation_suggestions(self, partial_request: str) -> List[str]:
        """Get quick automation suggestions for autocomplete."""
        suggestions = []
        request_lower = partial_request.lower()
        
        # Common automation patterns
        patterns = [
            "Turn on lights when motion detected",
            "Send notification when door opens",
            "Adjust thermostat based on schedule",
            "Turn off devices when away",
            "Flash lights when doorbell rings",
            "Start coffee maker at 7 AM",
            "Lock doors at bedtime",
            "Turn on fan when temperature rises",
            "Dim lights at sunset",
            "Alert when washing machine finishes"
        ]
        
        for pattern in patterns:
            if any(word in pattern.lower() for word in request_lower.split()):
                suggestions.append(pattern)
        
        return suggestions[:5]
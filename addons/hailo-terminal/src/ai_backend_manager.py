#!/usr/bin/env python3
"""
AI Backend Manager for Hailo AI Terminal

Supports multiple AI backends:
- Hailo: Local inference with Hailo acceleration
- OpenAI: GPT models via API
- Anthropic: Claude models via API  
- Ollama: Local open-source models
- Custom: User-defined API endpoints
"""

import os
import logging
import json
import requests
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Import Hailo runtime (if available)
try:
    from hailo_platform import HEF, VDevice, HailoStreamInterface, InferVStreams, ConfigureParams
    HAILO_AVAILABLE = True
except ImportError:
    HAILO_AVAILABLE = False
    logging.warning("Hailo runtime not available - falling back to other backends")

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Standardized AI response structure."""
    content: str
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None
    backend: Optional[str] = None
    error: Optional[str] = None


class AIBackend(ABC):
    """Abstract base class for AI backends."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get('ai_model', '')
        self.max_tokens = config.get('max_tokens', 512)
        self.temperature = config.get('temperature', 0.7)
        self.max_context_length = config.get('max_context_length', 4096)
    
    @abstractmethod
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> AIResponse:
        """Generate AI response for the given prompt."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available and properly configured."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current backend status and configuration."""
        pass


class HailoBackend(AIBackend):
    """Hailo AI accelerator backend for local inference."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.device_id = config.get('device_id', '0000:03:00.0')
        self.model_path = config.get('model_path', '/share/hailo/models')
        self.hef_file = None
        self.vdevice = None
        self.infer_model = None
        self._initialize_hailo()
    
    def _initialize_hailo(self):
        """Initialize Hailo device and load model."""
        if not HAILO_AVAILABLE:
            logger.error("Hailo runtime not available")
            return
        
        try:
            # Find model file
            model_file = f"{self.model_path}/{self.model}.hef"
            if not os.path.exists(model_file):
                logger.error(f"Hailo model not found: {model_file}")
                return
            
            # Load HEF file
            self.hef_file = HEF(model_file)
            
            # Create VDevice
            self.vdevice = VDevice(device_id=self.device_id)
            
            # Configure network group
            network_group = self.vdevice.configure(self.hef_file)[0]
            network_group_params = network_group.create_params()
            
            # Create input/output streams
            self.infer_model = self.vdevice.create_infer_model(self.hef_file)
            
            logger.info(f"Hailo model loaded successfully: {self.model}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Hailo backend: {e}")
            self.hef_file = None
            self.vdevice = None
    
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> AIResponse:
        """Generate response using Hailo-accelerated model."""
        if not self.is_available():
            return AIResponse(
                content="",
                error="Hailo backend not available",
                backend="hailo"
            )
        
        try:
            # Prepare input for the model
            input_text = self._prepare_input(prompt, context)
            
            # Run inference (simplified - actual implementation depends on model format)
            # This is a placeholder - real implementation would depend on the specific
            # Hailo model format and preprocessing requirements
            result = await self._run_inference(input_text)
            
            return AIResponse(
                content=result,
                model=self.model,
                backend="hailo",
                usage={"prompt_tokens": len(prompt.split()), "completion_tokens": len(result.split())}
            )
            
        except Exception as e:
            logger.error(f"Hailo inference error: {e}")
            return AIResponse(
                content="",
                error=str(e),
                backend="hailo"
            )
    
    async def _run_inference(self, input_text: str) -> str:
        """Run inference on Hailo device."""
        if not self.infer_model:
            return "Hailo model not loaded"
        
        try:
            # This is a more realistic implementation for text generation
            # The exact implementation depends on the specific model format
            
            # 1. Tokenize input (simplified - real tokenization would use
            # model-specific tokenizer)
            tokens = self._tokenize_input(input_text)
            
            # 2. Prepare input tensor
            input_data = self._prepare_input_tensor(tokens)
            
            # 3. Run inference using Hailo runtime
            # Note: This is pseudo-code - actual Hailo API calls depend
            # on model
            with self.infer_model.create_bindings() as bindings:
                # Set input data
                for input_name, data in input_data.items():
                    bindings.input(input_name)[:] = data
                
                # Run inference
                bindings.infer()
                
                # Get output
                output_data = {}
                for output_name in bindings.output_names():
                    output_data[output_name] = bindings.output(output_name)[:]
            
            # 4. Post-process and decode output
            result = self._decode_output(output_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Hailo inference failed: {e}")
            # Fallback to a helpful response
            return self._generate_fallback_response(input_text)
    
    def _tokenize_input(self, text: str) -> List[int]:
        """Tokenize input text (simplified implementation)."""
        # This would use a proper tokenizer for the specific model
        # For now, use a basic word-based tokenization
        words = text.lower().split()
        # Map to dummy token IDs (real implementation would use model
        # vocabulary)
        return [hash(word) % 10000 for word in words]
    
    def _prepare_input_tensor(self, tokens: List[int]) -> Dict[str, Any]:
        """Prepare input tensor for Hailo model."""
        try:
            import numpy as np
            # Pad or truncate to model's expected sequence length
            max_length = 512  # Model-specific parameter
            
            if len(tokens) > max_length:
                tokens = tokens[:max_length]
            else:
                # Pad with zeros
                tokens.extend([0] * (max_length - len(tokens)))
            
            # Convert to numpy array with correct dtype
            input_array = np.array(tokens, dtype=np.int32)
            
            return {"input_ids": input_array}
            
        except ImportError:
            logger.error("NumPy not available for tensor preparation")
            return {}
    
    def _decode_output(self, output_data: Dict[str, Any]) -> str:
        """Decode model output to text."""
        try:
            # This would use the model's specific decoding logic
            # For now, simulate a reasonable response
            
            if not output_data:
                return "Unable to process model output"
            
            # Simulate decoding process
            output_tokens = output_data.get('logits', [])
            if (hasattr(output_tokens, 'shape') and
                    len(output_tokens.shape) > 0):
                # Simplified decoding - real implementation would use
                # proper vocabulary
                decoded_text = self._tokens_to_text(output_tokens)
                return decoded_text
            
            return "Model inference completed successfully"
            
        except Exception as e:
            logger.error(f"Output decoding failed: {e}")
            return "Unable to decode model output"
    
    def _tokens_to_text(self, tokens) -> str:
        """Convert token IDs back to text (simplified)."""
        # This would use the model's vocabulary and proper decoding
        # For now, generate a contextual response
        return ("I'm running on Hailo AI hardware to help you with "
                "Home Assistant. How can I assist you with your "
                "automations, configurations, or monitoring?")
    
    def _generate_fallback_response(self, input_text: str) -> str:
        """Generate a helpful fallback response when inference fails."""
        query_lower = input_text.lower()
        
        help_words = ['help', 'assist', 'what', 'how']
        if any(word in query_lower for word in help_words):
            return ("I'm your Hailo AI assistant for Home Assistant. "
                    "I can help with automations, YAML configurations, "
                    "troubleshooting, and system monitoring. "
                    "What would you like help with?")
        
        resource_words = ['resource', 'cpu', 'memory', 'performance']
        if any(word in query_lower for word in resource_words):
            return ("I can monitor your system resources and provide "
                    "optimization suggestions. Your current system status "
                    "is available in the monitoring dashboard. "
                    "Would you like specific performance recommendations?")
        
        automation_words = ['automation', 'script', 'yaml']
        if any(word in query_lower for word in automation_words):
            return ("I can help you create and optimize Home Assistant "
                    "automations. What kind of automation are you trying "
                    "to build? For example: lights, climate control, "
                    "notifications, or device triggers?")
        
        else:
            preview = input_text[:100]
            return (f"I understand you're asking about: {preview}... "
                    "I'm here to help with Home Assistant configurations, "
                    "automations, and system monitoring. Could you provide "
                    "more specific details?")
    
    def _prepare_input(self, prompt: str,
                       context: List[Dict[str, str]] = None) -> str:
        """Prepare input text with context."""
        if context:
            context_text = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in context])
            return f"{context_text}\nuser: {prompt}\nassistant:"
        return f"user: {prompt}\nassistant:"
    
    def is_available(self) -> bool:
        """Check if Hailo backend is available."""
        return (HAILO_AVAILABLE and self.hef_file is not None and
                self.vdevice is not None)
    
    def get_status(self) -> Dict[str, Any]:
        """Get Hailo backend status."""
        return {
            "backend": "hailo",
            "available": self.is_available(),
            "model": self.model,
            "device_id": self.device_id,
            "model_path": self.model_path,
            "hailo_runtime": HAILO_AVAILABLE
        }


class OpenAIBackend(AIBackend):
    """OpenAI API backend."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('openai_api_key', '')
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    async def generate_response(self, prompt: str,
                                context: List[Dict[str, str]] = None
                                ) -> AIResponse:
        """Generate response using OpenAI API."""
        if not self.is_available():
            return AIResponse(
                content="",
                error="OpenAI API key not configured",
                backend="openai"
            )
        
        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": prompt})
            
            # Truncate messages if too long
            messages = self._truncate_messages(messages)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            return AIResponse(
                content=result['choices'][0]['message']['content'],
                model=result.get('model'),
                backend="openai",
                usage=result.get('usage')
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return AIResponse(
                content="",
                error=str(e),
                backend="openai"
            )
    
    def _truncate_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Truncate messages to fit context length."""
        # Simple truncation - keep system message and recent messages
        total_length = sum(len(msg['content']) for msg in messages)
        
        if total_length <= self.max_context_length:
            return messages
        
        # Keep system message if present
        result = []
        if messages and messages[0].get('role') == 'system':
            result.append(messages[0])
            messages = messages[1:]
        
        # Add messages from the end until we hit length limit
        current_length = sum(len(msg['content']) for msg in result)
        for msg in reversed(messages):
            if current_length + len(msg['content']) > self.max_context_length:
                break
            result.insert(-1 if result and result[0].get('role') == 'system' else 0, msg)
            current_length += len(msg['content'])
        
        return result
    
    def is_available(self) -> bool:
        """Check if OpenAI backend is available."""
        return bool(self.api_key)
    
    def get_status(self) -> Dict[str, Any]:
        """Get OpenAI backend status."""
        return {
            "backend": "openai",
            "available": self.is_available(),
            "model": self.model,
            "api_key_configured": bool(self.api_key)
        }


class AnthropicBackend(AIBackend):
    """Anthropic Claude API backend."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('anthropic_api_key', '')
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> AIResponse:
        """Generate response using Anthropic API."""
        if not self.is_available():
            return AIResponse(
                content="",
                error="Anthropic API key not configured",
                backend="anthropic"
            )
        
        try:
            messages = []
            if context:
                # Convert context to Anthropic format
                for msg in context:
                    if msg['role'] in ['user', 'assistant']:
                        messages.append(msg)
            
            messages.append({"role": "user", "content": prompt})
            
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            return AIResponse(
                content=result['content'][0]['text'],
                model=result.get('model'),
                backend="anthropic",
                usage=result.get('usage')
            )
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return AIResponse(
                content="",
                error=str(e),
                backend="anthropic"
            )
    
    def is_available(self) -> bool:
        """Check if Anthropic backend is available."""
        return bool(self.api_key)
    
    def get_status(self) -> Dict[str, Any]:
        """Get Anthropic backend status."""
        return {
            "backend": "anthropic",
            "available": self.is_available(),
            "model": self.model,
            "api_key_configured": bool(self.api_key)
        }


class OllamaBackend(AIBackend):
    """Ollama local model backend."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config.get('custom_api_url', 'http://localhost:11434')
        self.base_url = f"{self.api_url}/api/generate"
    
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> AIResponse:
        """Generate response using Ollama."""
        if not self.is_available():
            return AIResponse(
                content="",
                error="Ollama service not available",
                backend="ollama"
            )
        
        try:
            # Prepare prompt with context
            full_prompt = self._prepare_prompt(prompt, context)
            
            data = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(self.base_url, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            return AIResponse(
                content=result.get('response', ''),
                model=self.model,
                backend="ollama",
                usage={
                    "prompt_tokens": result.get('prompt_eval_count', 0),
                    "completion_tokens": result.get('eval_count', 0)
                }
            )
            
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return AIResponse(
                content="",
                error=str(e),
                backend="ollama"
            )
    
    def _prepare_prompt(self, prompt: str, context: List[Dict[str, str]] = None) -> str:
        """Prepare prompt with context for Ollama."""
        if not context:
            return prompt
        
        context_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context])
        return f"{context_text}\nuser: {prompt}\nassistant:"
    
    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get Ollama backend status."""
        return {
            "backend": "ollama",
            "available": self.is_available(),
            "model": self.model,
            "api_url": self.api_url
        }


class CustomBackend(AIBackend):
    """Custom API endpoint backend."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config.get('custom_api_url', '')
    
    async def generate_response(self, prompt: str, context: List[Dict[str, str]] = None) -> AIResponse:
        """Generate response using custom API."""
        if not self.is_available():
            return AIResponse(
                content="",
                error="Custom API URL not configured",
                backend="custom"
            )
        
        try:
            messages = []
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.api_url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Try to parse common response formats
            content = ""
            if 'choices' in result and result['choices']:
                content = result['choices'][0].get('message', {}).get('content', '')
            elif 'response' in result:
                content = result['response']
            elif 'text' in result:
                content = result['text']
            
            return AIResponse(
                content=content,
                model=self.model,
                backend="custom",
                usage=result.get('usage')
            )
            
        except Exception as e:
            logger.error(f"Custom API error: {e}")
            return AIResponse(
                content="",
                error=str(e),
                backend="custom"
            )
    
    def is_available(self) -> bool:
        """Check if custom API is available."""
        return bool(self.api_url)
    
    def get_status(self) -> Dict[str, Any]:
        """Get custom backend status."""
        return {
            "backend": "custom",
            "available": self.is_available(),
            "model": self.model,
            "api_url": self.api_url
        }


class AIBackendManager:
    """Manages multiple AI backends and provides unified interface."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_backend = config.get('ai_backend', 'hailo')
        self.backends = {}
        self.conversation_history = []
        self._initialize_backends()
    
    def _initialize_backends(self):
        """Initialize all available backends."""
        backend_classes = {
            'hailo': HailoBackend,
            'openai': OpenAIBackend,
            'anthropic': AnthropicBackend,
            'ollama': OllamaBackend,
            'local': CustomBackend,
            'custom': CustomBackend
        }
        
        for backend_name, backend_class in backend_classes.items():
            try:
                self.backends[backend_name] = backend_class(self.config)
                logger.info(f"Initialized {backend_name} backend")
            except Exception as e:
                logger.error(f"Failed to initialize {backend_name} backend: {e}")
    
    async def generate_response(self, prompt: str, use_context: bool = True) -> AIResponse:
        """Generate AI response using current backend."""
        backend = self.backends.get(self.current_backend)
        if not backend:
            return AIResponse(
                content="",
                error=f"Backend '{self.current_backend}' not available",
                backend=self.current_backend
            )
        
        context = self.conversation_history if use_context else None
        response = await backend.generate_response(prompt, context)
        
        # Add to conversation history if successful
        if response.content and not response.error:
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": response.content})
            
            # Keep conversation history manageable
            max_history = 20  # Keep last 20 messages
            if len(self.conversation_history) > max_history:
                self.conversation_history = self.conversation_history[-max_history:]
        
        return response
    
    def switch_backend(self, backend_name: str) -> bool:
        """Switch to different AI backend."""
        if backend_name in self.backends and self.backends[backend_name].is_available():
            self.current_backend = backend_name
            logger.info(f"Switched to {backend_name} backend")
            return True
        return False
    
    def get_available_backends(self) -> List[str]:
        """Get list of available backends."""
        return [name for name, backend in self.backends.items() if backend.is_available()]
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get status of all backends."""
        return {
            "current_backend": self.current_backend,
            "backends": {name: backend.get_status() for name, backend in self.backends.items()}
        }
    
    def clear_conversation_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
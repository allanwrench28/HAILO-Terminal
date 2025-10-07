# 🤖 AI Backend Configuration Guide

The Hailo AI Terminal supports multiple AI backends, giving you flexibility in how you want to process AI requests. Here's everything you need to know about AI model options and the role of your Hailo hardware.

## 🧠 Understanding Hailo's Role

### What is the Hailo-8?
The **Hailo-8** is an **AI accelerator chip** (not a complete AI system) that can:
- ✅ **Accelerate** compatible AI models by 10-100x
- ✅ **Reduce power consumption** significantly compared to CPU/GPU
- ✅ **Run locally** without internet connectivity
- ✅ **Process** computer vision, NLP, and other AI workloads

### What Hailo is NOT
- ❌ **Not a complete AI model** - it needs models designed for it
- ❌ **Not ChatGPT/Claude** - it's hardware acceleration
- ❌ **Not plug-and-play** - requires Hailo-optimized models (.hef files)

## 🔄 Supported AI Backends

### 1. **Hailo Backend** (Default - Local Processing)
**Best for**: Privacy, no internet required, maximum performance

```yaml
ai_backend: "hailo"
ai_model: "llama2-7b-chat"  # Must be Hailo-optimized (.hef file)
model_path: "/share/hailo/models"
```

**Available Models:**
- `llama2-7b-chat` - Conversational AI (7B parameters)
- `llama2-13b-chat` - Larger conversational model (13B parameters)
- `mistral-7b-instruct` - Instruction-following model
- `codellama-7b` - Code generation and analysis
- `custom-model` - Your own Hailo-compiled model

**Requirements:**
- Hailo-8 hardware installed
- Model files (.hef) downloaded from Hailo Model Zoo
- 4GB+ RAM for model loading

### 2. **OpenAI Backend** (Cloud-based)
**Best for**: Latest models, best quality responses

```yaml
ai_backend: "openai"
ai_model: "gpt-4"  # or gpt-3.5-turbo, gpt-4-turbo
openai_api_key: "sk-your-api-key-here"
```

**Available Models:**
- `gpt-4` - Most capable, slower, more expensive
- `gpt-4-turbo` - Faster GPT-4 with larger context
- `gpt-3.5-turbo` - Fast, cost-effective, good quality

**Requirements:**
- OpenAI API account and API key
- Internet connectivity
- Pay-per-use pricing

### 3. **Anthropic Backend** (Claude AI)
**Best for**: Long conversations, analysis, coding help

```yaml
ai_backend: "anthropic"
ai_model: "claude-3-sonnet"  # or claude-3-opus, claude-3-haiku
anthropic_api_key: "sk-ant-your-api-key-here"
```

**Available Models:**
- `claude-3-opus` - Most capable, best reasoning
- `claude-3-sonnet` - Balanced performance and cost
- `claude-3-haiku` - Fastest, most cost-effective

**Requirements:**
- Anthropic API account and API key
- Internet connectivity
- Pay-per-use pricing

### 4. **Ollama Backend** (Local Open Source)
**Best for**: Free local models, privacy, experimentation

```yaml
ai_backend: "ollama"
ai_model: "llama2:7b"  # Any Ollama-supported model
custom_api_url: "http://localhost:11434"
```

**Available Models:**
- `llama2:7b` / `llama2:13b` - Meta's Llama 2
- `mistral:7b` - Mistral AI's open model
- `codellama:7b` - Code-specialized Llama
- `vicuna:7b` - Fine-tuned conversational model
- `phi:2.7b` - Microsoft's compact model

**Requirements:**
- Ollama installed on your system
- Sufficient RAM (8GB+ recommended)
- No API keys needed

### 5. **Local/Custom Backend**
**Best for**: Custom setups, enterprise deployments

```yaml
ai_backend: "local"
custom_api_url: "http://your-local-ai:8000/v1/chat/completions"
ai_model: "your-custom-model"
```

**Use Cases:**
- Local LM Studio server
- Custom FastAPI AI service
- Enterprise AI endpoints
- Self-hosted models

## ⚡ Hailo Acceleration Scenarios

### Scenario 1: Pure Hailo (Maximum Performance)
```yaml
ai_backend: "hailo"
ai_model: "llama2-7b-chat"
# All processing on Hailo chip - fastest, most private
```

### Scenario 2: Hybrid (Best of Both Worlds)
```yaml
ai_backend: "openai"        # Primary: Cloud AI for complex queries
ai_model: "gpt-4"
# Hailo handles: Image processing, embeddings, local inference
# OpenAI handles: Complex reasoning, latest knowledge
```

### Scenario 3: Local + Hailo Acceleration
```yaml
ai_backend: "ollama"
ai_model: "llama2:7b"
# Ollama + Hailo acceleration for compatible operations
```

## 🔧 Configuration Examples

### Basic Home Assistant Helper
```yaml
# Simple, local, private
ai_backend: "hailo"
ai_model: "llama2-7b-chat"
max_context_length: 2048
temperature: 0.3
```

### Advanced AI Assistant
```yaml
# Best quality responses
ai_backend: "openai"
ai_model: "gpt-4-turbo"
openai_api_key: "sk-your-key"
max_context_length: 8192
temperature: 0.7
max_tokens: 1024
```

### Privacy-Focused Setup
```yaml
# No data leaves your network
ai_backend: "ollama"
ai_model: "mistral:7b"
custom_api_url: "http://localhost:11434"
max_context_length: 4096
```

### Development/Testing
```yaml
# Switch backends easily
ai_backend: "hailo"  # Change to test different backends
ai_model: "llama2-7b-chat"
# Keep multiple API keys configured for testing
openai_api_key: "sk-test-key"
anthropic_api_key: "sk-ant-test-key"
```

## 📊 Performance Comparison

| Backend | Speed | Cost | Privacy | Quality | Internet |
|---------|-------|------|---------|---------|----------|
| **Hailo** | ⚡⚡⚡⚡⚡ | 💰 (one-time) | 🔒🔒🔒🔒🔒 | ⭐⭐⭐⭐ | ❌ |
| **OpenAI** | ⚡⚡⚡ | 💰💰💰 | 🔒 | ⭐⭐⭐⭐⭐ | ✅ |
| **Anthropic** | ⚡⚡⚡ | 💰💰💰 | 🔒 | ⭐⭐⭐⭐⭐ | ✅ |
| **Ollama** | ⚡⚡ | 💰 (free) | 🔒🔒🔒🔒🔒 | ⭐⭐⭐ | ❌ |
| **Local** | ⚡⚡ | 💰 (varies) | 🔒🔒🔒🔒🔒 | ⭐⭐⭐ | ❌ |

## 🚀 Getting Started

### Step 1: Choose Your Backend
Consider your priorities:
- **Privacy first**: Use Hailo or Ollama
- **Best quality**: Use OpenAI or Anthropic
- **Cost-effective**: Use Hailo (after initial setup)
- **Experimenting**: Start with Ollama

### Step 2: Get Required Credentials

#### For OpenAI:
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create account and add payment method
3. Generate API key in "API Keys" section
4. Copy key to add-on configuration

#### For Anthropic:
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create account and add payment method
3. Generate API key in "API Keys" section
4. Copy key to add-on configuration

#### For Hailo Models:
1. Follow the [Hailo Package Setup Guide](HAILO_PACKAGE_SETUP.md)
2. Download models from Hailo Model Zoo
3. Place .hef files in `/share/hailo/models/`

### Step 3: Configure and Test
1. **Update** add-on configuration
2. **Restart** the add-on
3. **Test** AI functionality in the web interface
4. **Monitor** logs for any issues

## ❓ Frequently Asked Questions

### Q: Can I use multiple backends simultaneously?
**A:** Not directly, but you can switch backends by changing the configuration and restarting the add-on.

### Q: Will Hailo accelerate OpenAI/Anthropic models?
**A:** No, cloud-based models run on their servers. Hailo only accelerates locally-running models.

### Q: What happens if my API key runs out of credits?
**A:** The add-on will log errors and fall back to monitoring-only mode. Configure multiple backends as backup.

### Q: Can I create custom models for Hailo?
**A:** Yes! Use Hailo's Dataflow Compiler to convert ONNX models to .hef format. See Hailo's documentation.

### Q: Is there a way to automatically switch backends?
**A:** Not yet, but this is planned for future versions. You can manually switch in the configuration.

### Q: Which backend should I start with?
**A:** If you have Hailo hardware and want privacy: start with Hailo. If you want the easiest setup: start with OpenAI.

## 🛠️ Troubleshooting

### Hailo Backend Issues
- **Model not found**: Check .hef files in `/share/hailo/models/`
- **Device not detected**: Verify Hailo hardware installation
- **Out of memory**: Reduce `max_context_length` or try smaller model

### API Backend Issues  
- **Invalid API key**: Verify key and account status
- **Rate limiting**: Check API usage limits
- **Network errors**: Verify internet connectivity

### Performance Issues
- **Slow responses**: Try smaller models or reduce context length
- **High memory usage**: Adjust `max_tokens` and `temperature`
- **Frequent crashes**: Check system resources and model compatibility

---

## 🎯 Recommended Configurations

### **New Users (Easy Start)**
```yaml
ai_backend: "openai"
ai_model: "gpt-3.5-turbo"
openai_api_key: "your-key"
max_context_length: 2048
```

### **Privacy Enthusiasts**
```yaml
ai_backend: "hailo"
ai_model: "llama2-7b-chat"
max_context_length: 4096
```

### **Power Users**
```yaml
ai_backend: "anthropic"
ai_model: "claude-3-opus"
anthropic_api_key: "your-key"
max_context_length: 8192
temperature: 0.8
```

### **Developers**
```yaml
ai_backend: "ollama"
ai_model: "codellama:7b"
custom_api_url: "http://localhost:11434"
max_context_length: 4096
```

Ready to configure your AI backend? Choose the option that best fits your needs and follow the setup steps! 🚀
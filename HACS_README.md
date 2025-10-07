# 🤖 Hailo AI Terminal Add-on Repository

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

![Supports aarch64 Architecture][aarch64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports i386 Architecture][i386-shield]

## About

The **Hailo AI Terminal Add-on** transforms your Home Assistant into an intelligent AI-powered assistant with real-time resource monitoring capabilities. Leveraging Hailo's cutting-edge AI acceleration hardware, this add-on provides:

- 🧠 **AI-Powered Terminal**: Natural language processing for Home Assistant optimization
- 📊 **Real-time Resource Monitoring**: CPU, memory, disk, and Hailo device monitoring
- ⚡ **Local AI Processing**: Fast inference using Hailo-8 hardware acceleration
- 🔧 **Smart Automation Helper**: Intelligent suggestions for YAML configurations
- 🌐 **Web Interface**: Modern, responsive dashboard for AI interactions

## 🚀 Installation

### Prerequisites

**⚠️ Important: Hailo Package Installation Required**

This add-on requires Hailo runtime packages that must be downloaded separately from the [Hailo Developer Zone](https://hailo.ai/developer-zone/). Due to licensing restrictions, these packages cannot be included in this repository.

**📚 COMPREHENSIVE SETUP GUIDE:** [**Complete Hailo Package Setup Guide**](docs/HAILO_PACKAGE_SETUP.md)
- Step-by-step account creation with screenshots
- Detailed download instructions
- Automated verification tools  
- Troubleshooting for common issues
- User-friendly error messages

**Required Hailo Packages:**
- `hailort_*_arm64.deb` - Hailo Runtime
- `hailo_ai_sw_suite_*_arm64.deb` - AI Software Suite  
- `hailo_model_zoo_*_arm64.deb` - Model Zoo
- `hailo_dataflow_compiler_*_arm64.deb` - Dataflow Compiler

**🔍 Quick Verification:** Use the included verification tool to check your packages:
```bash
/share/hailo-terminal-addon/scripts/verify-hailo-packages.sh
```

### Step 1: Add Repository to HACS

1. Open **HACS** in your Home Assistant instance
2. Go to **Integrations** → **⋮** (menu) → **Custom repositories**
3. Add this repository URL: `https://github.com/your-username/hailo-terminal-addon`
4. Select **Category**: `Add-on`
5. Click **Add**

### Step 2: Install the Add-on

1. In HACS, find **"Hailo AI Terminal Add-on Repository"**
2. Click **Download**
3. Restart Home Assistant
4. Go to **Settings** → **Add-ons** → **Add-on Store**
5. Find **"Hailo AI Terminal"** and click **Install**

### Step 3: Setup Hailo Packages

Before starting the add-on, you must install the required Hailo packages:

1. Download packages from [Hailo Developer Zone](https://hailo.ai/developer-zone/)
2. Create directory: `/share/hailo/packages/`
3. Copy all `.deb` files to this directory
4. The add-on will automatically install them on first run

### Step 4: Configure and Start

1. Configure the add-on options:
   ```yaml
   model_path: "/share/hailo/models"
   device_id: "0000:03:00.0"  # Adjust for your Hailo device
   log_level: "info"
   enable_terminal: true
   terminal_port: 8080
   enable_monitoring: true
   ai_model: "hailo-llm-7b"
   ```

2. Start the add-on
3. Access the web interface at `http://your-ha-ip:8080`

## 🔧 Configuration

### Add-on Options

#### AI Backend Configuration
| Option | Description | Default |
|--------|-------------|---------|
| `ai_backend` | AI service to use | `hailo` |
| `ai_model` | Model name (backend-specific) | `llama2-7b-chat` |
| `openai_api_key` | OpenAI API key (if using OpenAI) | `` |
| `anthropic_api_key` | Anthropic API key (if using Claude) | `` |
| `custom_api_url` | Custom API endpoint URL | `` |
| `temperature` | AI response creativity (0.1-2.0) | `0.7` |
| `max_tokens` | Maximum response length | `512` |
| `max_context_length` | Maximum conversation context | `4096` |

#### Hardware & Application Settings
| Option | Description | Default |
|--------|-------------|---------|
| `model_path` | Path to store Hailo models | `/share/hailo/models` |
| `device_id` | Hailo device PCI ID | `0000:03:00.0` |
| `log_level` | Logging level | `info` |
| `enable_terminal` | Enable AI terminal interface | `true` |
| `terminal_port` | Web interface port | `8080` |
| `enable_monitoring` | Enable resource monitoring | `true` |
| `monitor_interval` | Monitoring update interval (seconds) | `5` |

**Supported AI Backends:**
- `hailo` - Local inference with Hailo acceleration (privacy-focused)
- `openai` - GPT models via OpenAI API (requires API key)
- `anthropic` - Claude models via Anthropic API (requires API key)  
- `ollama` - Local open-source models (requires Ollama installation)
- `local` - Custom API endpoints

📖 **[Complete AI Backend Configuration Guide →](docs/AI_BACKEND_GUIDE.md)**

### Hardware Requirements

- **Hailo-8 AI Accelerator**: Required for AI processing
- **ARM64 Architecture**: Recommended (also supports other architectures)
- **4GB RAM**: Minimum for AI model loading
- **10GB Storage**: For models and runtime packages

## 🎯 Features

### 🤖 Flexible AI Backends
- **Hailo Local**: Ultra-fast local inference with Hailo-8 acceleration
- **OpenAI**: GPT-4, GPT-3.5-turbo for best-in-class responses  
- **Anthropic**: Claude-3 models for detailed analysis and coding
- **Ollama**: Free local open-source models (Llama2, Mistral, etc.)
- **Custom APIs**: Connect to your own AI endpoints
- **Easy Switching**: Change backends without reinstalling

### 🧠 AI Terminal
- Natural language queries about your Home Assistant setup
- Intelligent automation suggestions with your choice of AI
- YAML configuration optimization
- Error diagnosis and troubleshooting
- Context-aware conversations that remember your setup

### 📊 Advanced Resource Monitor
- Real-time CPU, memory, and disk usage
- Hailo device temperature and utilization tracking
- Network and I/O statistics with historical trends
- Interactive performance charts and analytics
- Custom monitoring intervals and alerts

### ⚡ Smart Assistance
- Automated entity discovery and organization
- Performance optimization recommendations  
- Security best practices suggestions
- Integration compatibility checks
- Multi-backend AI processing for different use cases

## 🐛 Troubleshooting

### Common Issues

**Add-on won't start:**
- Verify Hailo packages are installed in `/share/hailo/packages/`
- Check device permissions in add-on configuration
- Ensure Hailo device is properly connected

**No AI responses:**
- Confirm AI model is downloaded and accessible
- Check Hailo device status in monitoring dashboard
- Verify model path configuration

**Web interface not accessible:**
- Check port configuration and conflicts
- Verify network connectivity
- Review add-on logs for errors

### Logs and Debugging

Enable debug logging:
```yaml
log_level: "debug"
```

View logs:
```bash
ha addons logs hailo_ai_terminal
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: Hailo packages are subject to their own licensing terms. Please review Hailo's license agreements before use.

## ⭐ Support

If this add-on helps you, please consider giving it a star ⭐

---

## Links

[Hailo Developer Zone]: https://hailo.ai/developer-zone/
[Home Assistant]: https://www.home-assistant.io/
[HACS]: https://hacs.xyz/

<!-- Badges -->
[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/your-username/hailo-terminal-addon.svg
[commits]: https://github.com/your-username/hailo-terminal-addon/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[license-shield]: https://img.shields.io/github/license/your-username/hailo-terminal-addon.svg
[releases-shield]: https://img.shields.io/github/release/your-username/hailo-terminal-addon.svg
[releases]: https://github.com/your-username/hailo-terminal-addon/releases
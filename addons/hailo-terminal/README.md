# 🤖 Hailo AI Terminal for Home Assistant

An intelligent AI-powered terminal and resource monitor that runs directly in your Home Assistant interface, leveraging the power of Hailo-8 AI acceleration for local, private AI assistance.

## 🌟 Features

### 🧠 AI Assistant
- **Natural Language Interface**: Chat with your Home Assistant setup in plain English
- **Configuration Helper**: Get help with YAML configurations and automations
- **Performance Optimization**: AI-powered recommendations for system optimization
- **Local Processing**: All AI runs locally on your Hailo-8 hardware - no cloud needed!

### 📊 Real-Time Monitoring
- **System Resources**: Live CPU, memory, and disk usage monitoring
- **Add-on Tracking**: Monitor resource usage of individual Home Assistant add-ons
- **Visual Dashboard**: Beautiful charts and graphs showing system performance
- **Performance Insights**: AI-powered analysis of resource usage patterns

### 🎯 Smart Features
- **Context Awareness**: Understands your specific Home Assistant configuration
- **Automation Assistance**: Help creating and optimizing automations
- **Troubleshooting**: Diagnose common issues and suggest fixes
- **YAML Validation**: Check configuration syntax and suggest improvements

## 🚀 Installation

### Prerequisites
- Home Assistant with Supervisor
- Hailo-8 AI Hat (or compatible Hailo device)
- ARM64 architecture (Raspberry Pi 4/5 recommended)

### Step 1: Download Hailo Packages
1. Visit the [Hailo Developer Portal](https://hailo.ai/developer-zone/)
2. Download the following packages for ARM64:
   - `hailort_X.X.X_arm64.deb` - Hailo runtime
   - `hailort-X.X.X-cp310-cp310-linux_aarch64.whl` - Python runtime
   - Any AI models you want to use (`.hef` files)

3. Place these files in the `hailo_packages/` directory

### Step 2: Install the Add-on
1. Copy this entire `hailo-terminal` folder to your Home Assistant `addons/` directory
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Refresh the page and find "Hailo AI Terminal"
4. Click **Install**

### Step 3: Configuration
Configure the add-on in the Home Assistant interface:

```yaml
model_path: "/share/hailo/models"      # Where to store AI models
device_id: "0000:03:00.0"             # Hailo device ID
log_level: "info"                      # Logging level
enable_terminal: true                  # Enable web interface
terminal_port: 8080                    # Web interface port
enable_monitoring: true                # Enable resource monitoring
monitor_interval: 5                    # Monitoring update interval (seconds)
ai_model: "hailo-llm-7b"              # AI model to use
max_context_length: 4096              # Maximum context for AI
```

### Step 4: Start the Add-on
1. Click **Start** in the add-on interface
2. Wait for initialization (may take a few minutes on first run)
3. Click **Open Web UI** to access the terminal

## 🎨 User Interface

### Main Interface
- **Left Panel**: AI chat terminal for natural language interaction
- **Right Panel**: Real-time system monitoring and add-on resource usage
- **Interactive Charts**: Live performance graphs
- **Responsive Design**: Works on desktop and mobile

### Example Conversations
```
You: "How can I optimize my Home Assistant performance?"
AI: "I can see your CPU usage is moderate at 15%. Consider disabling unused integrations and using template sensors instead of multiple individual sensors."

You: "Help me create an automation to turn on lights at sunset"
AI: "I'll help you create that automation! Here's a YAML configuration..."

You: "Why is my system using so much memory?"
AI: "Looking at your add-ons, I can see the database addon is using 45% of memory. Consider running database maintenance..."
```

## 🔧 Development

### Architecture
```
hailo-terminal/
├── config.yaml           # Home Assistant add-on configuration
├── Dockerfile            # Container build instructions
├── run.sh                # Startup script
├── requirements.txt      # Python dependencies
├── hailo_packages/       # Hailo runtime and model files
└── src/                  # Application source code
    ├── hailo_terminal.py # Main application
    └── templates/        # Web interface templates
        └── index.html    # Terminal UI
```

### Key Components

#### 1. ResourceMonitor
- Monitors system CPU, memory, disk usage
- Tracks individual add-on resource consumption
- Provides real-time data via WebSocket

#### 2. HailoAIEngine
- Handles AI model loading and inference
- Processes natural language queries
- Maintains conversation context

#### 3. Web Interface
- Flask-based web server with SocketIO
- Real-time communication between frontend and backend
- Beautiful, responsive UI with charts and monitoring

### Extending the Terminal
You can extend the AI capabilities by:

1. **Adding New Models**: Place `.hef` files in `hailo_packages/`
2. **Custom Prompts**: Modify the AI context in `HailoAIEngine`
3. **New Metrics**: Add monitoring for additional system resources
4. **UI Enhancements**: Customize the web interface in `templates/`

## 🤝 Integration with Home Assistant

### API Endpoints
- `GET /api/health` - Add-on health status
- `GET /api/resources` - Current resource usage
- `POST /api/query` - Send AI query

### WebSocket Events
- `ai_query` - Send question to AI
- `ai_response` - Receive AI response
- `resource_update` - Real-time resource updates

### Home Assistant Integration
The terminal can integrate with Home Assistant's:
- **Configuration**: Read and analyze your `configuration.yaml`
- **State API**: Monitor entity states and changes
- **Services**: Help create and optimize service calls
- **Automations**: Analyze and suggest automation improvements

## 📝 Example Use Cases

### 1. Performance Optimization
```
You: "My Home Assistant is slow, what can I do?"
AI: "I see several optimization opportunities:
1. Your recorder is using 2GB - consider purging old data
2. The logbook has 50,000 entries - enable filtering
3. Node-RED addon is using 15% CPU - check for inefficient flows"
```

### 2. Automation Creation
```
You: "Create an automation to turn off all lights when I leave home"
AI: "Here's an automation for that:

automation:
  - alias: 'Lights off when leaving'
    trigger:
      - platform: zone
        entity_id: person.you
        zone: zone.home
        event: leave
    action:
      - service: light.turn_off
        target:
          entity_id: all"
```

### 3. Troubleshooting
```
You: "Why aren't my Zigbee devices responding?"
AI: "Let me check your system:
1. Zigbee coordinator shows 85% link quality - good
2. But I see 15 unavailable entities
3. Try restarting the Zigbee integration
4. Check if devices need battery replacement"
```

## 🔒 Privacy & Security

- **Local Processing**: All AI runs on your Hailo hardware
- **No Cloud Dependencies**: No data sent to external services
- **Secure Communication**: WebSocket connections use authentication
- **Resource Monitoring**: Only accesses system metrics, not personal data

## 🛠️ Troubleshooting

### Common Issues

1. **Hailo Device Not Found**
   - Check device connection: `lsusb` or `lspci`
   - Verify device permissions in Home Assistant

2. **AI Not Responding**
   - Check Hailo model files are in `hailo_packages/`
   - Verify model compatibility with your hardware

3. **High Resource Usage**
   - Adjust `monitor_interval` to reduce polling
   - Lower `max_context_length` for less memory usage

4. **Web Interface Not Loading**
   - Check port conflicts (default 8080)
   - Verify add-on is fully started before accessing UI

## 📚 Resources

- [Hailo Developer Documentation](https://hailo.ai/developer-zone/)
- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
- [Home Assistant API Reference](https://developers.home-assistant.io/docs/api/rest/)

## 🎉 What Makes This Special

This isn't just another Home Assistant add-on - it's like having a **personal Home Assistant expert** available 24/7 that:

1. **Knows Your Setup**: Understands your specific configuration and devices
2. **Learns Over Time**: Builds context from your questions and usage patterns  
3. **Provides Intelligent Insights**: Uses AI to analyze and optimize your system
4. **Respects Privacy**: Everything runs locally on your hardware
5. **Saves Time**: No more searching documentation or forums for answers

## 🚀 Future Enhancements

Planned features for future versions:
- **Voice Interface**: Talk to your Home Assistant
- **Mobile App**: Dedicated mobile interface
- **Advanced Analytics**: Historical performance analysis
- **Custom Models**: Train AI on your specific setup
- **Integration Marketplace**: AI-powered integration recommendations

---

**Ready to revolutionize your Home Assistant experience?** Install the Hailo AI Terminal and experience intelligent, local AI assistance like never before!
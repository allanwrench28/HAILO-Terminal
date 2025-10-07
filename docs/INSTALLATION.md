# Installation Guide: Hailo AI Terminal Add-on

This guide walks you through installing and configuring the Hailo AI Terminal add-on for Home Assistant.

## 📋 Prerequisites

### Hardware Requirements
- ✅ **Hailo-8 AI Accelerator** (Required)
- ✅ **Home Assistant OS** or **Home Assistant Supervised**
- ✅ **4GB+ RAM** (Recommended for AI model loading)
- ✅ **ARM64 Architecture** (Recommended, other architectures supported)

### Software Requirements  
- ✅ **Home Assistant 2023.3.0+**
- ✅ **HACS (Home Assistant Community Store)**
- ✅ **Hailo Developer Account** (for package downloads)

## 🔑 Step 1: Obtain Hailo Packages

**⚠️ Critical**: This add-on requires proprietary Hailo packages that must be downloaded separately.

### 1.1 Register for Hailo Developer Zone
1. Visit [Hailo Developer Zone](https://hailo.ai/developer-zone/)
2. Create a free developer account
3. Complete the registration process

> **📖 Need detailed help?** See the [Complete Hailo Package Setup Guide](HAILO_PACKAGE_SETUP.md) for step-by-step instructions with screenshots and troubleshooting.

### 1.2 Download Required Packages
Navigate to the **Downloads** section and obtain these packages:

**Required Files:**
```
hailort_4.23.0_arm64.deb
hailo_ai_sw_suite_2023.10_arm64.deb  
hailo_model_zoo_2.12.0_arm64.deb
hailo_dataflow_compiler_3.27.0_arm64.deb
```

**Important Notes:**
- Package versions may vary - download the latest compatible versions
- Ensure you select **ARM64** architecture packages
- Save packages to your local computer for transfer

### 1.3 Prepare Package Directory
Create the required directory structure on your Home Assistant system:

```bash
# SSH into your Home Assistant system
ssh root@your-ha-ip

# Create Hailo package directory
mkdir -p /share/hailo/packages

# Set proper permissions
chmod 755 /share/hailo/packages
```

### 1.4 Transfer Packages
Transfer the downloaded `.deb` files to `/share/hailo/packages/`:

**Option A: Using SCP**
```bash
scp *.deb root@your-ha-ip:/share/hailo/packages/
```

**Option B: Using Home Assistant File Editor**
1. Install **File Editor** add-on from official add-on store
2. Navigate to `/share/hailo/packages/`
3. Upload each `.deb` file individually

**Option C: Using SMB/CIFS Share**
1. Enable **Samba** add-on
2. Access `\\your-ha-ip\share\hailo\packages\`
3. Copy files directly via network share

## 🏪 Step 2: Install via HACS

### 2.1 Add Custom Repository
1. Open **HACS** in Home Assistant
2. Click **⋮** (three dots menu) → **Custom repositories**
3. Add repository: `https://github.com/your-username/hailo-terminal-addon`
4. Category: **Add-on**
5. Click **Add**

### 2.2 Install the Add-on Repository
1. Search for **"Hailo AI Terminal"** in HACS
2. Click the repository
3. Click **Download**
4. Wait for download to complete
5. **Restart Home Assistant**

## ⚙️ Step 3: Configure the Add-on

### 3.1 Access Add-on Store
1. Navigate to **Settings** → **Add-ons**
2. Click **Add-on Store** tab
3. Find **"Hailo AI Terminal"**
4. Click **Install**

### 3.2 Choose Your AI Backend

The add-on supports multiple AI backends. Choose based on your preferences:

#### Option A: Hailo Local (Privacy + Performance) 🔒
```yaml
ai_backend: "hailo"
ai_model: "llama2-7b-chat" 
model_path: "/share/hailo/models"
device_id: "0000:03:00.0"
```
**Best for**: Privacy, no internet required, maximum performance

#### Option B: OpenAI (Best Quality) ⭐
```yaml
ai_backend: "openai"
ai_model: "gpt-4"
openai_api_key: "sk-your-api-key-here"
```
**Best for**: Highest quality responses, latest capabilities

#### Option C: Anthropic Claude (Analysis + Coding) 🧠
```yaml
ai_backend: "anthropic"
ai_model: "claude-3-sonnet"
anthropic_api_key: "sk-ant-your-api-key-here"
```
**Best for**: Long conversations, detailed analysis, coding help

#### Option D: Ollama (Free Local Models) 🆓
```yaml
ai_backend: "ollama"
ai_model: "llama2:7b"
custom_api_url: "http://your-ollama-server:11434"
```
**Best for**: Free local models, experimentation

📚 **[Complete AI Backend Guide →](AI_BACKEND_GUIDE.md)** for detailed setup instructions.

### 3.3 Configuration Options
Configure your chosen backend and common settings:

```yaml
# AI Backend (choose one from above)
ai_backend: "hailo"  # or openai, anthropic, ollama, local
ai_model: "llama2-7b-chat"

# API Keys (if using cloud services)
openai_api_key: ""     # For OpenAI backend
anthropic_api_key: ""  # For Anthropic backend

# Hardware Settings (for Hailo backend)
model_path: "/share/hailo/models"
device_id: "0000:03:00.0"  # Check your Hailo PCI ID

# Application Settings
log_level: "info"
enable_terminal: true
terminal_port: 8080
enable_monitoring: true
monitor_interval: 5

# AI Performance Tuning
max_context_length: 4096
temperature: 0.7
max_tokens: 512
```

### 3.3 Find Your Hailo Device ID
To find your Hailo device PCI ID:

```bash
# SSH into Home Assistant
ssh root@your-ha-ip

# List PCI devices
lspci | grep -i hailo

# Expected output:
# 03:00.0 Processing accelerators: Hailo Technologies Ltd. Hailo-8 AI Processor (rev 01)
```
Use the ID from the first column (e.g., `0000:03:00.0`).

## 🚀 Step 4: Start the Add-on

### 4.1 Initial Startup
1. Click **Start** in the add-on interface
2. **Monitor the logs** during first run - this will:
   - Install Hailo packages automatically
   - Initialize AI models
   - Configure the runtime environment

### 4.2 Verify Installation
Check the logs for these success messages:
```
[INFO] Hailo packages installed successfully
[INFO] AI models loaded and ready
[INFO] Web interface started on port 8080
[INFO] Resource monitoring active
```

### 4.3 Access Web Interface
1. Navigate to `http://your-ha-ip:8080`
2. You should see the Hailo AI Terminal dashboard
3. Test AI functionality with a simple query

## 🔧 Step 5: Advanced Configuration

### 5.1 Custom Model Configuration
To use custom AI models:

```yaml
# Custom model path
model_path: "/share/hailo/custom_models"
ai_model: "your-custom-model.hef"

# Performance tuning
max_context_length: 8192  # Increase for longer conversations
```

### 5.2 Network Configuration
For external access:

```yaml
# Enable external access (be cautious with security)
network: "host"
ports:
  8080: 8080
```

### 5.3 Resource Limits
Adjust resource usage:

```yaml
# In add-on configuration
cpu_limit: "2.0"
memory_limit: "4096M"
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### ❌ Add-on Won't Start
**Symptoms:** Add-on stops immediately after starting

**Solutions:**
1. **Check package installation:**
   ```bash
   ls -la /share/hailo/packages/
   ```
   Ensure all 4 `.deb` files are present

2. **Verify Hailo device:**
   ```bash
   lspci | grep -i hailo
   ```
   Device should be detected

3. **Check permissions:**
   ```bash
   chmod -R 755 /share/hailo/
   ```

#### ❌ No AI Responses
**Symptoms:** Terminal loads but AI doesn't respond

**Solutions:**
1. **Check model loading:**
   ```bash
   ha addons logs hailo_ai_terminal | grep -i model
   ```

2. **Verify device access:**
   - Ensure add-on has privileged access
   - Check `/dev/hailo0` permissions

3. **Restart add-on:**
   Sometimes models need a restart to initialize properly

#### ❌ Web Interface Not Accessible
**Symptoms:** Cannot reach `http://your-ha-ip:8080`

**Solutions:**
1. **Check port conflicts:**
   ```bash
   netstat -tlnp | grep 8080
   ```

2. **Verify add-on status:**
   Ensure add-on is running and not crashed

3. **Try different port:**
   ```yaml
   terminal_port: 8081
   ```

#### ❌ High Resource Usage
**Symptoms:** System becomes slow or unresponsive

**Solutions:**
1. **Reduce monitoring frequency:**
   ```yaml
   monitor_interval: 15  # Increase from 5 seconds
   ```

2. **Limit context length:**
   ```yaml
   max_context_length: 2048  # Reduce from 4096
   ```

3. **Disable features temporarily:**
   ```yaml
   enable_monitoring: false  # Disable monitoring
   ```

### Log Analysis
Enable detailed logging for troubleshooting:

```yaml
log_level: "debug"
```

Common log patterns:
- ✅ `[INFO] Hailo device initialized` - Device working
- ❌ `[ERROR] Failed to load model` - Model issue
- ❌ `[ERROR] Package installation failed` - Package problem

## 📞 Getting Help

### Community Support
- **GitHub Issues**: Report bugs and request features
- **Home Assistant Community**: General discussion and help
- **Hailo Community**: Hardware-specific questions

### Logs and Information
When seeking help, provide:
1. Add-on logs: `ha addons logs hailo_ai_terminal`
2. System information: `ha info`
3. Configuration details (redact sensitive information)
4. Steps to reproduce the issue

### Useful Commands
```bash
# Check add-on status
ha addons info hailo_ai_terminal

# View real-time logs  
ha addons logs hailo_ai_terminal --follow

# Restart add-on
ha addons restart hailo_ai_terminal

# Check system resources
ha supervisor stats
```

---

## ✅ Installation Complete!

Your Hailo AI Terminal should now be running. Visit `http://your-ha-ip:8080` to start using your AI-powered Home Assistant assistant!

**Next Steps:**
- Explore the AI terminal with natural language queries
- Set up automation suggestions
- Monitor your system resources
- Customize the AI model for your specific needs

Welcome to the future of Home Assistant management! 🚀
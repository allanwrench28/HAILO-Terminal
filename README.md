# 🤖 Hailo AI Terminal for Home Assistant

**Turn your Home Assistant into an AI-powered automation genius!** 

This add-on gives you a smart AI assistant that can see ALL your devices and help you create automations using plain English.

## ✨ What Does It Do?

- � **AI sees your actual devices** - No more guessing entity names!
- 💬 **Talk to it normally** - "Turn on lights when motion detected"
- 🎯 **Smart suggestions** - Only shows automations that work with your setup
- 🏠 **Works with everything** - Lights, sensors, thermostats, cameras, etc.

## � Super Simple Installation

### Step 1: Do you have Home Assistant?
**Need Home Assistant?** → https://www.home-assistant.io/installation/

### Step 2: Do you have HACS installed?
**Need HACS?** → https://hacs.xyz/docs/setup/download

### Step 3: Install This Add-on

**Easiest Method (HACS - Recommended):**
1. Open HACS in Home Assistant
2. Click the three dots (⋮) → Custom repositories  
3. Paste: `https://github.com/allanwrench28/HAILO-Terminal`
4. Category: Integration
5. Click Add → Install

**Alternative Method (Windows PowerShell):**
1. Press `Windows + R`
2. Type `powershell` and press Enter
3. Copy and paste this, then press Enter:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/allanwrench28/HAILO-Terminal/main/install_clean.ps1" -OutFile "install_hailo.ps1"; .\install_hailo.ps1
```

### Step 4: Configure
1. Go to Settings → Add-ons → Hailo AI Terminal
2. Add your Home Assistant details:
   - **URL**: Your Home Assistant address (like `http://192.168.1.100:8123`)
   - **Token**: [How to get a token →](docs/INSTALLATION.md#getting-your-token)

**📦 Note about AI Packages**: If you want to use Hailo hardware, you'll need to add the Hailo packages to the add-on directory. The add-on works great with OpenAI, Anthropic, or Ollama without any additional packages! [Package setup guide →](docs/HAILO_PACKAGE_SETUP.md)

### Step 5: Start Using It!
1. Open the add-on
2. Type: *"Turn on living room lights when someone walks in"*
3. Watch the magic happen! ✨

## 🎯 What You Can Ask It

- *"Turn on lights when motion detected"*
- *"Schedule my thermostat for energy savings"*  
- *"Create a security system for nighttime"*
- *"Turn everything off when we leave"*
- *"Dim lights gradually at bedtime"*

The AI will suggest automations using your **actual devices** - no more guessing!

## 🆘 Need Help?

**Something not working?** → [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

**Want different AI backends?** → [AI Setup Guide](docs/AI_BACKEND_EXPLAINED.md)

**Manual installation?** → [Detailed Instructions](INSTALLATION_GUIDE.md)

## ⚡ What Makes This Special?

### 🔍 **Smart Entity Discovery**
- Automatically finds ALL your Home Assistant devices
- No more copying and pasting entity names
- AI knows exactly what you have

### 🧠 **Multiple AI Options**
- **Hailo AI** (if you have the hardware)
- **OpenAI** (ChatGPT/GPT-4)
- **Anthropic** (Claude)
- **Ollama** (run AI locally)
- **Custom APIs**

### 💡 **Real Examples of What Users Ask**

> *"Turn on the porch light when someone approaches the front door"*
> 
> **AI Response**: "I found your front door motion sensor and porch light. Here's an automation that triggers the light when motion is detected between sunset and sunrise."

> *"Make my house energy efficient when we're sleeping"*
> 
> **AI Response**: "I found 12 controllable devices. I can turn off non-essential lights, lower the thermostat by 2°F, and put media devices in standby mode from 11 PM to 6 AM."

## 🏆 Why Choose This Over Other AI Tools?

| Feature | This Add-on | ChatGPT/Others |
|---------|-------------|----------------|
| **Knows Your Devices** | ✅ Sees all entities | ❌ Generic suggestions |
| **Works Offline** | ✅ Hailo/Ollama options | ❌ Internet required |
| **Home Assistant Integration** | ✅ Native | ❌ Manual copying |
| **Real Entity Names** | ✅ Uses actual IDs | ❌ Placeholder names |
| **Installation Testing** | ✅ Automated validation | ❌ Trial and error |

## 🛠️ For Developers

Want to customize or contribute? All the technical details are here:

- **[Developer Documentation →](docs/addon-development-guide.md)**
- **[Technical Implementation →](ENTITY_DISCOVERY_COMPLETE.md)**
- **[API Documentation →](docs/HAILO_PACKAGE_SETUP.md)**
- **[Contributing Guide →](CONTRIBUTING.md)**

## 📈 What's Next?

This add-on is actively developed with planned features:

- 🔮 **Predictive Automations** - Learn your patterns
- 📱 **Mobile App Integration** - Voice control
- 🏠 **Room-by-Room Setup** - Area-specific intelligence
- 🔄 **Automation Templates** - Share community automations

---

**🌟 Star this repo if it helps you!** 

**🐛 Found a bug?** → [Report it here](https://github.com/allanwrench28/HAILO-Terminal/issues)

**💡 Have an idea?** → [Share it here](https://github.com/allanwrench28/HAILO-Terminal/discussions)

## 📝 License

This workspace template is provided as-is for Home Assistant and Hailo AI development.

---

**Happy Developing!** 🎉

Build amazing AI-powered Home Assistant add-ons with Hailo acceleration!
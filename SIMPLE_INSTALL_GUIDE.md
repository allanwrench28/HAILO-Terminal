# 🚀 Hailo AI Terminal - Simple Installation Guide

## ✨ 5 Easy Steps to Install

This guide walks you through the easiest way to install the Hailo AI Terminal add-on for Home Assistant.

---

## 📦 Step 1: Download Hailo Packages

1. **Visit** [Hailo Developer Zone](https://hailo.ai/developer-zone/)
2. **Create** a free developer account (or login if you have one)
3. **Navigate** to the Downloads section
4. **Download** these 4 packages (ARM64 versions):
   - ✅ `hailort_*_arm64.deb` - Hailo Runtime
   - ✅ `hailo_ai_sw_suite_*_arm64.deb` - AI Software Suite
   - ✅ `hailo_model_zoo_*_arm64.deb` - Model Zoo
   - ✅ `hailo_dataflow_compiler_*_arm64.deb` - Dataflow Compiler

5. **Save** all files to your computer (remember where you saved them!)

> **💡 Tip**: Keep all 4 files in the same folder on your computer for easy access.

---

## 🔌 Step 2: Install Samba (If You Don't Have It)

Samba lets you easily transfer files to Home Assistant from Windows.

### 2.1 Check if you already have Samba:
1. Open **Home Assistant** in your browser
2. Go to **Settings** → **Add-ons**
3. Look for **"Samba share"** in your installed add-ons
4. ✅ If you see it and it's running, skip to **Step 3**

### 2.2 If you don't have Samba, install it:
1. In Home Assistant, go to **Settings** → **Add-ons** → **Add-on Store**
2. Search for **"Samba share"**
3. Click on **"Samba share"** by Home Assistant Community Add-ons
4. Click **INSTALL** (wait 1-2 minutes)
5. Click **START**
6. Click the **Configuration** tab
7. Set a username and password (write them down!)
8. Click **SAVE** → **RESTART**

**Example configuration:**
```yaml
username: homeassistant
password: yourpassword
```

---

## 📁 Step 3: Place Hailo Packages in Add-ons Folder

Now you'll copy the Hailo packages to Home Assistant using Samba.

### 3.1 Connect to Home Assistant from Windows:
1. Open **Windows File Explorer** (Windows Key + E)
2. In the address bar, type: `\\YOUR-HA-IP-ADDRESS`
   - Replace `YOUR-HA-IP-ADDRESS` with your actual IP (like `\\192.168.1.100`)
3. Press **Enter**
4. When prompted, enter:
   - **Username**: `homeassistant` (or what you set)
   - **Password**: Your Samba password
   - Check ✅ **"Remember my credentials"**
5. Click **OK**

### 3.2 Copy the Hailo packages:
1. You should now see Home Assistant folders: `addons`, `config`, `share`, etc.
2. Open the **`addons`** folder
3. **Copy** all 4 Hailo packages (.deb files) you downloaded in Step 1
4. **Paste** them directly into the `addons` folder

> **💡 Important**: Place the `.deb` files directly in the `addons` folder, not in a subfolder!

**Your files should look like this:**
```
\\YOUR-HA-IP\addons\
├── hailort_4.23.0_arm64.deb
├── hailo_ai_sw_suite_2023.10_arm64.deb
├── hailo_model_zoo_2.12.0_arm64.deb
└── hailo_dataflow_compiler_3.27.0_arm64.deb
```

---

## 🏪 Step 4: Add the Add-on Repository

Now you'll tell Home Assistant where to find the Hailo AI Terminal add-on.

1. Open **Home Assistant** in your browser
2. Navigate to **Settings** → **Add-ons** → **Add-on Store**
3. Click the **⋮** (three dots menu) in the top right corner
4. Click **Repositories**
5. In the text box, paste this URL:
   ```
   https://github.com/allanwrench28/HAILO-Terminal
   ```
6. Click **ADD**
7. Click **CLOSE**

> **✅ Success!** The repository is now added to your Home Assistant.

---

## 🎯 Step 5: Install the Add-on

Finally, install the Hailo AI Terminal add-on!

1. **Refresh** the Add-on Store page (or close and reopen it)
2. Scroll down to find **"Hailo AI Terminal"** in the list
3. Click on **Hailo AI Terminal**
4. Click **INSTALL** (this may take 5-10 minutes)
5. Wait for installation to complete

### What happens during installation:
- ✅ The add-on automatically finds your Hailo packages in the `addons` folder
- ✅ Packages are copied to the add-on's internal directory
- ✅ Hailo drivers and libraries are installed
- ✅ Everything is configured and ready to use!

> **📋 Note**: You'll see messages in the log about finding and installing Hailo packages. This is normal!

---

## 🎉 You're Done!

The Hailo AI Terminal is now installed and ready to use!

### Next Steps:

1. **Configure the add-on**:
   - Click on the **Configuration** tab
   - Choose your AI backend (Hailo, OpenAI, Anthropic, or Ollama)
   - Add API keys if using OpenAI or Anthropic

2. **Start the add-on**:
   - Click **START**
   - Wait for it to show **RUNNING**

3. **Check the logs**:
   - Click the **Log** tab
   - You should see: "Hailo packages copied" and "Hailo device found"

---

## 🆘 Troubleshooting

### Issue: "No Hailo packages found"
**Solution**: 
- Make sure you placed the `.deb` files in the `addons` folder, not a subfolder
- Check that all 4 files have the `.deb` extension
- Restart the add-on after copying files

### Issue: "Hailo device not found"
**Solution**:
- Check that your Hailo-8 hardware is properly connected
- Verify the add-on has privileged access enabled
- Check device with command: `ls /dev/hailo*`

### Issue: "Can't connect to Samba"
**Solution**:
- Verify Samba add-on is running
- Check you're using the correct IP address
- Try restarting the Samba add-on

---

## 💡 Key Points

- ✅ **Simple**: Just 5 steps, no command line needed
- ✅ **Automatic**: Add-on finds and installs Hailo packages for you
- ✅ **Works Without Hailo**: Even without packages, you can use OpenAI, Anthropic, or Ollama
- ✅ **Clean**: Packages are automatically managed by the add-on

---

**Need more help?** 
- 📖 [Detailed Installation Guide](docs/INSTALLATION.md)
- 🔧 [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- 💬 [GitHub Issues](https://github.com/allanwrench28/HAILO-Terminal/issues)

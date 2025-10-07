# 🚀 Hailo AI Terminal - Simple Installation Guide

## ✨ 5 Easy Steps to Install

This guide walks you through the easiest way to install the Hailo AI Terminal add-on for Home Assistant.

---

## 📦 Step 1: Download Hailo Packages

### 1.1 Visit Hailo Developer Zone

1. **Visit** [Hailo Developer Zone](https://hailo.ai/developer-zone/)
2. **Create** a free developer account (or login if you have one)
3. **Navigate** to the Downloads section

### 1.2 Download These EXACT 4 Packages

**⚠️ IMPORTANT: Download the ARM64 versions of these specific packages:**

| # | Package Name | What to Look For | Example Filename |
|---|--------------|-----------------|------------------|
| 1️⃣ | **HailoRT Runtime** | File starting with `hailort_` and ending with `_arm64.deb` | `hailort_4.28.0_arm64.deb` |
| 2️⃣ | **AI Software Suite** | File starting with `hailo_ai_sw_suite_` and ending with `_arm64.deb` | `hailo_ai_sw_suite_2024.04_arm64.deb` |
| 3️⃣ | **Model Zoo** | File starting with `hailo_model_zoo_` and ending with `_arm64.deb` | `hailo_model_zoo_2.15.0_arm64.deb` |
| 4️⃣ | **Dataflow Compiler** | File starting with `hailo_dataflow_compiler_` and ending with `_arm64.deb` | `hailo_dataflow_compiler_3.35.0_arm64.deb` |

**Version Notes:**
- ✅ **Use the LATEST versions** available on the site (versions shown above are examples)
- ✅ **Minimum versions**: HailoRT 4.23.0+, AI Suite 2023.10+, Model Zoo 2.12.0+, Compiler 3.27.0+
- ❌ **DO NOT download**: Files with `amd64`, `x86_64`, or `i386` in the name
- ❌ **DO NOT download**: Files with `.whl` extension (Python wheels) - we only need `.deb` files

### 1.3 How to Identify the Correct Files

**Each filename MUST contain ALL of these:**
- ✅ The package name at the start (e.g., `hailort_`)
- ✅ A version number (e.g., `4.28.0`)
- ✅ The text `arm64` (NOT amd64 or x86_64)
- ✅ The extension `.deb`

**Examples of CORRECT filenames:**
```
✅ hailort_4.28.0_arm64.deb
✅ hailo_ai_sw_suite_2024.04_arm64.deb
✅ hailo_model_zoo_2.15.0_arm64.deb
✅ hailo_dataflow_compiler_3.35.0_arm64.deb
```

**Examples of INCORRECT filenames (do NOT download these):**
```
❌ hailort_4.28.0_amd64.deb          (wrong architecture)
❌ hailort-4.28.0-cp310-linux.whl    (wrong format - .whl instead of .deb)
❌ hailo_platform_2.10.0_arm64.deb   (wrong package - platform instead of ai_sw_suite)
❌ hailort_3.20.0_arm64.deb          (too old - need 4.23.0+)
```

### 1.4 Save the Files

5. **Save** all 4 `.deb` files to your computer (remember where you saved them!)
6. **Keep them together** in the same folder for easy access

> **💡 Tip**: Create a folder on your Desktop called `hailo-packages` and save all 4 files there.

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

**Your files should look like this (version numbers may vary):**
```
\\YOUR-HA-IP\addons\
├── hailort_4.28.0_arm64.deb
├── hailo_ai_sw_suite_2024.04_arm64.deb
├── hailo_model_zoo_2.15.0_arm64.deb
└── hailo_dataflow_compiler_3.35.0_arm64.deb
```

> **📝 Note**: Your version numbers might be different - that's OK! Just make sure each file has `arm64` and `.deb` in the name.

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

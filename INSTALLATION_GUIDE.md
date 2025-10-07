# 🚀 HAILO AI TERMINAL - FOOLPROOF INSTALLATION GUIDE

## ⚡ **SUPER QUICK INSTALL (3 MINUTES)**

### 📋 **WHAT YOU NEED:**
- ✅ Home Assistant OS running (any device)
- ✅ Windows computer connected to same network
- ✅ 5 minutes of your time

---

## 🎯 **STEP-BY-STEP INSTALLATION**

### **STEP 1: GET YOUR HOME ASSISTANT TOKEN** (30 seconds)

1. **Open your web browser** (Chrome, Firefox, Edge)
2. **Go to:** `http://YOUR_HOME_ASSISTANT_IP:8123`
   - Replace `YOUR_HOME_ASSISTANT_IP` with your actual IP (like `192.168.0.143`)
3. **Click your profile icon** (bottom left corner)
4. **Scroll down** to "Long-lived access tokens"
5. **Click "CREATE TOKEN"**
6. **Give it a name:** "Hailo AI Terminal"
7. **Copy the token** (long string of letters/numbers)
8. **Save it** somewhere safe - you'll need it!

### **STEP 2: DOWNLOAD & RUN INSTALLER** (1 minute)

1. **Download** the installation files:
   - Right-click this link: [Download Hailo AI Terminal](https://github.com/your-repo/hailo-terminal/archive/main.zip)
   - Select "Save link as..." 
   - Save to your **Desktop**

2. **Extract the files:**
   - Right-click the downloaded ZIP file
   - Select "Extract All..."
   - Extract to **Desktop**

3. **Open PowerShell as Administrator:**
   - Press **Windows Key + X**
   - Click **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**
   - If it asks "Do you want to allow this app to make changes?" click **YES**

4. **Navigate to the downloaded folder:**
   ```powershell
   cd C:\Users\%USERNAME%\Desktop\hailo-terminal-main
   ```

5. **Run the installer:**
   ```powershell
   .\install.ps1 -HomeAssistantIP 192.168.0.143 -HAToken YOUR_TOKEN_HERE
   ```
   - Replace `192.168.0.143` with **your actual Home Assistant IP**
   - Replace `YOUR_TOKEN_HERE` with **your token from Step 1**

### **STEP 3: UPLOAD TO HOME ASSISTANT** (2 minutes)

The installer will create files. Now upload them:

#### **METHOD A: SAMBA UPLOAD (RECOMMENDED - EASIEST)**

1. **Install Samba in Home Assistant:**
   - Open Home Assistant web interface
   - Go to **Settings → Add-ons → Add-on Store**
   - Search for **"Samba share"**
   - Click **Install** then **Start**

2. **Open Windows File Explorer:**
   - Press **Windows Key + E**
   - In the address bar, type: `\\YOUR_HOME_ASSISTANT_IP`
   - Press **Enter**
   - Enter your Home Assistant username/password when prompted

3. **Upload the add-on:**
   - Double-click the **"addons"** folder
   - Right-click in empty space → **New → Folder**
   - Name it: **"hailo-terminal"**
   - Double-click the **"hailo-terminal"** folder you just created
   - Go back to your Desktop
   - Open the **"hailo-terminal-addon"** folder created by the installer
   - **Select ALL files** (Ctrl+A)
   - **Copy** them (Ctrl+C)
   - Go back to the Samba window
   - **Paste** them (Ctrl+V) into the hailo-terminal folder

### **STEP 4: INSTALL THE ADD-ON** (1 minute)

1. **Restart Home Assistant:**
   - Go to **Settings → System → Restart**
   - Wait for restart (about 30 seconds)

2. **Install the add-on:**
   - Go to **Settings → Add-ons**
   - You should see **"Hailo AI Terminal"** in the list
   - Click on it
   - Click **"Install"**
   - Wait for installation (1-2 minutes)

3. **Start the add-on:**
   - Click **"Start"**
   - Wait for it to turn green
   - Click **"Open Web UI"**

### **STEP 5: ENJOY YOUR AI ASSISTANT!** 🎉

- The AI Terminal will open in a new tab
- Start chatting with your AI assistant
- Try: "Turn on lights when motion detected"
- Watch it create automations using your actual devices!

---

## 🆘 **TROUBLESHOOTING**

### **"PowerShell won't run the script"**
**Fix:** Run this first in PowerShell (as Admin):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **"Can't connect to \\YOUR_HOME_ASSISTANT_IP"**
**Fix:** 
1. Make sure Samba add-on is installed and started
2. Try the IP address with http:// first: `http://192.168.0.143:8123`
3. Use your Home Assistant login credentials

### **"Add-on not showing up"**
**Fix:**
1. Make sure files are in `/addons/hailo-terminal/` folder
2. Restart Home Assistant: Settings → System → Restart
3. Refresh the Add-ons page

### **"Token doesn't work"**
**Fix:**
1. Create a new token in Home Assistant
2. Make sure you copied the entire token (it's very long)
3. Don't use quotes around the token in the command

---

## 🏆 **HACS INSTALLATION (ALTERNATIVE - EASIER)**

### **When Available on HACS:**

1. **Install HACS** (if not already installed):
   - Follow: https://hacs.xyz/docs/setup/download

2. **Add Custom Repository:**
   - HACS → Integrations → ⋮ (menu) → Custom repositories
   - Repository: `https://github.com/your-repo/hailo-terminal`
   - Type: Integration

3. **Install:**
   - Search for "Hailo AI Terminal"
   - Click Install
   - Restart Home Assistant

**Note:** HACS version is coming soon! For now, use the manual installation above.

---

## ❓ **NEED HELP?**

### **Common Questions:**

**Q: What's my Home Assistant IP?**
**A:** Check your router's admin page, or use an IP scanner app

**Q: Where do I get the token?**
**A:** Home Assistant → Profile → Long-lived access tokens → Create Token

**Q: Which PowerShell should I use?**
**A:** Windows PowerShell (the blue one) as Administrator

**Q: Can I install this on a different computer?**
**A:** Yes! Just make sure it can reach your Home Assistant network

### **Still Stuck?**
- Check the logs in Home Assistant: Settings → Add-ons → Hailo AI Terminal → Log
- Make sure your Home Assistant can access the internet
- Verify your token hasn't expired

---

## 🎯 **WHAT YOU GET AFTER INSTALLATION:**

✅ **AI Chat Interface** - Talk to your smart home
✅ **Smart Automation Builder** - "Turn on lights when motion detected"  
✅ **Entity Discovery** - AI sees all your devices automatically
✅ **Multi-AI Backend** - Hailo, OpenAI, Claude, Ollama support
✅ **Modern UI** - Beautiful, responsive interface
✅ **Real-time Monitoring** - System stats and performance
✅ **Automation Intelligence** - AI recommends based on your setup

**🚀 Your Home Assistant just got 10x smarter!**
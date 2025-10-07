# 📁 SAMBA UPLOAD GUIDE - Upload Hailo AI Terminal to Home Assistant

## 🎯 **WHAT THIS DOES:**
Upload your Hailo AI Terminal add-on files to Home Assistant using Windows file sharing (no command line needed!)

---

## 📋 **PREREQUISITES:**

✅ **Home Assistant OS** running on your network  
✅ **Windows computer** on same network  
✅ **Samba add-on** installed in Home Assistant  
✅ **Hailo AI Terminal files** prepared (from installer)  

---

## 🚀 **STEP-BY-STEP SAMBA UPLOAD**

### **STEP 1: INSTALL SAMBA ADD-ON** (1 minute)

1. **Open Home Assistant** in your web browser:
   - Go to: `http://YOUR_HOME_ASSISTANT_IP:8123`
   - Replace `YOUR_HOME_ASSISTANT_IP` with your actual IP

2. **Navigate to Add-ons:**
   - Click **Settings** (gear icon, bottom left)
   - Click **Add-ons**
   - Click **Add-on Store** (bottom right)

3. **Install Samba:**
   - In the search box, type: **"Samba share"**
   - Click on **"Samba share"** (by Home Assistant Community Add-ons)
   - Click **"INSTALL"** (wait 1-2 minutes)
   - Click **"START"**
   - Wait for it to show **"RUNNING"**

### **STEP 2: CONFIGURE SAMBA** (30 seconds)

1. **In the Samba add-on page:**
   - Click the **"Configuration"** tab
   - Set a username and password (remember these!)
   - Click **"SAVE"**
   - Click **"RESTART"**

Example configuration:
```yaml
workgroup: WORKGROUP
username: homeassistant
password: yourpassword
interface: ""
allow_hosts:
  - 10.0.0.0/8
  - 172.16.0.0/12
  - 192.168.0.0/16
  - fe80::/10
veto_files:
  - "._*"
  - ".DS_Store"
  - Thumbs.db
compatibility_mode: false
```

### **STEP 3: CONNECT FROM WINDOWS** (1 minute)

1. **Open Windows File Explorer:**
   - Press **Windows Key + E**
   - Or click the folder icon in taskbar

2. **Connect to Home Assistant:**
   - Click in the address bar at the top
   - Type: `\\YOUR_HOME_ASSISTANT_IP`
   - Replace `YOUR_HOME_ASSISTANT_IP` with your actual IP (like `\\192.168.0.143`)
   - Press **Enter**

3. **Enter credentials when prompted:**
   - Username: `homeassistant` (or whatever you set)
   - Password: `yourpassword` (or whatever you set)
   - Check **"Remember my credentials"**
   - Click **OK**

### **STEP 4: CREATE ADDON FOLDER** (30 seconds)

1. **You should now see Home Assistant folders:**
   - `addons` ← This is where we're going!
   - `backup`
   - `config`
   - `share`
   - `ssl`

2. **Open the addons folder:**
   - Double-click **"addons"**

3. **Create Hailo Terminal folder:**
   - Right-click in empty space
   - Select **New → Folder**
   - Name it exactly: **"hailo-terminal"**
   - Press Enter

### **STEP 5: UPLOAD HAILO FILES** (2 minutes)

1. **Open your Hailo AI Terminal files:**
   - On your Desktop, find the **"hailo-terminal-addon"** folder
   - This was created by the installer script
   - Double-click to open it

2. **Select all files:**
   - Press **Ctrl + A** (select all)
   - You should see files like:
     - `config.yaml`
     - `Dockerfile`
     - `README.md`
     - `src` folder
     - etc.

3. **Copy the files:**
   - Press **Ctrl + C** (copy)

4. **Paste into Home Assistant:**
   - Go back to the File Explorer window with Home Assistant
   - Make sure you're inside the **"hailo-terminal"** folder you created
   - Press **Ctrl + V** (paste)
   - Wait for files to copy (30 seconds to 2 minutes)

### **STEP 6: RESTART & INSTALL** (2 minutes)

1. **Restart Home Assistant:**
   - Go back to Home Assistant web interface
   - Click **Settings → System**
   - Click **"RESTART"** (big red button)
   - Wait for restart (30-60 seconds)

2. **Install the add-on:**
   - Go to **Settings → Add-ons**
   - You should see **"Hailo AI Terminal"** in the list
   - Click on it
   - Click **"INSTALL"**
   - Wait for installation (2-5 minutes)

3. **Start the add-on:**
   - Click **"START"**
   - Wait for it to show **"RUNNING"**
   - Click **"OPEN WEB UI"**

---

## ✅ **SUCCESS!**

If everything worked, you should see the Hailo AI Terminal interface open in a new tab!

---

## 🆘 **TROUBLESHOOTING**

### **Can't connect to `\\YOUR_HOME_ASSISTANT_IP`**

**Try these fixes:**

1. **Check Samba is running:**
   - Home Assistant → Settings → Add-ons → Samba share
   - Should show **"RUNNING"** in green

2. **Try different connection methods:**
   - Instead of `\\192.168.0.143`, try:
   - `\\homeassistant.local`
   - `\\homeassistant`

3. **Use Map Network Drive:**
   - In File Explorer, click **"Computer"** → **"Map network drive"**
   - Drive letter: Choose any (like Z:)
   - Folder: `\\YOUR_HOME_ASSISTANT_IP\addons`
   - Check **"Connect using different credentials"**
   - Enter your Samba username/password

### **Files won't copy**

**Possible causes:**

1. **Samba not configured properly:**
   - Check username/password in Samba configuration
   - Make sure you clicked "SAVE" and "RESTART"

2. **Permissions issue:**
   - Try copying files one at a time
   - Make sure you're in the right folder (`addons/hailo-terminal/`)

3. **Network timeout:**
   - Files are large, be patient
   - Try copying smaller batches

### **Add-on doesn't appear**

1. **Check folder structure:**
   ```
   addons/
   └── hailo-terminal/
       ├── config.yaml
       ├── Dockerfile
       ├── README.md
       └── src/
           ├── hailo_terminal.py
           ├── ai_backend_manager.py
           └── ... (other files)
   ```

2. **Restart Home Assistant:**
   - Settings → System → Restart

3. **Check logs:**
   - Settings → System → Logs
   - Look for any error messages about add-ons

---

## 🎉 **ALTERNATIVE: USB UPLOAD**

If Samba doesn't work, you can also:

1. **Copy files to USB drive**
2. **Plug USB into Home Assistant device**
3. **Use SSH to copy files** (advanced users)

---

## 💡 **PRO TIPS:**

- **Keep Samba running** - It's useful for editing config files later
- **Bookmark the network path** - `\\YOUR_HOME_ASSISTANT_IP` for quick access
- **Create desktop shortcut** - Right-click the Samba connection → "Create shortcut"

**🚀 You're all set! Enjoy your AI-powered Home Assistant!**
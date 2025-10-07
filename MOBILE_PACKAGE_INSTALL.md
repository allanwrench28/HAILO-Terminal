# 📱 Mobile Package Installation Guide for Hailo AI Terminal

## 🎯 **The Challenge**
You've got your Hailo packages (`.hef`, `.deb`, `.whl` files) on your phone and need to get them into your Home Assistant add-on directory. Here are the easiest mobile-friendly methods:

## 📁 **Where Packages Need to Go**
```
/config/addons/hailo-terminal/hailo_packages/
├── your_model.hef
├── hailort_4.23.0_arm64.deb  
├── hailort-4.23.0-cp310-cp310-linux_aarch64.whl
└── hailo_platform-4.23.0-cp310-cp310-linux_aarch64.whl
```

## 📱 **Mobile Installation Methods**

### **Method 1: Home Assistant Mobile App File Upload** ⭐ **EASIEST**

**Requirements**: Home Assistant Mobile App + File Manager access

1. **Download packages to your phone** from Hailo Developer Portal
2. **Open Home Assistant Mobile App**
3. **Go to**: Settings → Add-ons → Hailo AI Terminal → Configuration
4. **Look for**: File upload section or browse button
5. **Upload each package file** to the add-on directory

*Note: This method depends on the add-on having a file upload interface*

### **Method 2: Samba Share Upload** ⭐ **MOST RELIABLE**

**Requirements**: Samba add-on installed on Home Assistant

**Setup Samba (one-time):**
1. **Install Samba add-on** in Home Assistant
2. **Configure username/password** in Samba settings
3. **Start the Samba add-on**

**Upload from mobile:**
1. **Download packages** to your phone
2. **Open file manager** on your phone
3. **Connect to network location**: `\\YOUR-HA-IP\config`
4. **Navigate to**: `addons/hailo-terminal/hailo_packages/`
5. **Copy/paste** all package files

**Mobile apps that work well:**
- **Android**: ES File Explorer, Solid Explorer, Total Commander
- **iOS**: Files app (supports SMB), Documents by Readdle

### **Method 3: Cloud Storage Bridge** 📤 **UNIVERSAL**

**Requirements**: Cloud storage app + Home Assistant File Editor add-on

**Process:**
1. **Upload packages** to cloud storage (Google Drive, Dropbox, OneDrive)
2. **Access Home Assistant** web interface on mobile
3. **Install File Editor add-on** if not already installed
4. **Use File Editor** to create temporary download directory
5. **Download packages** from cloud storage to HA
6. **Move files** to correct add-on directory

### **Method 4: Terminal SSH Upload** 🖥️ **FOR TECH USERS**

**Requirements**: SSH access + terminal app on mobile

**Mobile SSH apps:**
- **Android**: Termux, JuiceSSH, ConnectBot
- **iOS**: Termius, Blink Shell, SSH Files

**Process:**
1. **Upload packages** to cloud storage first
2. **SSH into Home Assistant** from mobile terminal
3. **Download packages** using `wget` or `curl`
4. **Move to correct directory**:
```bash
cd /config/addons/hailo-terminal/hailo_packages/
wget "https://your-cloud-link/package.hef"
```

### **Method 5: USB-C Direct Transfer** 🔌 **ANDROID ONLY**

**Requirements**: Android phone + USB-C to USB-A adapter + USB drive

**Process:**
1. **Download packages** to phone
2. **Copy to USB drive** using phone
3. **Plug USB into Home Assistant device**
4. **Use File Editor** to copy from USB to add-on directory

## 🎯 **Recommended Workflow**

### **For Most Users** (Samba Method):
```
1. Set up Samba add-on (one-time, 5 minutes)
2. Download Hailo packages to mobile device
3. Use phone's built-in file manager to connect to \\HA-IP\config
4. Navigate to addons/hailo-terminal/hailo_packages/
5. Upload all package files
6. Restart Hailo AI Terminal add-on
```

### **For Quick One-Time Setup** (Cloud Storage):
```
1. Upload packages to Google Drive/Dropbox from mobile
2. Access Home Assistant web interface
3. Use File Editor add-on to download from cloud
4. Move files to correct add-on directory
```

## 📋 **Step-by-Step: Samba Method (Most Popular)**

### **Setup (One-Time)**
1. **Home Assistant** → Add-ons → Add-on Store
2. **Search**: "Samba share"
3. **Install** → **Configuration**:
   ```yaml
   workgroup: WORKGROUP
   username: hauser
   password: your-secure-password
   interface: ""
   allow_hosts:
     - 10.0.0.0/8
     - 172.16.0.0/12
     - 192.168.0.0/16
   ```
4. **Start** the add-on

### **Upload Packages**
1. **Download Hailo packages** to your phone
2. **Open file manager** (Files app on iOS, any file manager on Android)
3. **Add network location**: `\\YOUR-HA-IP\config`
4. **Enter credentials**: username/password from Samba setup
5. **Navigate**: `addons` → `hailo-terminal` → `hailo_packages`
6. **Upload all files** (drag/drop or copy/paste)

### **Verify & Restart**
1. **Home Assistant** → Settings → Add-ons → Hailo AI Terminal
2. **Check logs** to see if packages are detected
3. **Restart add-on** if needed

## ⚠️ **Common Mobile Issues**

### **File Manager Can't Connect**
- **Check IP address**: Use Home Assistant local IP (192.168.x.x)
- **Try different app**: Some mobile file managers work better than others
- **Check Samba settings**: Make sure allow_hosts includes your network

### **Packages Not Detected**
- **Check file names**: Must match exact Hailo naming convention
- **Check permissions**: Files should be readable by Home Assistant
- **Check directory**: Must be in `hailo_packages/` folder exactly

### **Upload Fails**
- **File too large**: Some mobile browsers limit upload size
- **Use smaller batches**: Upload one file at a time
- **Try different method**: Switch to cloud storage bridge method

## 🎉 **Success Indicators**

**You'll know it worked when:**
- ✅ Add-on logs show "Hailo packages detected"
- ✅ Add-on configuration shows Hailo backend available
- ✅ AI responses include "Hailo hardware detected"

## 💡 **Pro Tips**

1. **Download packages on WiFi** - They can be large files
2. **Use descriptive filenames** - Helps identify models later  
3. **Keep backup copies** - Store packages in cloud storage too
4. **Test with one model first** - Verify setup before uploading all packages
5. **Check add-on logs** - They'll tell you if packages are found and working

**The Samba method is usually the easiest for most users - it turns your Home Assistant into a network drive that any mobile device can access!** 📱➡️🏠
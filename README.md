# Home Assistant Hailo AI Add-on Development Workspace

Welcome to your complete development environment for building custom Home Assistant add-ons with Hailo AI integration!

## 🚀 Quick Start

### 🤖 Understanding AI Backends
**New to AI hardware?** The Hailo-8 is an AI accelerator that works with multiple AI backends for maximum flexibility.

📖 **[AI Backends Explained Simply →](docs/AI_BACKEND_EXPLAINED.md)** - Perfect for understanding how it all works!

### Generate Your First Add-on
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Generate a new add-on
./scripts/generate-addon.sh my-hailo-detector

# Or use the dev helper
./scripts/dev-helper.sh generate my-hailo-detector
```

### Build and Test
```bash
# Build the add-on
./scripts/build-addon.sh ./addons/my-hailo-detector

# Validate configuration
./scripts/dev-helper.sh validate ./addons/my-hailo-detector

# Verify Hailo packages
./scripts/verify-hailo-packages.sh
```

## 📁 Workspace Structure

```
├── addons/                 # Your custom add-ons
├── templates/             # Add-on templates
│   └── hailo-base-addon/  # Base Hailo add-on template
├── scripts/               # Development tools
│   ├── generate-addon.sh  # Generate new add-on
│   ├── build-addon.sh     # Build add-on
│   └── dev-helper.sh      # Development helper
├── docs/                  # Documentation
└── .github/              # Workspace configuration
```

## 🛠️ Development Tools

### Generate Add-on
Create a new add-on from the Hailo template:
```bash
./scripts/generate-addon.sh [OPTIONS] ADDON_NAME

Options:
  -d, --description DESC  Add-on description
  -v, --version VERSION   Initial version (default: 1.0.0)
  -a, --author AUTHOR     Add-on author
  --url URL              Repository URL
```

### Build Add-on
Build your add-on for Home Assistant:
```bash
./scripts/build-addon.sh [OPTIONS] ADDON_PATH

Options:
  -a, --arch ARCH         Target architecture (default: aarch64)
  -v, --version VERSION   Add-on version
  -n, --name NAME         Add-on name
  --no-cache             Build without cache
```

### Development Helper
All-in-one development tool:
```bash
./scripts/dev-helper.sh COMMAND [OPTIONS]

Commands:
  generate ADDON_NAME     Generate new add-on
  build ADDON_PATH        Build an add-on
  list                    List all add-ons
  clean                   Clean build artifacts
  validate ADDON_PATH     Validate add-on configuration
```

## 🧠 Hailo Integration

### Required Packages
Place these files from the Hailo Developer Portal in your add-on's `hailo_packages/` directory:

- **HEF Models**: `*.hef` files (Hailo Executable Format)
- **Runtime**: `hailort_*_arm64.deb` (system package)
- **Python SDK**: `hailort-*-cp*-linux_aarch64.whl`
- **Platform**: `hailo_platform-*-cp*-linux_aarch64.whl`

### Example Structure
```
addons/my-detector/hailo_packages/
├── yolov8s.hef
├── yolov8m.hef
├── hailort_4.23.0_arm64.deb
├── hailort-4.23.0-cp310-cp310-linux_aarch64.whl
└── hailo_platform-4.23.0-cp310-cp310-linux_aarch64.whl
```

## 🏗️ Add-on Template Features

The base template includes:

### Configuration (`config.yaml`)
- Multi-architecture support
- Device mapping for Hailo hardware
- Configurable options (model path, device ID, API settings)
- Proper Home Assistant integration

### Dockerfile
- Ubuntu 22.04 base with proper package management
- S6-Overlay for proper process management
- Bashio for Home Assistant integration
- Architecture-aware Hailo package installation

### Application (`src/main.py`)
- Flask API server for inference
- Model loading and management
- Device detection and initialization
- Comprehensive logging
- Health check endpoints

### API Endpoints
- `GET /health` - System health check
- `GET /models` - List available models
- `POST /inference` - Run model inference

## 🚀 Deployment Workflow

### 1. Development
```bash
# Generate add-on
./scripts/generate-addon.sh my-app

# Add Hailo packages
cp /path/to/hailo/packages/* ./addons/my-app/hailo_packages/

# Customize application
edit ./addons/my-app/src/main.py
```

### 2. Testing
```bash
# Validate configuration
./scripts/dev-helper.sh validate ./addons/my-app

# Build locally
./scripts/build-addon.sh ./addons/my-app

# Test run (if Hailo device available)
docker run --rm -it --device=/dev/hailo0 local/aarch64-addon-my_app:1.0.0
```

### 3. Home Assistant Installation
```bash
# Copy to Home Assistant
cp -r ./addons/my-app /path/to/homeassistant/addons/

# Install through Home Assistant UI
# Settings → Add-ons → Add-on Store → Local Add-ons
```

## 🎯 Use Cases

### Object Detection
```python
# Example: YOLOv8 object detection
def run_detection(image_path, model_name):
    model = load_hailo_model(f"{MODEL_PATH}/{model_name}.hef")
    image = preprocess_image(image_path)
    results = model.infer(image)
    return postprocess_results(results)
```

### Audio Processing
```python
# Example: Whisper speech recognition
def transcribe_audio(audio_path, model_name):
    model = load_hailo_model(f"{MODEL_PATH}/{model_name}.hef")
    audio = preprocess_audio(audio_path)
    transcript = model.infer(audio)
    return transcript
```

### Custom Models
```python
# Example: Custom trained model
def run_custom_inference(input_data, model_name):
    model = load_hailo_model(f"{MODEL_PATH}/{model_name}.hef")
    preprocessed = custom_preprocess(input_data)
    results = model.infer(preprocessed)
    return custom_postprocess(results)
```

## 📖 Documentation

- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
- [Hailo Developer Portal](https://hailo.ai/developer-zone/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🤝 Contributing

1. Create your add-on using the template
2. Test thoroughly on actual hardware
3. Document your configuration and usage
4. Share your innovations!

## 📝 License

This workspace template is provided as-is for Home Assistant and Hailo AI development.

---

**Happy Developing!** 🎉

Build amazing AI-powered Home Assistant add-ons with Hailo acceleration!
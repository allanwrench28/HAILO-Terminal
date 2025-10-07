# Hailo AI Hardware Integration Guide

This guide covers integrating Hailo AI accelerators with Home Assistant add-ons.

## Hardware Requirements

### Supported Hailo Devices
- **Hailo-8**: M.2 A+E key form factor
- **Hailo-8L**: M.2 A+E key form factor  
- **Hailo-15**: High-performance variant
- **Compatible development boards**

### System Requirements
- **Architecture**: ARM64 (aarch64) primary, AMD64 supported
- **OS**: Home Assistant OS, Home Assistant Supervised
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: 32GB+ for models and applications

## Device Setup

### Physical Installation
1. **Power down** your Home Assistant system
2. **Install Hailo card** in M.2 slot (A+E key)
3. **Secure with screw** if provided
4. **Power up** and verify detection

### Verify Device Detection
```bash
# SSH into Home Assistant
# Check if device is detected
lspci | grep Hailo

# Check device node
ls -la /dev/hailo*

# Verify permissions (should show crw-rw-rw-)
ls -la /dev/hailo0
```

### Device Permissions
If device permissions are incorrect:
```bash
# Fix permissions (temporary)
chmod 666 /dev/hailo0

# Or add udev rule (persistent)
echo 'KERNEL=="hailo[0-9]*", MODE="0666"' > /etc/udev/rules.d/99-hailo.rules
udevadm control --reload-rules
```

## Software Setup

### Hailo Runtime Installation
The add-on template automatically handles:
- HailoRT library installation
- Python SDK setup
- Device driver configuration

### Package Management
```bash
# Packages are installed during container build:
# 1. System package: hailort_X.X.X_arm64.deb
# 2. Python wheel: hailort-X.X.X-cp310-cp310-linux_aarch64.whl
# 3. Platform SDK: hailo_platform-X.X.X-cp310-cp310-linux_aarch64.whl
```

## Model Management

### HEF Model Format
Hailo models use the **HEF (Hailo Executable Format)**:
- Optimized for Hailo hardware
- Includes quantization and compilation
- Single file per model

### Model Organization
```
/share/hailo/models/
├── detection/
│   ├── yolov8s.hef
│   ├── yolov8m.hef
│   └── yolov8l.hef
├── classification/
│   ├── resnet50.hef
│   └── efficientnet.hef
└── custom/
    └── my_model.hef
```

### Model Loading Example
```python
import hailo_platform as hailo

class HailoModelManager:
    def __init__(self, device_id="0000:03:00.0"):
        self.device = hailo.Device(device_id)
        self.models = {}
    
    def load_model(self, model_path):
        """Load HEF model file."""
        try:
            hef = hailo.HEF(model_path)
            network_group = self.device.configure(hef)
            model_name = hef.get_network_groups()[0].get_name()
            
            self.models[model_name] = {
                'hef': hef,
                'network_group': network_group,
                'input_streams': network_group.get_input_streams(),
                'output_streams': network_group.get_output_streams()
            }
            
            return model_name
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_path}: {e}")
    
    def get_model_info(self, model_name):
        """Get model input/output specifications."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not loaded")
        
        model = self.models[model_name]
        
        input_info = []
        for stream in model['input_streams']:
            info = stream.get_info()
            input_info.append({
                'name': info.name,
                'shape': info.shape,
                'format': str(info.format)
            })
        
        output_info = []
        for stream in model['output_streams']:
            info = stream.get_info()
            output_info.append({
                'name': info.name,
                'shape': info.shape,
                'format': str(info.format)
            })
        
        return {
            'inputs': input_info,
            'outputs': output_info
        }
```

## Performance Optimization

### Batch Processing
```python
def run_batch_inference(model_manager, model_name, batch_data):
    """Run inference on multiple inputs efficiently."""
    model = model_manager.models[model_name]
    network_group = model['network_group']
    
    # Configure batch size
    batch_size = len(batch_data)
    
    with network_group.activate() as activated_network:
        # Prepare input tensors
        input_tensors = {}
        for i, stream in enumerate(model['input_streams']):
            input_tensors[stream.get_info().name] = batch_data
        
        # Run inference
        results = activated_network.infer(input_tensors)
        
        return results
```

### Memory Management
```python
class HailoInferenceManager:
    def __init__(self, max_concurrent=4):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_inference_async(self, model, input_data):
        """Run inference with concurrency control."""
        async with self.semaphore:
            return await self._run_inference(model, input_data)
    
    async def _run_inference(self, model, input_data):
        # Actual inference implementation
        pass
```

## Troubleshooting

### Common Issues

#### Device Not Detected
```bash
# Check PCI devices
lspci | grep -i hailo

# Check kernel messages
dmesg | grep -i hailo

# Verify driver loading
lsmod | grep hailo
```

#### Permission Denied
```bash
# Check device permissions
ls -la /dev/hailo0

# Fix permissions
sudo chmod 666 /dev/hailo0

# Or add user to hailo group (if exists)
sudo usermod -a -G hailo $USER
```

#### Memory Issues
```bash
# Check available memory
free -h

# Monitor memory usage during inference
watch -n 1 'free -h && ps aux --sort=-%mem | head -10'
```

#### Performance Issues
```python
# Monitor inference timing
import time

def benchmark_model(model_manager, model_name, test_data, iterations=100):
    """Benchmark model inference performance."""
    times = []
    
    for i in range(iterations):
        start_time = time.perf_counter()
        result = model_manager.infer(model_name, test_data)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    avg_time = sum(times) / len(times)
    fps = 1.0 / avg_time
    
    print(f"Average inference time: {avg_time*1000:.2f}ms")
    print(f"Average FPS: {fps:.2f}")
    
    return {
        'avg_time_ms': avg_time * 1000,
        'fps': fps,
        'min_time_ms': min(times) * 1000,
        'max_time_ms': max(times) * 1000
    }
```

### Debug Mode
Enable debug logging in your add-on:
```python
import logging

# Set debug level
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Enable Hailo debug logs
os.environ['HAILO_LOG_LEVEL'] = 'debug'
```

### Health Checks
```python
def health_check():
    """Comprehensive system health check."""
    checks = {
        'device_available': os.path.exists('/dev/hailo0'),
        'device_accessible': os.access('/dev/hailo0', os.R_OK | os.W_OK),
        'memory_available': psutil.virtual_memory().available > 1024**3,  # 1GB
        'models_loaded': len(model_manager.models) > 0
    }
    
    return {
        'healthy': all(checks.values()),
        'checks': checks
    }
```

## Best Practices

### Model Organization
- Use descriptive model names
- Organize by use case (detection, classification, etc.)
- Version your models
- Document model requirements and performance

### Resource Management
- Implement proper cleanup in your applications
- Use connection pooling for high-throughput scenarios
- Monitor memory usage and implement limits
- Handle device disconnection gracefully

### Error Handling
```python
def safe_inference(model_manager, model_name, input_data):
    """Safe inference with comprehensive error handling."""
    try:
        # Validate inputs
        if not model_manager.is_model_loaded(model_name):
            raise ValueError(f"Model {model_name} not loaded")
        
        # Check device availability
        if not model_manager.is_device_available():
            raise RuntimeError("Hailo device not available")
        
        # Run inference
        result = model_manager.infer(model_name, input_data)
        
        return {
            'success': True,
            'result': result,
            'model': model_name
        }
        
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        return {
            'success': False,
            'error': str(e),
            'model': model_name
        }
```

This hardware integration guide should help you successfully deploy Hailo AI accelerators in your Home Assistant add-ons!
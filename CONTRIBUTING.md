# Contributing to Hailo AI Terminal Add-on

Thank you for your interest in contributing! This guide will help you get started.

## 🔧 Development Setup

### Prerequisites
- **Docker** installed and running
- **Git** for version control  
- **Home Assistant** test environment
- **Hailo Developer Account** for testing packages

### Clone and Setup
```bash
git clone https://github.com/your-username/hailo-terminal-addon.git
cd hailo-terminal-addon

# Make scripts executable
chmod +x scripts/*.sh

# Generate development environment
./scripts/dev-helper.sh setup
```

## 🏗️ Building and Testing

### Local Development Build
```bash
# Build for your architecture
./scripts/build-addon.sh ./addons/hailo-terminal

# Test configuration validation
./scripts/dev-helper.sh validate ./addons/hailo-terminal

# Run linting
./scripts/dev-helper.sh lint
```

### Testing with Home Assistant
1. Copy the addon to your Home Assistant addons directory
2. Install required Hailo packages in `/share/hailo/packages/`
3. Install and test the addon through the UI

## 📝 Code Standards

### Python Code
- **PEP 8** compliance required
- **Type hints** for all functions
- **Docstrings** for classes and methods
- **Error handling** with proper logging

Example:
```python
def monitor_resources(self, interval: int = 5) -> Dict[str, Any]:
    """Monitor system resources at specified interval.
    
    Args:
        interval: Monitoring interval in seconds
        
    Returns:
        Dictionary containing resource metrics
        
    Raises:
        ResourceMonitorError: If monitoring fails
    """
```

### Configuration Files
- **YAML** validation required
- **Schema** compliance for all options
- **Documentation** for all configuration parameters

### Docker
- **Multi-architecture** support required
- **Security** best practices
- **Minimal** image sizes where possible

## 🧪 Testing Guidelines

### Unit Tests
```bash
# Run Python unit tests
./scripts/test.sh unit

# Run with coverage
./scripts/test.sh coverage
```

### Integration Tests
```bash
# Test addon installation
./scripts/test.sh integration

# Test with real Hailo hardware (if available)
./scripts/test.sh hardware
```

### Manual Testing Checklist
- [ ] Add-on installs successfully
- [ ] Web interface loads correctly
- [ ] AI responses work as expected
- [ ] Resource monitoring displays data
- [ ] Configuration changes apply properly
- [ ] Logs are clear and informative

## 📋 Pull Request Process

### Before Submitting
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m "Add amazing feature"`
4. **Test** thoroughly using the checklist above
5. **Push** to branch: `git push origin feature/amazing-feature`

### Pull Request Requirements
- [ ] **Description** explains what and why
- [ ] **Tests** pass (automated and manual)
- [ ] **Documentation** updated if needed
- [ ] **Changelog** entry added
- [ ] **Screenshots** for UI changes

### Review Process
1. **Automated** checks must pass
2. **Code review** by maintainers
3. **Testing** on real hardware when possible
4. **Approval** and merge

## 🐛 Bug Reports

### Good Bug Reports Include
- **Environment** details (HA version, architecture, etc.)
- **Steps** to reproduce the issue
- **Expected** vs **actual** behavior
- **Logs** and error messages
- **Screenshots** if applicable

### Use This Template
```markdown
**Environment:**
- Home Assistant version: 
- Add-on version:
- Architecture:
- Hailo device:

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**

**Actual Behavior:**

**Logs:**
```

## 💡 Feature Requests

### Good Feature Requests Include
- **Problem** statement - what issue does this solve?
- **Proposed** solution - how should it work?
- **Alternatives** considered - what other options exist?
- **Additional** context - mockups, examples, etc.

## 🏷️ Release Process

### Version Numbering
We use **Semantic Versioning** (semver.org):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps
1. **Update** version in `config.yaml`
2. **Update** `CHANGELOG.md`
3. **Create** release PR
4. **Tag** release: `git tag v1.2.3`
5. **Push** tag: `git push origin v1.2.3`
6. **GitHub** automatically creates release

## 📚 Documentation

### What Needs Documentation
- **New features** and configuration options
- **API changes** and breaking changes
- **Installation** and setup procedures
- **Troubleshooting** guides

### Documentation Standards
- **Clear** and concise language
- **Examples** for complex concepts
- **Screenshots** for UI elements
- **Links** to related resources

## 🤝 Community Guidelines

### Be Respectful
- **Patient** with new contributors
- **Constructive** feedback only
- **Inclusive** language and behavior

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code review and discussion

## 🆘 Getting Help

### Development Questions
- Check existing **GitHub Issues**
- Review **documentation** and **code comments**
- Ask in **GitHub Discussions**

### Contact Maintainers
- **@mention** in issues or PRs
- **Email** for security issues: security@your-domain.com

## 📄 License

By contributing, you agree that your contributions will be licensed under the same **MIT License** that covers the project.

---

Thank you for contributing to the Hailo AI Terminal Add-on! 🚀
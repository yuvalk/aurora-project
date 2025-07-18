# Contributing to Aurora Borealis Toolkit

Thank you for your interest in contributing to the Aurora Borealis Toolkit! This project aims to make aurora science accessible and enjoyable for everyone.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Use clear, descriptive titles
- Include steps to reproduce the issue
- Provide your system information (OS, Python version)
- Share expected vs actual behavior

### 🎯 Feature Requests
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity
- Think about backward compatibility

### 💻 Code Contributions
- Follow Python PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write tests for new functionality
- Update documentation as needed

### 📚 Documentation
- Fix typos and grammatical errors
- Improve clarity and examples
- Add missing documentation
- Translate to other languages

## 🔧 Development Setup

1. **Clone the repository**:
   ```bash
   git clone [repository-url]
   cd aurora-project
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

## 🎨 Code Style

- Use **4 spaces** for indentation
- Maximum line length: **88 characters**
- Use meaningful variable names
- Follow the existing code patterns
- Add comments for complex logic

### Example Code Style:
```python
def calculate_aurora_probability(
    location: str, 
    kp_index: float, 
    magnetic_latitude: float
) -> float:
    """
    Calculate the probability of aurora visibility at a given location.
    
    Args:
        location: Name of the location
        kp_index: Current KP index value (0-9)
        magnetic_latitude: Magnetic latitude of the location
        
    Returns:
        Probability percentage (0-100)
    """
    # Calculate threshold based on KP index
    threshold_lat = 67 - (kp_index * 2.5)
    
    if magnetic_latitude >= threshold_lat:
        return min(95, (magnetic_latitude - threshold_lat + 5) * 10)
    else:
        return max(0, (magnetic_latitude - threshold_lat + 10) * 2)
```

## 🧪 Testing

- Write unit tests for all new functions
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests focused and independent

### Example Test:
```python
def test_aurora_probability_calculation():
    """Test aurora probability calculation with various inputs."""
    # Test high latitude, high KP
    prob = calculate_aurora_probability("Fairbanks", 6.0, 65.1)
    assert prob > 80
    
    # Test low latitude, low KP
    prob = calculate_aurora_probability("Seattle", 2.0, 54.2)
    assert prob < 20
```

## 📋 Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the style guidelines
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

### Pull Request Template:
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🌐 Priority Areas

We're especially looking for help with:

1. **Real-time data integration** - Connect to NOAA/ESA APIs
2. **Mobile responsiveness** - Web interface for mobile devices
3. **International locations** - Add more global viewing locations
4. **Advanced visualizations** - Interactive maps and charts
5. **Performance optimization** - Faster data processing
6. **Accessibility** - Screen reader support, keyboard navigation
7. **Translations** - Multi-language support

## 📞 Getting Help

- **Issues**: Create a GitHub issue for questions
- **Discussions**: Use GitHub Discussions for broader topics
- **Documentation**: Check the README and docs folder
- **Examples**: Look at existing code for patterns

## 🎯 Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Celebrate diverse perspectives

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributor section
- Release notes for significant contributions
- Special mentions for innovative features

Thank you for helping make aurora science accessible to everyone! 🌌✨
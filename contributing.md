# Contributing to Universal Integer System

First off, thank you for considering contributing to Universal Integer System! 🎉

## Code of Conduct

Be kind, be respectful. We're all here to make distributed systems better.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Code examples if applicable
- Your environment (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- Include code examples of how it might work

### Adding New Integer Codes

The beauty of this system is that it grows with the community! To add new codes:

1. Choose the appropriate range for your codes
2. Create a new IntEnum class in the relevant module
3. Follow the existing naming conventions
4. Document the purpose of each code
5. Add tests for your new codes

Example:
```python
class CloudProviderEvent(IntEnum):
    """Cloud provider specific events - Range: 3700-3799"""
    
    INSTANCE_LAUNCHED = 3700
    INSTANCE_STOPPED = 3701
    INSTANCE_TERMINATED = 3702
    SCALING_TRIGGERED = 3703
    # ... more events
```

## Development Process

1. **Fork the repo** and create your branch from `main`
2. **Set up your development environment:**
   ```bash
   git clone https://github.com/yourusername/universal-integer-system
   cd universal-integer-system
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e ".[dev]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

3. **Make your changes:**
   - Write code that follows the existing style
   - Add tests for new functionality
   - Update documentation as needed

4. **Run the test suite:**
   ```bash
   # Run tests
   pytest
   
   # Run with coverage
   pytest --cov=universal_integer_system
   
   # Run linters
   black src/ tests/
   ruff check src/ tests/
   mypy src/
   ```

5. **Commit your changes:**
   - Use clear and meaningful commit messages
   - Reference any related issues

6. **Push to your fork** and submit a pull request

## Pull Request Guidelines

- Include a description of what your PR does
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused - one feature/fix per PR

## Style Guide

### Python Style

We use Black for formatting and Ruff for linting. The pre-commit hooks will handle this automatically, but you can also run manually:

```bash
black src/ tests/
ruff check src/ tests/
```

### Code Conventions

- Use descriptive variable names
- Add type hints for all functions
- Document all public APIs
- Keep functions focused and small
- Follow the existing patterns in the codebase

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Testing

- Write tests for all new functionality
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use pytest fixtures for reusable test components

Example test:
```python
def test_new_code_translation():
    """Test that new codes translate correctly."""
    assert translate_code(3700) == "instance.launched"
    assert get_system_for_code(3700) == "deployment"
```

## Documentation

- Update the README if adding major features
- Add docstrings to all public functions/classes
- Include usage examples in docstrings
- Update architecture docs for structural changes

## Questions?

Feel free to open an issue with your question or reach out in the discussions section.

Thank you for contributing! 🚀
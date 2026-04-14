# Contributing to artty

Thank you for your interest in contributing! This guide will help you get set up and productive.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- pip (latest version recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/divisionseven/artty.git
cd artty
```

### 2. Create a Virtual Environment

```bash
# Using venv
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode along with all development tools:
- pytest (testing)
- pytest-cov (coverage)
- ruff (linting and formatting)
- mypy (type checking)

## Running Tests

Run the full test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run tests with coverage report:

```bash
pytest --cov=artty --cov-report=html
```

Run a specific test file:

```bash
pytest tests/test_converter.py
```

## Code Style Requirements

This project uses **ruff** for linting and formatting, and **mypy** for type checking.

### Linting

```bash
ruff check src/
```

### Formatting

```bash
ruff format src/
```

Check formatting without applying changes:

```bash
ruff format --check src/
```

### Type Checking

```bash
mypy src/
```

### Pre-commit Hooks (Recommended)

To ensure code quality before each commit, install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

This will run ruff and mypy on staged files before each commit.

## Submitting Pull Requests

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow the code style guidelines (ruff + mypy)
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

Before submitting, ensure all checks pass:

```bash
ruff check src/
ruff format --check src/
mypy src/
pytest
```

### 4. Commit Your Changes

Write clear, descriptive commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git add .
git commit -m "feat: add new feature X"
# or
git commit -m "fix: resolve issue with Y"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what you changed and why
- Reference to any related issues

## Code Conventions

- **Type hints**: All function parameters and return values must be typed
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Line length**: Maximum 88 characters (ruff default)
- **Imports**: Organize as Standard library → Third-party → Local, alphabetically within groups

## Questions?

If you have questions, feel free to open an issue for discussion before starting work.
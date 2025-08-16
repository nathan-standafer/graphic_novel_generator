












# Contributing Guide

Thank you for considering contributing to the Graphic Novel Video Creator project! We welcome contributions from everyone. This document provides guidelines for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

Please read and follow our [Code of Conduct](https://github.com/user/graphic_novel/blob/main/CODE_OF_CONDUCT.md). We expect all contributors to adhere to these guidelines.

## How Can I Contribute?

### Reporting Bugs

1. Check if the issue already exists in the [issue tracker](https://github.com/user/graphic_novel/issues)
2. If not, create a new issue with:
   - A clear title and description
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Screenshots or error messages (if applicable)

### Suggesting Enhancements

1. Check if a similar enhancement has been suggested before
2. Create a new issue with:
   - A clear title and description of the feature
   - Why it would be useful
   - Any specific implementation details you have in mind

### Pull Requests

1. Fork the repository and create your branch from `main`
2. Make sure your changes follow our [code style guidelines](#code-style-guidelines)
3. Write tests for your changes (if applicable)
4. Update documentation if needed
5. Create a pull request with:
   - A clear title and description of what your change does
   - Why the change is necessary
   - Any relevant issue numbers

## Development Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/user/graphic_novel.git
   cd graphic_novel
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks**:

   ```bash
   pre-commit install
   ```

5. **Set up WhisperSpeech model**:

   ```bash
   python -m whisperspeech.download --model collabora/whisperspeech:s2a-q4-base-en+pl.model
   ```

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use descriptive variable and function names
- Write docstrings for public functions and classes
- Keep lines under 80 characters when possible
- Use consistent indentation (4 spaces)

### Linting and Formatting

We use the following tools to maintain code quality:

- **Black**: Code formatter
- **Flake8**: Linter
- **isort**: Import sorter
- **Pre-commit**: Automated code quality checks

Run these manually with:

```bash
black .
flake8 .
isort .
pre-commit run --all-files
```

## Testing

We use [pytest](https://pytest.org/) for testing. To run tests:

```bash
pytest
```

Please add tests for any new functionality you implement.

## Documentation

Documentation is important! Please update the README and other documentation files whenever you make changes that affect how users interact with the project.

### Building Documentation

To build the documentation locally:

1. Install mkdocs and dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. Build and serve the docs:

   ```bash
   mkdocs serve
   ```

3. Open your browser to `http://localhost:8000` to view the documentation

## Thank You!

We appreciate your contributions to making Graphic Novel Video Creator better! 🎬📚✨











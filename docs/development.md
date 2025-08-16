











# Development Guide

Thank you for considering contributing to the Graphic Novel Video Creator project! This guide provides information for developers working on the project.

## Code Structure

```
graphic_novel/
├── source_text/              # Original book files
├── source_text_chunked/      # Chapter-by-chapter text files
├── generated_prompts/        # AI-generated image prompts
├── generated_illustrations/  # Generated scene illustrations
├── generated_audio/          # Narration audio and subtitles
├── create_video.py           # Video assembly script
├── generate_audio_and_srt.py # Audio and subtitle generation
├── generate_prompts.py       # Prompt generation pipeline
└── recreate_chapter_1_video.sh # End-to-end video creation script
```

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

## Contributing

Please read our [CONTRIBUTING.md](https://github.com/user/graphic_novel/blob/main/CONTRIBUTING.md) for detailed guidelines on contributing to this project.

### Pull Request Process

1. Fork the repository and create your branch from `main`
2. Make sure your changes follow our code style guidelines
3. Write tests for your changes (if applicable)
4. Update documentation if needed
5. Create a pull request with:
   - A clear title and description of what your change does
   - Why the change is necessary
   - Any relevant issue numbers

## CI/CD Pipeline

We use GitHub Actions for continuous integration:

- **Python application**: Runs on push and pull request to `main` branch
- **Linting**: Checks code style with flake8
- **Testing**: Runs pytest suite

You can view the workflow configuration in [.github/workflows/python-app.yml](https://github.com/user/graphic_novel/blob/main/.github/workflows/python-app.yml).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/user/graphic_novel/blob/main/LICENSE) file for details.











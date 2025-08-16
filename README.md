



# Graphic Novel Video Creator

[![Graphic Novel Video Creator](https://img.shields.io/badge/Graphic%20Novel-Video%20Creator-blue?style=for-the-badge&logo=github)](https://github.com/user/graphic_novel)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Powered-orange?style=for-the-badge)](https://github.com/user/graphic_novel)

**Transform classic literature into immersive, narrated video experiences with professional illustrations and synchronized subtitles.**

## 🎬 Features

- **Automated Illustration Generation**: Creates high-quality, moody oil painting style illustrations for each scene
- **Professional Narration**: Uses advanced TTS (Text-to-Speech) technology with WhisperSpeech for natural-sounding audio
- **Synchronized Subtitles**: Automatically generates and burns-in accurate subtitles using WhisperX
- **Seamless Video Production**: Automates the entire video creation pipeline from text to final video
- **Chapter-by-Chapter Processing**: Handles long-form content by processing chapters individually

## 📚 Supported Input

The system currently processes classic literature in plain text format. The included example uses:
- **Moby Dick by Herman Melville** (135 chapters, ~200,000 words)

## 🎨 Technology Stack

- **Text Processing**: Python with NLTK for natural language processing
- **AI Illustration Generation**: ComfyUI with stable diffusion models
- **Audio Generation**: WhisperSpeech TTS pipeline
- **Subtitle Generation**: WhisperX with large-v2 model
- **Video Production**: FFmpeg and HandBrakeCLI for professional video encoding

## 🚀 Getting Started

### Quick Demo

Want to see the pipeline in action? Try our demo script:

```bash
python demo.py
```

This will create a simple test video using placeholder content.

### Prerequisites

1. Python 3.8+
2. Conda or virtualenv for dependency management
3. GPU recommended for illustration generation and audio processing
4. Local LLM server (e.g., openai/gpt-oss-20b) for prompt generation

### Installation

```bash
# Clone the repository
git clone https://github.com/user/graphic_novel.git
cd graphic_novel

# Install dependencies
pip install -r requirements.txt

# Set up WhisperSpeech model
python -m whisperspeech.download --model collabora/whisperspeech:s2a-q4-base-en+pl.model
```

### Usage

1. **Prepare your text**: Place your book in `source_text/` and chunk it into chapters in `source_text_chunked/`
2. **Generate prompts**: Run the prompt generation pipeline
   ```bash
   python generate_prompts.py
   ```
3. **Create illustrations**: Use ComfyUI with the provided workflow to generate images
4. **Generate audio and subtitles**:
   ```bash
   python generate_audio_and_srt.py
   ```
5. **Assemble the video**:
   ```bash
   bash recreate_chapter_1_video.sh
   ```

## 📈 Pipeline Overview

1. **Text Processing**: Split chapters into scenes and generate descriptive prompts
2. **Illustration Generation**: Create moody oil painting style images for each scene
3. **Audio Narration**: Generate natural-sounding speech with WhisperSpeech
4. **Subtitle Synchronization**: Align subtitles with audio using WhisperX
5. **Video Assembly**: Combine illustrations, audio, and subtitles into a professional video

## 🎥 Sample Output

The included example processes the first chapter of Moby Dick:

- [Chapter 1 Video](chapter_001_with_subs.mp4)
- [Generated Illustrations](generated_illustrations/chapter_001/)
- [Narration Audio](generated_audio/chapter_001.wav)
- [Subtitle File](generated_audio/chapter_001.srt)

## 🛠 Development

### Directory Structure

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

### Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and send pull requests.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- **Herman Melville** for the classic literature that inspired this project
- The open-source community for providing amazing tools like FFmpeg, WhisperSpeech, and ComfyUI
- All contributors who have helped improve this project

---

**Transform your favorite books into engaging video experiences with Graphic Novel Video Creator!** 🎬📚✨




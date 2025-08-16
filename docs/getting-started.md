










# Getting Started

This guide will help you set up and run the Graphic Novel Video Creator on your local machine.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8+
- Conda or virtualenv for dependency management
- GPU recommended for illustration generation and audio processing
- Local LLM server (e.g., openai/gpt-oss-20b) for prompt generation

## Quick Demo

Want to see the pipeline in action? Try our demo script:

```bash
python demo.py
```

This will create a simple test video using placeholder content.

## Installation

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
   ```

4. **Set up WhisperSpeech model**:

   ```bash
   python -m whisperspeech.download --model collabora/whisperspeech:s2a-q4-base-en+pl.model
   ```

## Running the Pipeline

1. **Prepare your text**: Place your book in `source_text/` and chunk it into chapters in `source_text_chunked/`

2. **Generate prompts**:

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

## Troubleshooting

- If you encounter GPU issues, try setting `CUDA_VISIBLE_DEVICES=0` before running commands
- For audio generation problems, ensure your WhisperSpeech model is properly downloaded
- Check the [issues page](https://github.com/user/graphic_novel/issues) for common problems and solutions









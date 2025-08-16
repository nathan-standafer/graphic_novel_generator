











# Usage Guide

This guide provides step-by-step instructions for using the Graphic Novel Video Creator pipeline.

## Preparing Your Text

1. **Place your book in `source_text/`**: The system currently processes classic literature in plain text format.

2. **Chunk into chapters**: Create individual chapter files in `source_text_chunked/`. Each file should contain one chapter of your book.

3. **Naming convention**: Use descriptive filenames like `chapter_001.txt`, `chapter_002.txt`, etc.

## Generating Prompts

Run the prompt generation pipeline to create AI prompts for illustration generation:

```bash
python generate_prompts.py
```

This will analyze your text and generate descriptive prompts in the `generated_prompts/` directory.

## Creating Illustrations

Use ComfyUI with the provided workflow to generate illustrations:

1. Open ComfyUI and load the provided workflow file
2. Set the input prompt directory to `generated_prompts/`
3. Configure output settings to save images in `generated_illustrations/`
4. Run the workflow to generate images for each scene

## Generating Audio and Subtitles

Run the audio generation script:

```bash
python generate_audio_and_srt.py
```

This will:
- Generate narration audio files using WhisperSpeech TTS pipeline
- Create subtitle files (.srt) using WhisperX with large-v2 model
- Save outputs in the `generated_audio/` directory

## Assembling the Video

Run the video assembly script:

```bash
bash recreate_chapter_1_video.sh
```

This will:
- Combine illustrations, audio, and subtitles into a professional video
- Use FFmpeg for high-quality video encoding
- Output the final video file (e.g., `chapter_001_with_subs.mp4`)

## Customizing the Pipeline

### Illustration Styles

To change illustration styles:
1. Modify the prompt generation script (`generate_prompts.py`)
2. Adjust ComfyUI workflow settings
3. Experiment with different stable diffusion models

### Audio Settings

To customize audio:
1. Edit the `generate_audio_and_srt.py` script
2. Change voice, speed, or volume parameters
3. Test different WhisperSpeech models

### Subtitle Appearance

To modify subtitles:
1. Update subtitle generation settings in `generate_audio_and_srt.py`
2. Adjust font, size, position, or color preferences
3. Test with different WhisperX configurations

## Troubleshooting

- **GPU Issues**: Try setting `CUDA_VISIBLE_DEVICES=0` before running commands
- **Audio Problems**: Ensure your WhisperSpeech model is properly downloaded
- **Video Errors**: Check FFmpeg installation and dependencies
- **Common Solutions**: See the [issues page](https://github.com/user/graphic_novel/issues) for troubleshooting tips










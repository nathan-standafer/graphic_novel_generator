

#!/bin/bash
# Full pipeline script for Graphic Novel Video Creator

echo "Starting Graphic Novel Video Creator pipeline..."

# Step 1: Generate prompts from text
echo "1. Generating image prompts..."
python generate_prompts.py

# Step 2: Generate audio and subtitles (this requires WhisperSpeech setup)
echo "2. Generating audio and subtitles..."
python generate_audio_and_srt.py

# Step 3: Create video (assumes illustrations are already generated)
echo "3. Creating video..."
python create_video.py
bash run_ffmpeg.sh

# Step 4: Burn subtitles into video
echo "4. Burning subtitles into final video..."
HandBrakeCLI -i chapter_001.mp4 -o chapter_001_with_subs.mp4 --srt-file generated_audio/chapter_001.srt --srt-burn

# Clean up
rm chapter_001.mp4

echo "Pipeline complete! Final video: chapter_001_with_subs.mp4"


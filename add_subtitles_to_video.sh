#!/bin/bash

# This script recreates the video for Chapter 1 with burned-in subtitles.

# Step 1: Generate ffmpeg input files
#python3 create_video.py

# Step 2: Create the initial video without subtitles
#bash run_ffmpeg.sh

# Step 3: Burn the subtitles into the video
HandBrakeCLI -i chapter_002.mp4 -o chapter_002_with_subs.mp4 --srt-file generated_audio/chapter_002.srt --srt-burn

# Step 4: Clean up the intermediate video file
#rm chapter_001.mp4

echo "Video creation for Chapter 1 complete. The final video is chapter_002_with_subs.mp4"

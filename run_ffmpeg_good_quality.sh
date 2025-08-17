ffmpeg -y -f concat -safe 0 -i ffmpeg_input.txt -i generated_audio/chapter_001.wav \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p -movflags +faststart \
  chapter_001.mp4

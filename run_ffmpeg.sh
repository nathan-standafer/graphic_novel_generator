#!/bin/bash
ffmpeg -y -f concat -safe 0 -i ffmpeg_input.txt -i generated_audio/book_000.wav -c:v mpeg4 -b:v 5000k -qscale:v 2 -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart book_000.mp4
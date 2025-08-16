
import re
from datetime import datetime, timedelta

def parse_srt_time(s):
    return datetime.strptime(s, '%H:%M:%S,%f')

def calculate_duration(start, end):
    duration =  (end - start).total_seconds()
    print("{} - {} = {}".format(start, end, duration))
    return (end - start).total_seconds()

def generate_ffmpeg_input_file(srt_path, num_images, output_path):
    with open(srt_path, 'r') as f:
        srt_content = f.read()

    srt_blocks = srt_content.strip().split('\n\n')
    
    # Distribute images evenly among srt blocks
    images_per_block = num_images // len(srt_blocks)
    extra_images = num_images % len(srt_blocks)

    image_durations = []
    image_counter = 1
    duration_total = 0
    last_end_str = "00:00:00,000"

    for i, block in enumerate(srt_blocks):
        lines = block.split('\n')
        time_line = lines[1]
        start_str, end_str = time_line.split(' --> ')
        start_time = parse_srt_time(last_end_str)
        end_time = parse_srt_time(end_str)
        
        duration = calculate_duration(start_time, end_time)
        last_end_str = end_str

        duration_total += duration
        print("Duration Total: {}".format(duration_total))

        image_durations.append((f"file 'generated_illustrations/chapter_001/chapter_001_scene_{image_counter:03d}.png'", duration))
        image_counter += 1

    with open(output_path, 'w') as f:
        for img_path, duration in image_durations:
            f.write(f"{img_path}\n")
            f.write(f"duration {duration}\n")
        # Repeat the last image to fill any remaining time
        if image_durations:
            f.write(f"{image_durations[-1][0]}\n")


if __name__ == '__main__':
    srt_file = 'generated_audio/chapter_001.srt'
    num_images = 191
    ffmpeg_input_file = 'ffmpeg_input.txt'
    generate_ffmpeg_input_file(srt_file, num_images, ffmpeg_input_file)

    output_video_file = 'chapter_001.mp4'
    audio_file = 'generated_audio/chapter_001.wav'
    srt_file_for_subtitles = 'generated_audio/chapter_001.srt'

    ffmpeg_command = (
        f"ffmpeg -y -f concat -safe 0 -i {ffmpeg_input_file} -i {audio_file} "
        f"-c:v mpeg4 -c:a aac -strict experimental -b:a 192k -pix_fmt yuv420p -movflags +faststart {output_video_file}"
    )

    with open('run_ffmpeg.sh', 'w') as f:
        f.write(ffmpeg_command)

    print(f"FFmpeg command written to run_ffmpeg.sh")

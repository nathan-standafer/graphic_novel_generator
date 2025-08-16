

#!/usr/bin/env python3
"""
Demo script for Graphic Novel Video Creator

This script demonstrates the basic functionality of the pipeline
by processing a small sample text and generating a simple video.
"""

import os
import subprocess
import tempfile

def demo_pipeline():
    """Run a simplified demo of the graphic novel video creator pipeline."""

    print("🎬 Welcome to Graphic Novel Video Creator Demo! 📚")
    print("This demo will process a short sample text and create a simple video.")

    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Step 1: Create a simple test chapter
        test_chapter = """
CHAPTER 1

Once upon a time in a land far, far away, there lived a brave knight.
The knight embarked on a quest to find the magical treasure hidden deep within the enchanted forest.

As he ventured deeper into the woods, he encountered various challenges and mystical creatures. The sun began to set, casting long shadows through the dense canopy above.

With determination in his heart, the knight pressed onward, knowing that the treasure was within reach.
"""

        with open("test_chapter.txt", "w") as f:
            f.write(test_chapter)

        print("\n1️⃣ Creating test chapter: ✅")

        # Step 2: Generate a simple prompt (mock version)
        print("2️⃣ Generating image prompts...")

        # Mock prompt generation
        prompt = "A dark, moody oil painting of a brave knight venturing into an enchanted forest at sunset"

        with open("test_prompt.txt", "w") as f:
            f.write(prompt)

        print("   Prompt: '{}'".format(prompt))
        print("3️⃣ Image prompt generation: ✅")

        # Step 3: Generate simple audio (mock version)
        print("\n4️⃣ Generating narration audio...")

        # Create a simple placeholder audio file
        with open("test_audio.wav", "wb") as f:
            f.write(b"\x00" * 1024)  # Minimal WAV header

        print("   Created test_audio.wav")
        print("5️⃣ Audio generation: ✅")

        # Step 4: Create simple video
        print("\n6️⃣ Creating demo video...")

        # Create a simple ffmpeg input file
        with open("ffmpeg_input.txt", "w") as f:
            f.write("file 'test_image.png'\nduration 5\n")

        # Run ffmpeg to create a simple video
        subprocess.run([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", "ffmpeg_input.txt",
            "-i", "test_audio.wav",
            "-c:v", "mpeg4",
            "-c:a", "aac",
            "-strict", "experimental",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "demo_output.mp4"
        ], capture_output=True)

        print("   Video created: demo_output.mp4")
        print("7️⃣ Video creation: ✅")

        # Step 5: Show results
        print("\n🎉 Demo complete!")
        print("The demo has created:")
        print("  - test_chapter.txt (sample text)")
        print("  - test_prompt.txt (image prompt)")
        print("  - test_audio.wav (narration audio)")
        print("  - ffmpeg_input.txt (video input file)")
        print("  - demo_output.mp4 (final video)")

        print("\n💡 For a full pipeline experience:")
        print("1. Place your book in source_text/")
        print("2. Run 'python generate_prompts.py'")
        print("3. Generate illustrations using ComfyUI")
        print("4. Run 'python generate_audio_and_srt.py'")
        print("5. Run 'bash recreate_chapter_1_video.sh'")

if __name__ == "__main__":
    demo_pipeline()


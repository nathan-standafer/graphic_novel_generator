
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_thumbnails(chapter_number):
    """
    Adds a title to the first 10 images in a chapter's illustration
    folder and saves them as thumbnails.

    Args:
        chapter_number (str): The chapter number (e.g., '001').
    """
    base_dir = 'generated_illustrations'
    chapter_dir = os.path.join(base_dir, f'book_{chapter_number}')

    if not os.path.isdir(chapter_dir):
        print(f"Error: Directory not found at '{chapter_dir}'")
        return

    # Get the first 10 image files
    try:
        images = sorted([
            f for f in os.listdir(chapter_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ])[:10]
    except FileNotFoundError:
        print(f"Error: Could not list files in '{chapter_dir}'. It may be empty or inaccessible.")
        return
        
    if not images:
        print(f"No images found in '{chapter_dir}'")
        return

    # --- Font Configuration ---
    # You may need to change this path to a valid font file on your system.
    # Common Linux path: /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
    # If you're on another OS, you might need to provide a full path to a .ttf file.
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size=90)
    except IOError:
        print("Default font 'DejaVuSans-Bold.ttf' not found. Using basic font.")
        try:
            font = ImageFont.truetype("sans-serif.ttf", size=90)
        except IOError:
            print("Fallback sans-serif font not found. Using PIL default.")
            font = ImageFont.load_default()

    for image_name in images:
        try:
            image_path = os.path.join(chapter_dir, image_name)
            with Image.open(image_path).convert("RGBA") as img:
                draw = ImageDraw.Draw(img)

                # Text to add
                #text = f"Moby Dick\nChapter {chapter_number}"
                text = f"The Odyssey\nPrologue"

                # Get text size
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]


                # Position text at the bottom left
                img_width, img_height = img.size
                x = 30  # 30px padding from left
                y = img_height - text_height - 30  # 30px padding from bottom

                # Draw a thin black border for better visibility
                draw.text((x-2, y-2), text, font=font, fill="black")
                draw.text((x+2, y-2), text, font=font, fill="black")
                draw.text((x-2, y+2), text, font=font, fill="black")
                draw.text((x+2, y+2), text, font=font, fill="black")

                # Draw the main text with the specified RGB color
                draw.text((x, y), text, font=font, fill=(185, 213, 37))

                # Save the new image
                name, ext = os.path.splitext(image_name)
                new_filename = f"{name}_thumb{ext}"
                output_path = os.path.join(chapter_dir, new_filename)
                img.save(output_path)
                print(f"Created thumbnail: {output_path}")

        except Exception as e:
            print(f"Could not process {image_name}. Reason: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_thumbnails.py <chapter_number>")
        print("Example: python create_thumbnails.py 001")
        sys.exit(1)

    chapter = sys.argv[1]
    create_thumbnails(chapter)

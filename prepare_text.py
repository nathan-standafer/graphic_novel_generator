
import os
import re

def split_text_into_chapters(input_file, output_dir):
    """
    Splits a text file into chapters and saves each chapter to a separate file.

    Args:
        input_file (str): The path to the input text file.
        output_dir (str): The path to the directory where chapter files will be saved.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Split the text by "CHAPTER" followed by a number.
    # The regex uses a positive lookahead (?=...) to keep the delimiter.
    chapters = re.split(r'(?=CHAPTER \d+)', text)

    # The first split might be the content before the first chapter
    # (e.g., title page, table of contents). We'll start from the first real chapter.
    chapter_num = 0
    for i, chapter_content in enumerate(chapters):
        if chapter_content.strip().startswith("CHAPTER"):
            chapter_num += 1
            # Clean up the chapter content
            # Remove extra whitespace at the beginning and end
            cleaned_content = chapter_content.strip()

            # Create a logical filename
            file_name = f"chapter_{chapter_num:03d}.txt"
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, 'w', encoding='utf-8') as chapter_file:
                chapter_file.write(cleaned_content)
            print(f"Created {file_path}")

if __name__ == '__main__':
    # The user specified the source file is in ./source_text/Moby_Dick.txt
    # and the output directory is ./source_text_chunked
    source_file = os.path.join('source_text', 'Moby_Dick.txt')
    chunked_dir = 'source_text_chunked'
    
    split_text_into_chapters(source_file, chunked_dir)
    print("\nText splitting into chapters is complete.")
    print(f"Chapter files are located in the '{chunked_dir}' directory.")

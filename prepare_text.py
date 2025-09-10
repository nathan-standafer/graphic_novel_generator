
import os
import re
source_text_filename = "the_odyssey.txt"
def split_text_into_books(input_file, output_dir):
    """
    Splits a text file into books and saves each book to a separate file.

    Args:
        input_file (str): The path to the input text file.
        output_dir (str): The path to the directory where book files will be saved.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Split the text by "BOOK" followed by a Roman numeral or number.
    # The regex uses a positive lookahead (?=...) to keep the delimiter.
    books = re.split(r'(?=(?:BOOK\s+(?:[IVXLCDM]+|[0-9]+)))', text)
    print("found {} books".format(len(books)))

    # The first split might be the content before the first book
    # (e.g., title page, table of contents). We'll start from the first real book.
    book_num = 0
    for i, book_content in enumerate(books):
        if re.match(r'^BOOK\s+(?:[IVXLCDM]+|[0-9]+)', book_content.strip()):
            book_num += 1
            # Clean up the book content
            # Remove extra whitespace at the beginning and end
            cleaned_content = book_content.strip()

            # Create a logical filename
            file_name = f"book_{book_num:03d}.txt"
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, 'w', encoding='utf-8') as book_file:
                book_file.write(cleaned_content)
            print(f"Created {file_path}")

if __name__ == '__main__':
    # The user specified the source file is in ./source_text/{source_text_filename}
    # and the output directory is ./source_text_chunked
    source_file = os.path.join('source_text', source_text_filename)
    chunked_dir = 'source_text_chunked'
    
    split_text_into_books(source_file, chunked_dir)
    print("\nText splitting into books is complete.")
    print(f"Book files are located in the '{chunked_dir}' directory.")

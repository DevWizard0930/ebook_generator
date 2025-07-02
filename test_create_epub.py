from book_formatter import BookFormatter
from config import Config

def main():
    formatter = BookFormatter()
    
    # Sample book data with correct structure
    book_data = {
        "title": "Test Book",
        "chapters": [
            {
                "chapter_number": 1,
                "chapter_title": "Introduction",
                "content": "This is the introduction chapter content."
            },
            {
                "chapter_number": 2,
                "chapter_title": "Main Content",
                "content": "This is the main chapter content with multiple paragraphs.\n\nThis is the second paragraph."
            }
        ],
        "back_cover_blurb": "This is a test back cover blurb for the book.",
        "synopsis": "A test book for EPUB creation.",
        "cover_path": "output/test_cover.png"
    }
    
    output_path = "output/test_book.epub"
    
    try:
        result = formatter.create_epub(book_data, output_path)
        print(f"EPUB created successfully at: {result}")
    except Exception as e:
        print(f"Error creating: {e}")

if __name__ == "__main__":
    main()
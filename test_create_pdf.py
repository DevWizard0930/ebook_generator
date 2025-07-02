from book_formatter import BookFormatter

def main():
    formatter = BookFormatter()
    # Example book data (adjust keys/structure as needed for your function)
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "chapters": [
            {'chapter_number': 1, "chapter_title": "Introduction", "content": "This is the introduction."},
            {'chapter_number': 2, "chapter_title": "Chapter 1", "content": "This is the first chapter."}
        ],
        "back_cover_blurb": "This is a test blurb.",
        # Add any other fields your function expects
    }
    output_path = "output/test_book.mobi"
    try:
        formatter.create_mobi('output/test_book.epub', output_path)
        print(f"Mobi created at: {output_path}")
    except Exception as e:
        print(f"Error creating Mobi: {e}")

if __name__ == "__main__":
    main()
from book_builder import BookBuilder

def main():
    builder = BookBuilder()
    # Example concept, outline, chapters, blurb, and cover_path
    concept = {
        "title": "Test Book",
        "niche": "Test Niche",
        "concept_summary": "A test book concept.",
        "word_count": 10000,
        "chapter_count": 2,
        "subgenre": "Test Subgenre"
    }
    outline = {
        "title": "Test Book",
        "chapters": [
            {"chapter_number": 1, "chapter_title": "Intro", "summary": "Intro summary"},
            {"chapter_number": 2, "chapter_title": "Main", "summary": "Main summary"}
        ]
    }
    chapters = [
        "This is the introduction.",
        "This is the first chapter."
    ]
    back_cover_blurb = "This is a test back cover blurb."
    cover_path = "output/test_cover.png"  # Use a real image path if your formatter requires it

    try:
        result = builder.format_book_files(
            concept=concept,
            outline=outline,
            chapters=chapters,
            back_cover_blurb=back_cover_blurb,
            cover_path=cover_path
        )
        print("Format book files result:", result)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
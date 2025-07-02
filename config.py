import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GPT4_MODEL = "gpt-4"
    GPT35_MODEL = "gpt-3.5-turbo"
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS_FILE = os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_DRIVE_TOKEN_FILE = os.getenv('GOOGLE_DRIVE_TOKEN_FILE', 'token.json')
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    # Airtable Configuration
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME', 'Books')
    
    # StreetLib Configuration
    STREETLIB_EMAIL = os.getenv('STREETLIB_EMAIL')
    STREETLIB_PASSWORD = os.getenv('STREETLIB_PASSWORD')
    STREETLIB_URL = "https://hub.streetlib.com"
    
    # File Paths
    OUTPUT_DIR = "output"
    TEMPLATES_DIR = "templates"
    COVERS_DIR = "covers"
    BOOKS_DIR = "books"
    
    # Book Generation Settings
    MIN_WORD_COUNT = 16000
    MAX_WORD_COUNT = 20000
    MIN_CHAPTERS = 10
    MAX_CHAPTERS = 15
    WORDS_PER_CHAPTER = 1200
    
    # Cover Image Settings
    COVER_WIDTH = 1024
    COVER_HEIGHT = 1792
    
    # Supported Genres
    SUPPORTED_GENRES = ["Paranormal Romance", "Cozy Mystery"]
    
    # Author Information
    AUTHOR_NAME = "AI Author"
    AUTHOR_EMAIL = "ai@example.com"
    
    # Publishing Settings
    DEFAULT_PRICE_USD = 2.99
    DEFAULT_PRICE_EUR = 2.49
    PUBLICATION_YEAR = 2025
    LANGUAGE = "English"
    AGE_RATING = "Adult" 
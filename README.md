# J & M Publishing Automation

A complete AI-powered eBook generation and publishing system that automates the entire process from concept to publication. This system generates commercially viable fiction books in Paranormal Romance and Cozy Mystery genres, creates professional covers, formats them into multiple eBook formats, uploads to Google Drive, and publishes to StreetLib.

## 🚀 Features

### Milestone 1: Core AI Generation Pipeline ✅
- **GPT-4 + GPT-3.5 Integration**: Uses GPT-4 for concept and outline generation, GPT-3.5 for chapter writing
- **Dynamic Genre Selection**: Automatically selects between Paranormal Romance and Cozy Mystery
- **Structured Content Generation**: Creates complete book concepts, titles, outlines, and chapters
- **Local File Storage**: All content saved locally in organized folders

### Milestone 2: Cover Generation + File Formatting ✅
- **DALL-E 3 Integration**: Generates professional book covers using AI
- **Text Overlay**: Adds title and author text to covers using Pillow
- **Multiple Format Support**: Creates EPUB, PDF, and MOBI formats using ebooklib and reportlab
- **Professional Layout**: Includes title pages, table of contents, and proper formatting

### Milestone 3: Google Drive Upload + Metadata Logging ✅
- **Google Drive API Integration**: Uploads all book files and covers to organized folders
- **Airtable Logging**: Tracks all book metadata, generation times, and publishing status
- **Error Handling**: Comprehensive error handling and confirmation logging
- **Backup Systems**: Local backup logs in case of API failures

### Milestone 4: StreetLib Publishing via Playwright ✅
- **Browser Automation**: Uses Playwright to automate StreetLib dashboard interactions
- **Form Filling**: Automatically fills all required metadata, uploads files and covers
- **ISBN Assignment**: Handles ISBN assignment and dropdown selections
- **Screenshot Logging**: Takes screenshots for debugging and verification

### Milestone 5: One-Click Book Builder ✅
- **CLI Interface**: Simple command-line interface for easy operation
- **Modular Architecture**: Clean, maintainable code structure
- **Error Recovery**: Retry logic and graceful error handling
- **Complete Automation**: Input genre → Output published eBook

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to GPT-4 and DALL-E 3
- Google Cloud Platform account (for Google Drive API)
- Airtable account (optional, for logging)
- StreetLib account (for publishing)
- Calibre (optional, for MOBI conversion)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ebook_automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys and credentials
   ```

5. **Set up Google Drive API**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Drive API
   - Create credentials (OAuth 2.0 Client ID)
   - Download `credentials.json` and place in project root

6. **Set up Airtable** (optional):
   - Create a new base in Airtable
   - Create a table named "Books" with appropriate fields
   - Get your API key and base ID

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Drive Configuration
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
GOOGLE_DRIVE_TOKEN_FILE=token.json
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id_here

# Airtable Configuration
AIRTABLE_API_KEY=your_airtable_api_key_here
AIRTABLE_BASE_ID=your_airtable_base_id_here
AIRTABLE_TABLE_NAME=Books

# StreetLib Configuration
STREETLIB_EMAIL=your_streetlib_email@example.com
STREETLIB_PASSWORD=your_streetlib_password_here
```

### Airtable Table Structure

Create a table named "Books" with these fields:
- Title (Single line text)
- Genre (Single select: Paranormal Romance, Cozy Mystery)
- Subgenre (Single line text)
- Hook (Long text)
- Synopsis (Long text)
- Word Count (Number)
- Chapter Count (Number)
- Keywords (Long text)
- Status (Single select: Generated, Cover Generated, Files Created, Google Drive Uploaded, Published on StreetLib)
- Generation Date (Date)
- Generation Time (seconds) (Number)
- Author (Single line text)
- Publication Year (Number)
- Language (Single line text)
- Back Cover Blurb (Long text)
- Cover Generated (Checkbox)
- Cover Path (Single line text)
- Files Created (Checkbox)
- Available Formats (Multiple select)
- Google Drive Uploaded (Checkbox)
- Google Drive Folder ID (Single line text)
- StreetLib Published (Checkbox)
- ISBN (Single line text)
- Publishing URL (URL)

## 🚀 Usage

### Basic Usage

Generate a book with random genre:
```bash
python book_builder.py
```

### Advanced Usage

Generate a specific genre:
```bash
python book_builder.py --genre "Paranormal Romance"
```

Generate with custom title:
```bash
python book_builder.py --title "My Custom Book Title"
```

Skip Google Drive upload:
```bash
python book_builder.py --skip-google-drive
```

Skip StreetLib publishing:
```bash
python book_builder.py --skip-streetlib
```

### Output Structure

The system creates the following directory structure:

```
ebook_automation/
├── output/                 # General output files
├── covers/                 # Generated cover images
├── books/                  # Formatted book files
│   └── Book_Title/
│       ├── Book_Title.epub
│       ├── Book_Title.pdf
│       └── Book_Title.mobi
├── screenshots/            # StreetLib automation screenshots
├── logs/                   # Log files
└── book_builder.log        # Main log file
```

## 📚 Generated Content

### Book Specifications
- **Word Count**: 16,000-20,000 words
- **Chapters**: 10-15 chapters
- **Genres**: Paranormal Romance, Cozy Mystery
- **Formats**: EPUB, PDF, MOBI
- **Cover**: 1024x1536 pixels, AI-generated with text overlay

### Content Quality
- **Professional Structure**: Proper pacing, character development, conflict resolution
- **Genre-Appropriate**: Follows genre conventions and reader expectations
- **Market-Ready**: Commercially viable concepts and execution
- **SEO-Optimized**: Includes relevant keywords and metadata

## 🔍 Monitoring and Logging

### Log Files
- `book_builder.log`: Main application log
- `logs/`: Additional log files for specific components

### Airtable Tracking
- Real-time status updates
- Generation metrics and timing
- File paths and links
- Error tracking and resolution

### Screenshots
- StreetLib automation screenshots for debugging
- Stored in `screenshots/` directory

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **API Failures**: Graceful degradation when APIs are unavailable
- **File Operations**: Safe file handling with proper cleanup
- **Browser Automation**: Screenshot capture and error logging
- **Retry Logic**: Automatic retries for transient failures
- **Backup Logging**: Local backup when Airtable is unavailable

## 🔧 Customization

### Adding New Genres
1. Update `Config.SUPPORTED_GENRES`
2. Modify AI prompts in `ai_generator.py`
3. Update cover generation prompts
4. Add genre-specific formatting rules

### Custom Prompts
Edit the prompt templates in `ai_generator.py` to customize:
- Book concept generation
- Chapter writing style
- Cover image prompts
- Metadata generation

### Format Customization
Modify `book_formatter.py` to:
- Change PDF styling
- Customize EPUB structure
- Add new file formats
- Modify cover text overlay

## 📊 Performance

### Typical Generation Times
- **Concept + Outline**: 30-60 seconds
- **Chapters**: 5-10 minutes (depending on chapter count)
- **Cover Generation**: 30-60 seconds
- **File Formatting**: 10-30 seconds
- **Google Drive Upload**: 1-5 minutes
- **StreetLib Publishing**: 2-5 minutes

### Total Time
- **Complete Process**: 10-20 minutes per book
- **Text-Only Generation**: 5-10 minutes

## 🚨 Troubleshooting

### Common Issues

**OpenAI API Errors**:
- Check API key validity
- Verify account has GPT-4 and DALL-E 3 access
- Check rate limits and billing

**Google Drive Upload Failures**:
- Verify `credentials.json` is in project root
- Check Google Drive API is enabled
- Ensure folder ID is correct

**StreetLib Publishing Issues**:
- Verify login credentials
- Check website structure hasn't changed
- Review screenshots for debugging

**Airtable Logging Problems**:
- Verify API key and base ID
- Check table structure matches requirements
- Ensure proper field types

### Debug Mode
Enable detailed logging by modifying the logging level in `book_builder.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is proprietary software for J & M Publishing. All rights reserved.

## 🤝 Support

For support and questions:
- Check the troubleshooting section
- Review log files for detailed error information
- Contact the development team

## 🔄 Updates

### Version History
- **v1.0.0**: Initial release with all 5 milestones completed
- Full AI-powered book generation
- Multi-format output support
- Google Drive integration
- StreetLib automation
- Airtable logging

### Future Enhancements
- Additional genre support
- Enhanced cover customization
- Batch processing capabilities
- Advanced analytics dashboard
- Integration with additional publishing platforms 
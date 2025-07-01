#!/usr/bin/env python3
"""
J & M Publishing Automation - Book Builder
Complete AI-powered eBook generation and publishing system
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Import our modules
from config import Config
from ai_generator import AIGenerator
from book_formatter import BookFormatter
from google_drive_uploader import GoogleDriveUploader
from airtable_logger import AirtableLogger
from streetlib_publisher import StreetLibPublisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('book_builder.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BookBuilder:
    def __init__(self):
        self.ai_generator = AIGenerator()
        self.book_formatter = BookFormatter()
        self.drive_uploader = None
        self.airtable_logger = AirtableLogger()
        self.streetlib_publisher = None
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for the project"""
        directories = [
            Config.OUTPUT_DIR,
            Config.COVERS_DIR,
            Config.BOOKS_DIR,
            "screenshots",
            "logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_book_concept(self) -> Dict:
        """Generate a complete book concept"""
        logger.info("=== STEP 1: Generating Book Concept ===")
        start_time = time.time()
        
        try:
            concept = self.ai_generator.generate_book_concept()
            generation_time = time.time() - start_time
            
            logger.info(f"Generated concept: {concept['niche']} - {concept['hook']}")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            return concept
            
        except Exception as e:
            logger.error(f"Error generating book concept: {e}")
            raise
    
    def generate_title_and_outline(self, concept: Dict) -> Dict:
        """Generate title and chapter outline"""
        logger.info("=== STEP 2: Generating Title and Outline ===")
        start_time = time.time()
        
        try:
            outline = self.ai_generator.generate_title_and_outline(concept)
            generation_time = time.time() - start_time
            
            logger.info(f"Generated title: {outline['title']}")
            logger.info(f"Generated {len(outline['chapters'])} chapters")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            return outline
            
        except Exception as e:
            logger.error(f"Error generating title and outline: {e}")
            raise
    
    def generate_chapters(self, book_title: str, genre: str, outline: Dict) -> List[str]:
        """Generate all chapters"""
        logger.info("=== STEP 3: Generating Chapters ===")
        start_time = time.time()
        
        try:
            chapters = []
            previous_chapters = []
            
            for chapter_data in outline['chapters']:
                chapter_number = chapter_data['chapter_number']
                chapter_title = chapter_data['chapter_title']
                chapter_summary = chapter_data['summary']
                
                logger.info(f"Generating chapter {chapter_number}: {chapter_title}")
                
                chapter_content = self.ai_generator.generate_chapter(
                    book_title=book_title,
                    genre=genre,
                    chapter_number=chapter_number,
                    chapter_title=chapter_title,
                    chapter_summary=chapter_summary,
                    previous_chapters=previous_chapters
                )
                
                chapters.append(chapter_content)
                previous_chapters.append(chapter_summary)
                
                # Small delay between chapters
                time.sleep(1)
            
            generation_time = time.time() - start_time
            logger.info(f"Generated {len(chapters)} chapters")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            # Save full text content to file
            book_title_clean = book_title.replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
            content_file_path = os.path.join(Config.OUTPUT_DIR, f"{book_title_clean}_full_content.txt")
            
            with open(content_file_path, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("📖 FULL BOOK CONTENT\n")
                f.write("="*80 + "\n")
                f.write(f"Title: {book_title}\n")
                f.write(f"Genre: {genre}\n")
                f.write(f"Total Chapters: {len(chapters)}\n")
                f.write(f"Estimated Word Count: {sum(len(chapter.split()) for chapter in chapters)}\n")
                f.write("="*80 + "\n\n")
                
                for i, chapter in enumerate(chapters):
                    f.write(f"--- Chapter {i+1}: {outline['chapters'][i]['chapter_title']} ---\n")
                    f.write(chapter + "\n")
                    f.write("\n" + "-"*60 + "\n\n")
                
                f.write("="*80 + "\n")
                f.write("📖 END OF BOOK CONTENT\n")
                f.write("="*80 + "\n")
            
            logger.info(f"Full book content saved to: {content_file_path}")
            
            return chapters
            
        except Exception as e:
            logger.error(f"Error generating chapters: {e}")
            raise
    
    def generate_back_cover_blurb(self, book_title: str, genre: str, concept_summary: str) -> str:
        """Generate back cover blurb"""
        logger.info("=== STEP 4: Generating Back Cover Blurb ===")
        start_time = time.time()
        
        try:
            blurb = self.ai_generator.generate_back_cover_blurb(
                book_title=book_title,
                genre=genre,
                concept_summary=concept_summary
            )
            
            generation_time = time.time() - start_time
            logger.info(f"Generated back cover blurb ({len(blurb)} characters)")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            return blurb
            
        except Exception as e:
            logger.error(f"Error generating back cover blurb: {e}")
            raise
    
    def generate_cover_image(self, book_title: str, genre: str) -> str:
        """Generate cover image"""
        logger.info("=== STEP 5: Generating Cover Image ===")
        start_time = time.time()
        
        try:
            # Generate image prompt
            image_prompt = self.ai_generator.generate_cover_image_prompt(
                book_title=book_title,
                genre=genre
            )
            
            # Generate cover image
            cover_filename = f"cover_{book_title.replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')}.png"
            cover_path = os.path.join(Config.COVERS_DIR, cover_filename)
            
            cover_path = self.ai_generator.generate_cover_image(image_prompt, cover_path)
            
            # Add text overlay
            final_cover_path = os.path.join(Config.COVERS_DIR, f"final_{cover_filename}")
            self.book_formatter.add_text_to_cover(
                cover_path=cover_path,
                title=book_title,
                author=Config.AUTHOR_NAME,
                output_path=final_cover_path
            )
            
            generation_time = time.time() - start_time
            logger.info(f"Generated cover image: {final_cover_path}")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            # Save book details to file
            book_title_clean = book_title.replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
            details_file_path = os.path.join(Config.OUTPUT_DIR, f"{book_title_clean}_book_details.txt")
            
            with open(details_file_path, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("📚 BOOK DETAILS\n")
                f.write("="*80 + "\n")
                f.write(f"Title: {book_title}\n")
                f.write(f"Genre: {genre}\n")
                f.write(f"Cover Image: {final_cover_path}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"Book details saved to: {details_file_path}")
            
            return final_cover_path
            
        except Exception as e:
            logger.error(f"Error generating cover image: {e}")
            raise
    
    def format_book_files(self, concept: Dict, outline: Dict, chapters: List[str], 
                         back_cover_blurb: str, cover_path: str) -> Dict:
        """Format book into various file formats"""
        logger.info("=== STEP 6: Formatting Book Files ===")
        start_time = time.time()
        
        try:
            # Format book data
            book_data = self.book_formatter.format_book_data(
                concept=concept,
                outline=outline,
                chapters=chapters,
                back_cover_blurb=back_cover_blurb,
                cover_path=cover_path
            )
            
            # Create output directory for this book
            book_title = book_data['title'].replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
            book_output_dir = os.path.join(Config.BOOKS_DIR, book_title)
            
            # Create all formats
            book_files = self.book_formatter.create_all_formats(book_data, book_output_dir)
            
            creation_time = time.time() - start_time
            logger.info(f"Created book files: {list(book_files.keys())}")
            logger.info(f"Creation time: {creation_time:.2f} seconds")
            
            # Save book formats info to file
            book_title_clean = book_data['title'].replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
            formats_file_path = os.path.join(Config.OUTPUT_DIR, f"{book_title_clean}_book_formats.txt")
            
            with open(formats_file_path, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("📄 BOOK FORMATS CREATED\n")
                f.write("="*80 + "\n")
                f.write(f"Book Title: {book_data['title']}\n")
                f.write(f"Author: {book_data['author']}\n")
                f.write(f"Output Directory: {book_output_dir}\n")
                f.write("\nFormats:\n")
                for format_name, file_path in book_files.items():
                    f.write(f"  • {format_name.upper()}: {file_path}\n")
                f.write("="*80 + "\n")
            
            logger.info(f"Book formats info saved to: {formats_file_path}")
            
            return book_files
            
        except Exception as e:
            logger.error(f"Error formatting book files: {e}")
            raise
    
    def upload_to_google_drive(self, book_title: str, book_files: Dict, cover_path: str) -> Optional[Dict]:
        """Upload files to Google Drive"""
        logger.info("=== STEP 7: Uploading to Google Drive ===")
        start_time = time.time()
        
        try:
            if not self.drive_uploader:
                self.drive_uploader = GoogleDriveUploader()
            
            upload_info = self.drive_uploader.upload_book_files(
                book_title=book_title,
                book_files=book_files,
                cover_path=cover_path
            )
            
            upload_time = time.time() - start_time
            logger.info(f"Uploaded to Google Drive: {upload_info['folder_name']}")
            logger.info(f"Upload time: {upload_time:.2f} seconds")
            
            return upload_info
            
        except Exception as e:
            logger.error(f"Error uploading to Google Drive: {e}")
            return None
    
    def generate_streetlib_metadata(self, book_data: Dict) -> Dict:
        """Generate StreetLib metadata"""
        logger.info("=== STEP 8: Generating StreetLib Metadata ===")
        start_time = time.time()
        
        try:
            metadata = self.ai_generator.generate_streetlib_metadata(book_data)
            
            generation_time = time.time() - start_time
            logger.info(f"Generated StreetLib metadata for: {metadata.get('title', '')}")
            logger.info(f"Generation time: {generation_time:.2f} seconds")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating StreetLib metadata: {e}")
            raise
    
    def publish_to_streetlib(self, metadata: Dict, cover_path: str, book_files: Dict) -> Dict:
        """Publish to StreetLib"""
        logger.info("=== STEP 9: Publishing to StreetLib ===")
        start_time = time.time()
        
        try:
            with StreetLibPublisher() as publisher:
                result = publisher.publish_book(
                    metadata=metadata,
                    cover_path=cover_path,
                    book_files=book_files
                )
            
            publishing_time = time.time() - start_time
            logger.info(f"StreetLib publishing result: {result.get('success', False)}")
            logger.info(f"Publishing time: {publishing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error publishing to StreetLib: {e}")
            return {'success': False, 'error': str(e)}
    
    def build_book(self, genre: Optional[str] = None, title: Optional[str] = None) -> Dict:
        """Complete book building process"""
        logger.info("=== STARTING BOOK BUILDING PROCESS ===")
        total_start_time = time.time()
        
        try:
            # Step 1: Generate concept
            concept = self.generate_book_concept()
            
            # Override genre if specified
            if genre:
                concept['niche'] = genre
            
            # Step 2: Generate title and outline
            outline = self.generate_title_and_outline(concept)
            
            # Override title if specified
            if title:
                outline['title'] = title
            
            # Step 3: Generate chapters
            chapters = self.generate_chapters(
                book_title=outline['title'],
                genre=concept['niche'],
                outline=outline
            )
            
            # Step 4: Generate back cover blurb
            back_cover_blurb = self.generate_back_cover_blurb(
                book_title=outline['title'],
                genre=concept['niche'],
                concept_summary=concept['concept_summary']
            )
            
            # Calculate total time
            total_time = time.time() - total_start_time
            
            
            # Create backup log
            backup_log_path = os.path.join(Config.OUTPUT_DIR, f"{outline['title'].replace(' ', '_')}_backup.json")
            # Prepare result
            result = {
                'success': True,
                'book_title': outline['title'],
                'genre': concept['niche'],
                'word_count': concept['word_count'],
                'total_time': total_time,
            }
            
            logger.info("=== BOOK BUILDING PROCESS COMPLETED ===")
            logger.info(f"Book: {outline['title']}")
            logger.info(f"Genre: {concept['niche']}")
            logger.info(f"Word Count: {concept['word_count']}")
            logger.info(f"Total Time: {total_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in book building process: {e}")
            total_time = time.time() - total_start_time

            return {
                'success': False,
                'error': str(e),
                'total_time': total_time
            }
            

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='J & M Publishing Automation - Book Builder')
    parser.add_argument('--genre', choices=Config.SUPPORTED_GENRES, 
                       help='Specify genre (Paranormal Romance or Cozy Mystery)')
    parser.add_argument('--title', help='Specify custom book title')
    parser.add_argument('--skip-google-drive', action='store_true', 
                       help='Skip Google Drive upload')
    parser.add_argument('--skip-streetlib', action='store_true', 
                       help='Skip StreetLib publishing')
    parser.add_argument('--demo', action='store_true', 
                       help='Run demo mode with sample data')
    
    args = parser.parse_args()
    
    # Initialize book builder
    builder = BookBuilder()
    
    if args.demo:
        logger.info("Running in demo mode...")
        # Demo mode would use sample data instead of AI generation
        print("Demo mode not implemented yet. Use normal mode.")
        return
    
    try:
        # Build the book
        result = builder.build_book(genre=args.genre, title=args.title)
        
        if result['success']:
            print(f"\n Book successfully created: {result['book_title']}")
            print(f"Genre: {result['genre']}")
            print(f"Word Count: {result['word_count']}")
            print(f"Total Time: {result['total_time']:.2f} seconds")
        else:
            print(f"\n Book creation failed: {result['error']}")
            print(f"Time spent: {result['total_time']:.2f} seconds")
    
    except KeyboardInterrupt:
        print("\n  Book creation interrupted by user")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        logger.error(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main() 
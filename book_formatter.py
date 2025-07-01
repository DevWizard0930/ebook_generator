import os
import json
from typing import Dict, List
from ebooklib import epub
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image, ImageDraw, ImageFont
import markdown
from bs4 import BeautifulSoup
import logging
from config import Config

logger = logging.getLogger(__name__)

class BookFormatter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for PDF formatting"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Chapter title style
        self.chapter_style = ParagraphStyle(
            'CustomChapter',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16
        )
    
    def create_epub(self, book_data: Dict, output_path: str) -> str:
        """Create EPUB format book"""
        try:
            # Create EPUB book
            book = epub.EpubBook()
            
            # Set metadata
            book.set_identifier(f"book_{book_data['title'].replace(' ', '_').lower()}")
            book.set_title(book_data['title'])
            book.set_language(Config.LANGUAGE.lower())
            book.add_author(Config.AUTHOR_NAME)
            
            # Add description if available
            if 'synopsis' in book_data:
                book.add_metadata('DC', 'description', book_data['synopsis'])
            
            # Create chapters
            chapters = []
            spine = ['nav']
            
            # Add title page
            title_content = f"""
            <h1>{book_data['title']}</h1>
            <p>by {Config.AUTHOR_NAME}</p>
            <p>{Config.PUBLICATION_YEAR}</p>
            """
            title_chapter = epub.EpubHtml(title='Title Page', file_name='title.xhtml')
            title_chapter.content = title_content
            book.add_item(title_chapter)
            chapters.append(title_chapter)
            spine.append(title_chapter)
            
            # Add table of contents
            toc_content = "<h1>Table of Contents</h1><ul>"
            for chapter in book_data['chapters']:
                toc_content += f"<li><a href='chapter_{chapter['chapter_number']}.xhtml'>{chapter['chapter_title']}</a></li>"
            toc_content += "</ul>"
            
            toc_chapter = epub.EpubHtml(title='Table of Contents', file_name='toc.xhtml')
            toc_chapter.content = toc_content
            book.add_item(toc_chapter)
            chapters.append(toc_chapter)
            spine.append(toc_chapter)
            
            # Add chapters
            for chapter_data in book_data['chapters']:
                chapter_number = chapter_data['chapter_number']
                chapter_title = chapter_data['chapter_title']
                chapter_content = chapter_data['content']
                
                # Format chapter content
                html_content = f"""
                <h2>{chapter_title}</h2>
                {self._format_text_to_html(chapter_content)}
                """
                
                chapter = epub.EpubHtml(
                    title=chapter_title,
                    file_name=f'chapter_{chapter_number}.xhtml'
                )
                chapter.content = html_content
                book.add_item(chapter)
                chapters.append(chapter)
                spine.append(chapter)
            
            # Add back cover blurb if available
            if 'back_cover_blurb' in book_data:
                blurb_content = f"""
                <h2>About the Book</h2>
                <p>{book_data['back_cover_blurb']}</p>
                """
                blurb_chapter = epub.EpubHtml(title='About the Book', file_name='blurb.xhtml')
                blurb_chapter.content = blurb_content
                book.add_item(blurb_chapter)
                chapters.append(blurb_chapter)
                spine.append(blurb_chapter)
            
            # Set table of contents
            book.toc = [(epub.Section('Table of Contents'), chapters)]
            book.spine = spine
            
            # Add default NCX and Nav files
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            
            # Add cover if available
            if 'cover_path' in book_data and os.path.exists(book_data['cover_path']):
                with open(book_data['cover_path'], 'rb') as cover_file:
                    book.set_cover("cover.jpg", cover_file.read())
            
            # Write EPUB file
            epub.write_epub(output_path, book)
            logger.info(f"Created EPUB: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating EPUB: {e}")
            raise
    
    def create_pdf(self, book_data: Dict, output_path: str) -> str:
        """Create PDF format book"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            # Add title page
            story.append(Paragraph(book_data['title'], self.title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"by {Config.AUTHOR_NAME}", self.body_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(str(Config.PUBLICATION_YEAR), self.body_style))
            story.append(PageBreak())
            
            # Add table of contents
            story.append(Paragraph("Table of Contents", self.chapter_style))
            story.append(Spacer(1, 20))
            
            for chapter in book_data['chapters']:
                story.append(Paragraph(f"{chapter['chapter_number']}. {chapter['chapter_title']}", self.body_style))
            story.append(PageBreak())
            
            # Add chapters
            for chapter_data in book_data['chapters']:
                chapter_title = chapter_data['chapter_title']
                chapter_content = chapter_data['content']
                
                story.append(Paragraph(chapter_title, self.chapter_style))
                story.append(Spacer(1, 20))
                
                # Split content into paragraphs and add to story
                paragraphs = chapter_content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), self.body_style))
                        story.append(Spacer(1, 12))
                
                story.append(PageBreak())
            
            # Add back cover blurb if available
            if 'back_cover_blurb' in book_data:
                story.append(Paragraph("About the Book", self.chapter_style))
                story.append(Spacer(1, 20))
                story.append(Paragraph(book_data['back_cover_blurb'], self.body_style))
            
            # Build PDF
            doc.build(story)
            logger.info(f"Created PDF: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            raise
    
    def create_mobi(self, epub_path: str, output_path: str) -> str:
        """Convert EPUB to MOBI format (requires Calibre command line tools)"""
        try:
            # This requires Calibre's ebook-convert command line tool
            import subprocess
            
            cmd = ['ebook-convert', epub_path, output_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Created MOBI: {output_path}")
                return output_path
            else:
                logger.warning(f"Calibre conversion failed: {result.stderr}")
                # Return EPUB path as fallback
                return epub_path
                
        except FileNotFoundError:
            logger.warning("Calibre not found. MOBI conversion skipped.")
            return epub_path
        except Exception as e:
            logger.error(f"Error creating MOBI: {e}")
            return epub_path
    
    def _format_text_to_html(self, text: str) -> str:
        """Convert plain text to HTML with proper formatting"""
        # Convert markdown to HTML if needed
        if '**' in text or '*' in text or '#' in text:
            html = markdown.markdown(text)
        else:
            # Simple text to HTML conversion
            paragraphs = text.split('\n\n')
            html_paragraphs = []
            for para in paragraphs:
                if para.strip():
                    # Convert line breaks to <br> tags
                    para_html = para.replace('\n', '<br>')
                    html_paragraphs.append(f"<p>{para_html}</p>")
            html = '\n'.join(html_paragraphs)
        
        return html
    
    def add_text_to_cover(self, cover_path: str, title: str, author: str, output_path: str) -> str:
        """Add text overlay to cover image"""
        try:
            # Open the cover image
            with Image.open(cover_path) as img:
                # Create a copy to work with
                cover = img.copy()
                
                # Create a drawing object
                draw = ImageDraw.Draw(cover)
                
                # Try to load a font, fall back to default if not available
                try:
                    # Try to use a nice font if available
                    title_font = ImageFont.truetype("arial.ttf", 60)
                    author_font = ImageFont.truetype("arial.ttf", 40)
                except:
                    # Fall back to default font
                    title_font = ImageFont.load_default()
                    author_font = ImageFont.load_default()
                
                # Get image dimensions
                width, height = cover.size
                
                # Calculate text positions (centered)
                title_bbox = draw.textbbox((0, 0), title, font=title_font)
                title_width = title_bbox[2] - title_bbox[0]
                title_x = (width - title_width) // 2
                title_y = height // 4
                
                author_bbox = draw.textbbox((0, 0), author, font=author_font)
                author_width = author_bbox[2] - author_bbox[0]
                author_x = (width - author_width) // 2
                author_y = title_y + 80
                
                # Add text with outline for better visibility
                # Draw outline
                outline_color = (0, 0, 0)
                text_color = (255, 255, 255)
                
                # Title outline
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            draw.text((title_x + dx, title_y + dy), title, font=title_font, fill=outline_color)
                
                # Title text
                draw.text((title_x, title_y), title, font=title_font, fill=text_color)
                
                # Author outline
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:
                            draw.text((author_x + dx, author_y + dy), author, font=author_font, fill=outline_color)
                
                # Author text
                draw.text((author_x, author_y), author, font=author_font, fill=text_color)
                
                # Save the modified cover
                cover.save(output_path, 'PNG')
                
                logger.info(f"Added text to cover: {output_path}")
                return output_path
                
        except Exception as e:
            logger.error(f"Error adding text to cover: {e}")
            # Return original cover path if modification fails
            return cover_path
    
    def format_book_data(self, concept: Dict, outline: Dict, chapters: List[str], 
                        back_cover_blurb: str, cover_path: str = None) -> Dict:
        """Format all book data into a structured format for formatting"""
        book_data = {
            'title': outline['title'],
            'genre': concept['niche'],
            'subgenre': concept['subgenre'],
            'word_count': concept['word_count'],
            'synopsis': concept['concept_summary'],
            'back_cover_blurb': back_cover_blurb,
            'chapters': []
        }
        
        # Add cover path if available
        if cover_path:
            book_data['cover_path'] = cover_path
        
        # Format chapters
        for i, chapter_content in enumerate(chapters):
            chapter_data = {
                'chapter_number': i + 1,
                'chapter_title': outline['chapters'][i]['chapter_title'],
                'content': chapter_content
            }
            book_data['chapters'].append(chapter_data)
        
        return book_data
    
    def create_all_formats(self, book_data: Dict, output_dir: str) -> Dict:
        """Create all book formats (EPUB, PDF, MOBI)"""
        os.makedirs(output_dir, exist_ok=True)
        
        book_title = book_data['title'].replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
        
        # Create EPUB
        epub_path = os.path.join(output_dir, f"{book_title}.epub")
        epub_path = self.create_epub(book_data, epub_path)
        
        # Create PDF
        pdf_path = os.path.join(output_dir, f"{book_title}.pdf")
        pdf_path = self.create_pdf(book_data, pdf_path)
        
        # Create MOBI (if Calibre is available)
        mobi_path = os.path.join(output_dir, f"{book_title}.mobi")
        mobi_path = self.create_mobi(epub_path, mobi_path)
        
        return {
            'epub': epub_path,
            'pdf': pdf_path,
            'mobi': mobi_path
        } 
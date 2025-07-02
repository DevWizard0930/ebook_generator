import os
import json
from typing import Dict, List, Union
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


from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
import tempfile
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter

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
            
            spine: list[Union[str, epub.EpubHtml]] = ['nav']


            with open(book_data['cover_path'], "rb") as f:
                cover_content = f.read()
                book.set_cover("cover.png", cover_content)  # This sets the EPUB thumbnail cover

            # === Add the image as a resource (so we can reference it in HTML) ===
            cover_image_item = epub.EpubItem(
                uid="cover-image",
                file_name="cover.png",
                media_type="image/png",
                content=cover_content
            )
            book.add_item(cover_image_item)

            # === Create a visible cover page (HTML with image tag) ===
            cover_html = epub.EpubHtml(
                title="Cover Page",
                file_name="cover.xhtml",
                content="""
                <!DOCTYPE html>
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta charset="utf-8"/>
                    <title>Cover</title>
                    <style type="text/css">
                    @page {
                        margin: 0;
                    }
                    html, body {
                        margin: 0 !important;
                        padding: 0 !important;
                        height: 100%;
                        width: 100%;
                    }
                    body {
                        display: flex;
                        align-items: stretch;
                        justify-content: stretch;
                    }
                    img {
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                        border: none;
                        display: block;
                    }
                    </style>
                </head>
                <body>
                    <img src="cover.png" alt="Cover"/>
                </body>
                </html>
                """
            )
            book.add_item(cover_html)
            # spine.append(cover_html)
            spine.insert(0, cover_html)

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
            
            # Write EPUB file
            epub.write_epub(output_path, book)
            logger.info(f"Created EPUB: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating EPUB: {e}")
            return output_path
    
    def create_pdf(self, book_data: Dict, output_path: str) -> str:
        try:
            temp_story_path = os.path.join(tempfile.gettempdir(), "temp_story.pdf")
            temp_cover_path = os.path.join(tempfile.gettempdir(), "temp_cover.pdf")

            # STEP 1 — Build the content PDF
            doc = SimpleDocTemplate(temp_story_path, pagesize=letter)
            story = []

            story.append(Paragraph(book_data['title'], self.title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"by {Config.AUTHOR_NAME}", self.body_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(str(Config.PUBLICATION_YEAR), self.body_style))
            story.append(PageBreak())

            story.append(Paragraph("Table of Contents", self.chapter_style))
            story.append(Spacer(1, 20))
            for chapter in book_data['chapters']:
                story.append(Paragraph(f"{chapter['chapter_number']}. {chapter['chapter_title']}", self.body_style))
            story.append(PageBreak())

            for chapter_data in book_data['chapters']:
                story.append(Paragraph(chapter_data['chapter_title'], self.chapter_style))
                story.append(Spacer(1, 20))
                for para in chapter_data['content'].split('\n\n'):
                    if para.strip():
                        story.append(Paragraph(para.strip(), self.body_style))
                        story.append(Spacer(1, 12))
                story.append(PageBreak())

            if 'back_cover_blurb' in book_data:
                story.append(Paragraph("About the Book", self.chapter_style))
                story.append(Spacer(1, 20))
                story.append(Paragraph(book_data['back_cover_blurb'], self.body_style))

            doc.build(story)

            # STEP 2 — Draw the cover image into a separate PDF
            c = pdf_canvas.Canvas(temp_cover_path, pagesize=letter)
            width, height = letter

            if 'cover_path' in book_data and os.path.exists(book_data['cover_path']):
                cover_image = ImageReader(book_data['cover_path'])
                c.drawImage(cover_image, 0, 0, width=width, height=height, preserveAspectRatio=False, mask='auto')
            else:
                c.setFillColor(colors.lightgrey)
                c.rect(0, 0, width, height, fill=1)
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 24)
                c.drawCentredString(width / 2, height / 2, "Missing Cover Image")

            c.showPage()
            c.save()

            # STEP 3 — Combine into final output_path cleanly
            final_writer = PdfWriter()
            final_writer.append(PdfReader(temp_cover_path))      # cover
            final_writer.append(PdfReader(temp_story_path))      # story
            with open(output_path, "wb") as f_out:
                final_writer.write(f_out)

            # Optional: cleanup temp files
            os.remove(temp_story_path)
            os.remove(temp_cover_path)

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
            
            os.environ["PATH"] += os.pathsep + r"C:\Program Files\Calibre2"
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
    
    # def add_text_to_cover(self, cover_path: str, title: str, author: str, output_path: str) -> str:
    #     """Add text overlay to cover image"""
    #     try:
    #         # Open the cover image
    #         with Image.open(cover_path) as img:
    #             # Create a copy to work with
    #             cover = img.copy()
                
    #             # Create a drawing object
    #             draw = ImageDraw.Draw(cover)
                
    #             # Try to load a font, fall back to default if not available
    #             try:
    #                 # Try to use a nice font if available
    #                 title_font = ImageFont.truetype("arial.ttf", 60)
    #                 author_font = ImageFont.truetype("arial.ttf", 40)
    #             except:
    #                 # Fall back to default font
    #                 title_font = ImageFont.load_default()
    #                 author_font = ImageFont.load_default()
                
    #             # Get image dimensions
    #             width, height = cover.size
                
    #             # Calculate text positions (centered)
    #             title_bbox = draw.textbbox((0, 0), title, font=title_font)
    #             title_width = title_bbox[2] - title_bbox[0]
    #             title_x = (width - title_width) // 2
    #             title_y = height // 4
                
    #             author_bbox = draw.textbbox((0, 0), author, font=author_font)
    #             author_width = author_bbox[2] - author_bbox[0]
    #             author_x = (width - author_width) // 2
    #             author_y = title_y + 80
                
    #             # Add text with outline for better visibility
    #             # Draw outline
    #             outline_color = (0, 0, 0)
    #             text_color = (255, 255, 255)
                
    #             # Title outline
    #             for dx in [-2, -1, 0, 1, 2]:
    #                 for dy in [-2, -1, 0, 1, 2]:
    #                     if dx != 0 or dy != 0:
    #                         draw.text((title_x + dx, title_y + dy), title, font=title_font, fill=outline_color)
                
    #             # Title text
    #             draw.text((title_x, title_y), title, font=title_font, fill=text_color)
                
    #             # Author outline
    #             for dx in [-2, -1, 0, 1, 2]:
    #                 for dy in [-2, -1, 0, 1, 2]:
    #                     if dx != 0 or dy != 0:
    #                         draw.text((author_x + dx, author_y + dy), author, font=author_font, fill=outline_color)
                
    #             # Author text
    #             draw.text((author_x, author_y), author, font=author_font, fill=text_color)
                
    #             # Save the modified cover
    #             cover.save(output_path, 'PNG')
                
    #             logger.info(f"Added text to cover: {output_path}")
    #             return output_path
                
    #     except Exception as e:
    #         logger.error(f"Error adding text to cover: {e}")
    #         # Return original cover path if modification fails
    #         return cover_path
    
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
                
                # Function to wrap text
                def wrap_text(text, font, max_width):
                    words = text.split()
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        test_line = current_line + " " + word if current_line else word
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        test_width = bbox[2] - bbox[0]
                        
                        if test_width <= max_width:
                            current_line = test_line
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = word
                    
                    if current_line:
                        lines.append(current_line)
                    
                    return lines
                
                # Wrap title text (use 80% of image width)
                max_title_width = int(width * 0.8)
                title_lines = wrap_text(title, title_font, max_title_width)
                
                # Calculate text positions (centered)
                title_y = height // 4
                line_height = 70  # Adjust based on font size
                
                # Draw title lines
                for i, line in enumerate(title_lines):
                    bbox = draw.textbbox((0, 0), line, font=title_font)
                    line_width = bbox[2] - bbox[0]
                    title_x = (width - line_width) // 2
                    line_y = title_y + (i * line_height)
                    
                    # Title outline
                    outline_color = (0, 0, 0)
                    text_color = (255, 255, 255)
                    
                    for dx in [-2, -1, 0, 1, 2]:
                        for dy in [-2, -1, 0, 1, 2]:
                            if dx != 0 or dy != 0:
                                draw.text((title_x + dx, line_y + dy), line, font=title_font, fill=outline_color)
                    
                    # Title text
                    draw.text((title_x, line_y), line, font=title_font, fill=text_color)
                
                # Calculate author position (below the last title line)
                author_bbox = draw.textbbox((0, 0), author, font=author_font)
                author_width = author_bbox[2] - author_bbox[0]
                author_x = (width - author_width) // 2
                author_y = title_y + (len(title_lines) * line_height) + 20
                
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
                        back_cover_blurb: str, cover_path: str) -> Dict:
        """Format all book data into a structured format for formatting"""
        book_data = {
            'title': outline['title'],
            'genre': concept['niche'],
            'subgenre': concept['subgenre'],
            'word_count': concept['word_count'],
            'synopsis': concept['concept_summary'],
            'cover_path': cover_path,
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
    
    def create_all_formats(self, book_data: Dict, output_dir: str, cover_path: str) -> Dict:
        """Create all book formats (EPUB, PDF, MOBI)"""
        os.makedirs(output_dir, exist_ok=True)
        
        book_title = book_data['title'].replace(' ', '_').replace(':', '').replace('?', '').replace('!', '')
        
        result = {'epub': '', 'pdf': '', 'mobi': ''}

        # --- EPUB ---
        try:
            epub_path = os.path.join(output_dir, f"{book_title}.epub")
            result['epub'] = self.create_epub(book_data, epub_path)
        except Exception as e:
            logger.error(f"Failed to create EPUB: {e}")

        # --- PDF ---
        try:
            pdf_path = os.path.join(output_dir, f"{book_title}.pdf")
            result['pdf'] = self.create_pdf(book_data, pdf_path)
        except Exception as e:
            logger.error(f"Failed to create PDF: {e}")

        # --- MOBI ---
        try:
            mobi_path = os.path.join(output_dir, f"{book_title}.mobi")
            if result['epub']:  # ensure EPUB exists first
                result['mobi'] = self.create_mobi(result['epub'], mobi_path)
            else:
                logger.warning("Skipping MOBI creation because EPUB was not generated.")
        except Exception as e:
            logger.error(f"Failed to create MOBI: {e}")
        
        return result

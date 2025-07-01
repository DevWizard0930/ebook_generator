#!/usr/bin/env python3
"""
J & M Publishing Automation - Demo Script
Demonstrates the system capabilities with sample data
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List
import logging

# Import our modules
from config import Config
from book_formatter import BookFormatter
from airtable_logger import AirtableLogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoBookBuilder:
    def __init__(self):
        self.book_formatter = BookFormatter()
        self.airtable_logger = AirtableLogger()
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for the demo"""
        directories = [
            Config.OUTPUT_DIR,
            Config.COVERS_DIR,
            Config.BOOKS_DIR,
            "screenshots",
            "logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_sample_concept(self) -> Dict:
        """Generate a sample book concept"""
        return {
            "niche": "Cozy Mystery",
            "subgenre": "Holiday Mystery",
            "hook": "A Christmas tree decorator discovers a murder weapon inside a vintage ornament box—and must solve the mystery before Christmas Eve.",
            "concept_summary": "Emily, a struggling florist in a snowy Vermont town, takes on a seasonal side job decorating holiday homes. But when she opens a delivery of antique ornaments and finds a bloody letter opener tucked inside, her quiet winter gig turns into a deadly puzzle. With the help of her retired-cop father and her charming bakery rival, Emily uncovers decades-old secrets buried under tinsel and mistletoe. As the snow falls, the mystery deepens—and time runs out before the killer strikes again.",
            "word_count": 17000,
            "chapter_count": 13
        }
    
    def generate_sample_outline(self) -> Dict:
        """Generate a sample book outline"""
        return {
            "title": "Tinsel and Tension",
            "chapters": [
                {
                    "chapter_number": 1,
                    "chapter_title": "The Delivery",
                    "summary": "Emily receives a mysterious box of antique Christmas ornaments, one of which contains a bloody letter opener. Her curiosity piqued, she begins asking around town."
                },
                {
                    "chapter_number": 2,
                    "chapter_title": "Tinsel and Tension",
                    "summary": "A visit to the antique shop reveals the ornaments were part of an estate sale from a woman who disappeared in the 80s. Emily senses this job may be more than festive cheer."
                },
                {
                    "chapter_number": 3,
                    "chapter_title": "Mistletoe and Mystery",
                    "summary": "Emily's retired-cop father helps her investigate the missing woman's case, uncovering connections to the town's wealthy founding family."
                },
                {
                    "chapter_number": 4,
                    "chapter_title": "Sugar and Spice",
                    "summary": "Emily's bakery rival, handsome Jake, offers to help with the investigation, but his family's past involvement in the case raises suspicions."
                },
                {
                    "chapter_number": 5,
                    "chapter_title": "Frost and Fear",
                    "summary": "A threatening note appears in Emily's shop, and she realizes someone doesn't want her digging into the past."
                },
                {
                    "chapter_number": 6,
                    "chapter_title": "Holly and Hiding",
                    "summary": "Emily discovers the missing woman was investigating the founding family's dark secrets before she vanished."
                },
                {
                    "chapter_number": 7,
                    "chapter_title": "Candy Canes and Clues",
                    "summary": "Jake's grandmother reveals she knew the missing woman and shares crucial information about the family's history."
                },
                {
                    "chapter_number": 8,
                    "chapter_title": "Snow and Secrets",
                    "summary": "Emily finds evidence that the missing woman is still alive and hiding in the town, protected by someone who knows the truth."
                },
                {
                    "chapter_number": 9,
                    "chapter_title": "Pine and Peril",
                    "summary": "The killer makes a move against Emily, but she's prepared with help from her father and Jake."
                },
                {
                    "chapter_number": 10,
                    "chapter_title": "Garland and Guilt",
                    "summary": "The truth about the founding family's crimes comes to light, and Emily must decide how to handle the revelation."
                },
                {
                    "chapter_number": 11,
                    "chapter_title": "Ornaments and Justice",
                    "summary": "Emily confronts the killer and rescues the missing woman, bringing the decades-old mystery to a close."
                },
                {
                    "chapter_number": 12,
                    "chapter_title": "Twinkle and Truth",
                    "summary": "The town comes together to celebrate Christmas and justice, while Emily and Jake's relationship deepens."
                },
                {
                    "chapter_number": 13,
                    "chapter_title": "Christmas and Closure",
                    "summary": "Emily reflects on her journey and the new life she's found in the small town, with love, family, and a future full of possibilities."
                }
            ],
            "keywords": [
                "cozy Christmas mystery",
                "small town secrets",
                "antique shop mystery",
                "missing person cold case",
                "female amateur sleuth",
                "holiday suspense with heart",
                "second chance healing romance"
            ]
        }
    
    def generate_sample_chapters(self) -> List[str]:
        """Generate sample chapter content"""
        chapters = []
        
        chapter_templates = [
            """Emily's breath formed little clouds in the crisp December air as she pulled up to the Victorian mansion on Maple Street. The job posting had been simple enough—decorate the house for Christmas, no questions asked, good pay. But as she stepped out of her beat-up van, she couldn't shake the feeling that something was off about this place.

The delivery truck had already been and gone, leaving a large cardboard box on the front porch. Emily approached it cautiously, her boots crunching on the fresh snow. The box was unmarked except for a handwritten note: "For the Christmas decorations. Handle with care."

She lifted the lid, and her heart stopped. Nestled among the delicate glass ornaments was a silver letter opener, its blade stained with what could only be dried blood. Emily's hands trembled as she stared at it, her mind racing with possibilities. This wasn't just a seasonal decorating job anymore—it was the beginning of a mystery that would change her life forever.""",
            
            """The antique shop on Main Street was exactly what Emily expected—dusty, cramped, and filled with the kind of treasures that held stories of their own. Mrs. Winthrop, the elderly proprietor, peered at her over wire-rimmed glasses as Emily showed her the ornaments.

"Those came from the old Henderson estate," Mrs. Winthrop said, her voice barely above a whisper. "Poor Margaret Henderson disappeared back in '87. Never found her, never found a body. Just... gone."

Emily felt a chill run down her spine. "What happened to her?"

"Some say she ran off with a lover. Others say the family had something to do with it. The Hendersons were always... private people. But Margaret was different. She was asking questions, digging into things that should have been left buried."

Emily looked at the ornaments with new eyes. These weren't just decorations—they were pieces of a puzzle that had been waiting thirty years to be solved.""",
            
            """"Dad, I need your help," Emily said, sitting down at her father's kitchen table. Retired Detective Mike Callahan looked up from his crossword puzzle, his sharp eyes immediately picking up on his daughter's distress.

"What's wrong, sweetheart?"

Emily pulled out the bloody letter opener and told him everything—the job, the ornaments, the missing woman. Her father's expression grew serious as he listened.

"Margaret Henderson," he said slowly. "I remember that case. I was just a rookie then, but I worked on it. We never found any evidence of foul play, but something about it never sat right with me."

He reached for the letter opener, examining it with a detective's eye. "This is silver, probably sterling. Expensive. And that stain... it's old, but it's definitely blood. Where did you say you found this?"

"In a box of Christmas ornaments, delivered to a house I'm supposed to decorate."

Her father's eyes narrowed. "Someone wanted you to find this. Someone who knows about Margaret's case and wants it reopened." He stood up, his old detective instincts kicking in. "Let's go to the station. I still have friends there who can help us investigate this properly.""""
        ]
        
        # Generate 13 chapters using the templates and variations
        for i in range(13):
            chapter_num = i + 1
            template = chapter_templates[i % len(chapter_templates)]
            
            # Add some variation to make each chapter unique
            chapter_content = f"""Chapter {chapter_num}

{template}

Emily's heart raced as she realized she was getting closer to the truth. The small town of Maplewood held secrets that had been buried for decades, and she was determined to uncover them all. With her father's help and the growing support of the community, she knew she could solve this mystery and bring justice to Margaret Henderson.

But time was running out. Christmas was approaching, and with it came the deadline for her decorating job. She had to work quickly, carefully, and above all, stay alive long enough to see the case through to its conclusion.

The snow continued to fall outside, covering the town in a blanket of white that seemed to hide as much as it revealed. Emily knew that beneath that pristine surface lay the answers she was looking for—and the danger that came with them."""
            
            chapters.append(chapter_content)
        
        return chapters
    
    def generate_sample_back_cover_blurb(self) -> str:
        """Generate a sample back cover blurb"""
        return """When struggling florist Emily Callahan takes on a seasonal job decorating a Victorian mansion for Christmas, she expects nothing more than a paycheck and some festive cheer. But when she opens a delivery of antique ornaments and finds a bloody letter opener tucked inside, her quiet winter gig turns into a deadly puzzle.

With the help of her retired-cop father and her charming bakery rival Jake, Emily uncovers decades-old secrets buried under tinsel and mistletoe. As the snow falls and Christmas approaches, the mystery deepens—and time runs out before the killer strikes again.

A heartwarming holiday mystery that combines the charm of small-town life with the thrill of amateur sleuthing, Tinsel and Tension is perfect for fans of cozy mysteries and holiday romance."""
    
    def create_sample_cover(self) -> str:
        """Create a sample cover image (placeholder)"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple placeholder cover
            cover = Image.new('RGB', (1024, 1536), color='darkgreen')
            draw = ImageDraw.Draw(cover)
            
            # Add some decorative elements
            draw.rectangle([100, 100, 924, 1436], outline='gold', width=5)
            draw.rectangle([150, 150, 874, 1386], outline='white', width=3)
            
            # Add title
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            title = "Tinsel and Tension"
            author = "AI Author"
            
            # Calculate text positions
            title_bbox = draw.textbbox((0, 0), title, font=font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (1024 - title_width) // 2
            title_y = 1536 // 4
            
            # Draw title with outline
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((title_x + dx, title_y + dy), title, font=font, fill='black')
            
            draw.text((title_x, title_y), title, font=font, fill='white')
            
            # Add author
            author_y = title_y + 100
            author_bbox = draw.textbbox((0, 0), author, font=font)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = (1024 - author_width) // 2
            
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        draw.text((author_x + dx, author_y + dy), author, font=font, fill='black')
            
            draw.text((author_x, author_y), author, font=font, fill='white')
            
            # Add "DEMO" watermark
            draw.text((50, 50), "DEMO VERSION", font=font, fill='red')
            
            # Save the cover
            cover_path = os.path.join(Config.COVERS_DIR, "demo_cover.png")
            cover.save(cover_path)
            
            logger.info(f"Created demo cover: {cover_path}")
            return cover_path
            
        except Exception as e:
            logger.error(f"Error creating demo cover: {e}")
            return ""
    
    def run_demo(self) -> Dict:
        """Run the complete demo process"""
        logger.info("=== STARTING DEMO BOOK BUILDING PROCESS ===")
        total_start_time = time.time()
        
        try:
            # Step 1: Generate sample concept
            logger.info("=== STEP 1: Generating Sample Concept ===")
            concept = self.generate_sample_concept()
            logger.info(f"Generated concept: {concept['niche']} - {concept['hook']}")
            
            # Step 2: Generate sample outline
            logger.info("=== STEP 2: Generating Sample Outline ===")
            outline = self.generate_sample_outline()
            logger.info(f"Generated title: {outline['title']}")
            logger.info(f"Generated {len(outline['chapters'])} chapters")
            
            # Step 3: Generate sample chapters
            logger.info("=== STEP 3: Generating Sample Chapters ===")
            chapters = self.generate_sample_chapters()
            logger.info(f"Generated {len(chapters)} chapters")
            
            # Step 4: Generate sample back cover blurb
            logger.info("=== STEP 4: Generating Sample Back Cover Blurb ===")
            back_cover_blurb = self.generate_sample_back_cover_blurb()
            logger.info(f"Generated back cover blurb ({len(back_cover_blurb)} characters)")
            
            # Step 5: Create sample cover
            logger.info("=== STEP 5: Creating Sample Cover ===")
            cover_path = self.create_sample_cover()
            logger.info(f"Created cover: {cover_path}")
            
            # Step 6: Format book files
            logger.info("=== STEP 6: Formatting Book Files ===")
            book_files = self.book_formatter.format_book_files(
                concept=concept,
                outline=outline,
                chapters=chapters,
                back_cover_blurb=back_cover_blurb,
                cover_path=cover_path
            )
            logger.info(f"Created book files: {list(book_files.keys())}")
            
            # Step 7: Create backup log
            logger.info("=== STEP 7: Creating Backup Log ===")
            book_data = {
                'title': outline['title'],
                'synopsis': concept['concept_summary'],
                'genre': concept['niche'],
                'word_count': concept['word_count'],
                'back_cover_blurb': back_cover_blurb
            }
            
            backup_log_path = os.path.join(Config.OUTPUT_DIR, f"demo_{outline['title'].replace(' ', '_')}_backup.json")
            self.airtable_logger.create_backup_log(book_data, backup_log_path)
            
            # Calculate total time
            total_time = time.time() - total_start_time
            
            # Prepare result
            result = {
                'success': True,
                'book_title': outline['title'],
                'genre': concept['niche'],
                'word_count': concept['word_count'],
                'total_time': total_time,
                'files': book_files,
                'cover_path': cover_path,
                'backup_log': backup_log_path
            }
            
            logger.info("=== DEMO BOOK BUILDING PROCESS COMPLETED ===")
            logger.info(f"Book: {outline['title']}")
            logger.info(f"Genre: {concept['niche']}")
            logger.info(f"Word Count: {concept['word_count']}")
            logger.info(f"Total Time: {total_time:.2f} seconds")
            logger.info(f"Files Created: {list(book_files.keys())}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in demo process: {e}")
            total_time = time.time() - total_start_time
            
            return {
                'success': False,
                'error': str(e),
                'total_time': total_time
            }

def main():
    """Main demo function"""
    print("🎄 J & M Publishing Automation - Demo Mode 🎄")
    print("=" * 50)
    print("This demo showcases the system capabilities with sample data.")
    print("No API calls or external services are required.")
    print("=" * 50)
    
    # Initialize demo builder
    demo_builder = DemoBookBuilder()
    
    try:
        # Run the demo
        result = demo_builder.run_demo()
        
        if result['success']:
            print(f"\n✅ Demo book successfully created: {result['book_title']}")
            print(f"📚 Genre: {result['genre']}")
            print(f"📝 Word Count: {result['word_count']}")
            print(f"⏱️  Total Time: {result['total_time']:.2f} seconds")
            print(f"📁 Files: {list(result['files'].keys())}")
            print(f"🖼️  Cover: {result['cover_path']}")
            print(f"📊 Backup Log: {result['backup_log']}")
            
            print(f"\n📂 Check the following directories for generated files:")
            print(f"   - {Config.BOOKS_DIR}/")
            print(f"   - {Config.COVERS_DIR}/")
            print(f"   - {Config.OUTPUT_DIR}/")
            
            print(f"\n🎯 Demo completed successfully!")
            print(f"   This demonstrates the complete book generation pipeline")
            print(f"   without requiring any external API calls or services.")
        else:
            print(f"\n❌ Demo failed: {result['error']}")
            print(f"⏱️  Time spent: {result['total_time']:.2f} seconds")
    
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error in demo: {e}")

if __name__ == "__main__":
    main() 
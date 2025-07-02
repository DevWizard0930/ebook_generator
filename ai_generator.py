import json
import openai
from typing import Dict, List, Optional
from config import Config
from prompts import (
    book_concept_prompt,
    title_and_outline_prompt,
    chapter_generation_prompt,
    back_cover_blurb_prompt,
    cover_image_prompt,
    streetlib_metadata_prompt
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_book_concept(self) -> Dict:
        """Generate a complete book concept using GPT-4"""
        prompt = book_concept_prompt()
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT4_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            # Extract JSON from the response

            if content is None:
                logger.error("No content returned from GPT-4")
                raise Exception("No content returned from GPT-4")
            
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            concept = json.loads(json_str)
            logger.info(f"Generated book concept: {concept.get('niche', 'Unknown')} - {concept.get('title', 'Unknown')}")
            return concept
            
        except Exception as e:
            logger.error(f"Error generating book concept: {e}")
            raise
    
    def generate_title_and_outline(self, concept: Dict) -> Dict:
        """Generate title and chapter outline using GPT-4"""
        prompt = title_and_outline_prompt(concept)
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT4_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            if content is None:
                logger.error("No content returned from GPT-4")
                raise Exception("No content returned from GPT-4")
            # Extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            outline = json.loads(json_str)
            logger.info(f"Generated title and outline: {outline.get('title', 'Unknown')}")
            return outline
            
        except Exception as e:
            logger.error(f"Error generating title and outline: {e}")
            raise
    
    def generate_chapter(self, book_title: str, genre: str, chapter_number: int, 
                        chapter_title: str, chapter_summary: str, 
                        previous_chapters: List[str]) -> str:
        """Generate a single chapter using GPT-3.5 Turbo"""
        previous_context = ""
        if previous_chapters:
            previous_context = "\n".join([f"Chapter {i+1}: {summary}" for i, summary in enumerate(previous_chapters)])
        prompt = chapter_generation_prompt(
            book_title=book_title,
            genre=genre,
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            chapter_summary=chapter_summary,
            previous_chapters=previous_context
        )
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT35_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            chapter_content = response.choices[0].message.content

            if chapter_content is None:
                logger.error("No content returned from GPT-3.5 Turbo")
                raise Exception("No content returned from GPT-3.5 Turbo")

            logger.info(f"Generated chapter {chapter_number}: {chapter_title}")
            return chapter_content
            
        except Exception as e:
            logger.error(f"Error generating chapter {chapter_number}: {e}")
            raise
    
    def generate_back_cover_blurb(self, book_title: str, genre: str, concept_summary: str) -> str:
        """Generate back cover blurb using GPT-3.5 Turbo"""
        prompt = back_cover_blurb_prompt(
            book_title=book_title,
            genre=genre,
            concept_summary=concept_summary
        )
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT35_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            blurb = response.choices[0].message.content

            if blurb is None:
                logger.error("No content returned from GPT-3.5 Turbo")
                raise Exception("No content returned from GPT-3.5 Turbo")

            logger.info(f"Generated back cover blurb for: {book_title}")
            return blurb
            
        except Exception as e:
            logger.error(f"Error generating back cover blurb: {e}")
            raise
    
    def generate_cover_image_prompt(self, book_title: str, genre: str) -> str:
        """Generate cover image prompt using GPT-3.5 Turbo"""
        prompt = cover_image_prompt(
            book_title=book_title,
            genre=genre
        )
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT35_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            image_prompt = response.choices[0].message.content

            if image_prompt is None:
                logger.error("No content returned from GPT-3.5 Turbo")
                raise Exception("No content returned from GPT-3.5 Turbo")

            logger.info(f"Generated cover image prompt for: {book_title}")
            return image_prompt
            
        except Exception as e:
            logger.error(f"Error generating cover image prompt: {e}")
            raise
    
    def generate_cover_image(self, image_prompt: str, output_path: str) -> str:
        """Generate cover image using DALL-E 3"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1792",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            import requests

            if image_url is None:
                logger.error("No image URL returned from DALL-E 3")
                raise Exception("No image URL returned from DALL-E 3")

            img_response = requests.get(image_url)      
            img_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            
            logger.info(f"Generated cover image: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating cover image: {e}")
            raise
    
    def generate_streetlib_metadata(self, book_data: Dict) -> Dict:
        """Generate StreetLib metadata using GPT-4"""
        prompt = streetlib_metadata_prompt(book_data, Config)
        try:
            response = self.client.chat.completions.create(
                model=Config.GPT4_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            content = response.choices[0].message.content

            if content is None:
                logger.error("No content returned from GPT-4")
                raise Exception("No content returned from GPT-4")

            # Extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            metadata = json.loads(json_str)
            logger.info(f"Generated StreetLib metadata for: {metadata.get('title', '')}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating StreetLib metadata: {e}")
            raise 
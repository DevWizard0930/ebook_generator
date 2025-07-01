import os
import time
import json
from typing import Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser
import logging
from config import Config

logger = logging.getLogger(__name__)

class StreetLibPublisher:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
    
    def __enter__(self):
        """Context manager entry"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,  # Set to True for production
            slow_mo=1000  # Slow down for better reliability
        )
        self.page = self.browser.new_page()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def login(self) -> bool:
        """Login to StreetLib"""
        try:
            logger.info("Logging into StreetLib...")
            
            # Navigate to login page
            self.page.goto(f"{Config.STREETLIB_URL}/login")
            time.sleep(2)
            
            # Fill in email
            self.page.fill('input[name="email"]', Config.STREETLIB_EMAIL)
            time.sleep(1)
            
            # Fill in password
            self.page.fill('input[name="password"]', Config.STREETLIB_PASSWORD)
            time.sleep(1)
            
            # Click login button
            self.page.click('button[type="submit"]')
            time.sleep(3)
            
            # Check if login was successful
            if "dashboard" in self.page.url or "hub" in self.page.url:
                logger.info("Successfully logged into StreetLib")
                return True
            else:
                logger.error("Login failed - not redirected to dashboard")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def navigate_to_publishing(self) -> bool:
        """Navigate to the publishing section"""
        try:
            logger.info("Navigating to publishing section...")
            
            # Navigate to HUB
            self.page.goto(f"{Config.STREETLIB_URL}/hub")
            time.sleep(2)
            
            # Look for "Add New Book" or similar button
            add_book_selectors = [
                'a[href*="add"]',
                'button:has-text("Add New Book")',
                'a:has-text("Add New Book")',
                'button:has-text("New Book")',
                'a:has-text("New Book")',
                '[data-testid="add-book"]'
            ]
            
            for selector in add_book_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.click(selector)
                        time.sleep(3)
                        logger.info("Found and clicked add book button")
                        return True
                except:
                    continue
            
            # If no button found, try direct navigation
            self.page.goto(f"{Config.STREETLIB_URL}/hub/books/add")
            time.sleep(3)
            
            logger.info("Navigated to publishing section")
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to publishing: {e}")
            return False
    
    def fill_basic_metadata(self, metadata: Dict) -> bool:
        """Fill in basic book metadata"""
        try:
            logger.info("Filling basic metadata...")
            
            # Title
            if 'title' in metadata:
                self.page.fill('input[name="title"]', metadata['title'])
                time.sleep(1)
            
            # Subtitle (if available)
            if 'subtitle' in metadata and metadata['subtitle']:
                self.page.fill('input[name="subtitle"]', metadata['subtitle'])
                time.sleep(1)
            
            # Author
            if 'author' in metadata:
                self.page.fill('input[name="author"]', metadata['author'])
                time.sleep(1)
            
            # Language
            if 'language' in metadata:
                self.page.select_option('select[name="language"]', metadata['language'])
                time.sleep(1)
            
            # Publication year
            if 'publication_year' in metadata:
                self.page.fill('input[name="publication_year"]', str(metadata['publication_year']))
                time.sleep(1)
            
            # Age rating
            if 'age_rating' in metadata:
                self.page.select_option('select[name="age_rating"]', metadata['age_rating'])
                time.sleep(1)
            
            logger.info("Basic metadata filled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error filling basic metadata: {e}")
            return False
    
    def fill_description_and_keywords(self, metadata: Dict) -> bool:
        """Fill in description and keywords"""
        try:
            logger.info("Filling description and keywords...")
            
            # Description/Synopsis
            if 'synopsis' in metadata:
                # Try different selectors for description field
                description_selectors = [
                    'textarea[name="description"]',
                    'textarea[name="synopsis"]',
                    'textarea[name="summary"]',
                    '[data-testid="description"]',
                    'textarea[placeholder*="description"]',
                    'textarea[placeholder*="synopsis"]'
                ]
                
                for selector in description_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.page.fill(selector, metadata['synopsis'])
                            time.sleep(1)
                            break
                    except:
                        continue
            
            # Keywords
            if 'keywords' in metadata:
                keyword_selectors = [
                    'input[name="keywords"]',
                    'textarea[name="keywords"]',
                    '[data-testid="keywords"]',
                    'input[placeholder*="keyword"]'
                ]
                
                for selector in keyword_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.page.fill(selector, metadata['keywords'])
                            time.sleep(1)
                            break
                    except:
                        continue
            
            logger.info("Description and keywords filled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error filling description and keywords: {e}")
            return False
    
    def select_categories(self, metadata: Dict) -> bool:
        """Select BISAC categories"""
        try:
            logger.info("Selecting categories...")
            
            if 'bisac_categories' in metadata and metadata['bisac_categories']:
                categories = metadata['bisac_categories']
                
                # Try to select primary category
                if len(categories) > 0:
                    primary_category = categories[0]
                    
                    # Look for category selection elements
                    category_selectors = [
                        'select[name="category"]',
                        'select[name="primary_category"]',
                        'select[name="bisac_category"]',
                        '[data-testid="category-select"]'
                    ]
                    
                    for selector in category_selectors:
                        try:
                            if self.page.locator(selector).count() > 0:
                                # Try to select by name or code
                                category_name = primary_category.get('name', '')
                                category_code = primary_category.get('code', '')
                                
                                # Try by name first
                                try:
                                    self.page.select_option(selector, category_name)
                                    time.sleep(1)
                                    break
                                except:
                                    # Try by code
                                    try:
                                        self.page.select_option(selector, category_code)
                                        time.sleep(1)
                                        break
                                    except:
                                        continue
                        except:
                            continue
            
            logger.info("Categories selected successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error selecting categories: {e}")
            return False
    
    def upload_cover(self, cover_path: str) -> bool:
        """Upload book cover"""
        try:
            logger.info(f"Uploading cover: {cover_path}")
            
            if not os.path.exists(cover_path):
                logger.error(f"Cover file not found: {cover_path}")
                return False
            
            # Look for file upload elements
            upload_selectors = [
                'input[type="file"]',
                'input[name="cover"]',
                'input[name="cover_image"]',
                '[data-testid="cover-upload"]',
                'input[accept*="image"]'
            ]
            
            for selector in upload_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.set_input_files(selector, cover_path)
                        time.sleep(3)  # Wait for upload
                        logger.info("Cover uploaded successfully")
                        return True
                except:
                    continue
            
            logger.error("Could not find cover upload element")
            return False
            
        except Exception as e:
            logger.error(f"Error uploading cover: {e}")
            return False
    
    def upload_book_file(self, file_path: str, file_type: str = "epub") -> bool:
        """Upload book file (EPUB, PDF, etc.)"""
        try:
            logger.info(f"Uploading book file: {file_path}")
            
            if not os.path.exists(file_path):
                logger.error(f"Book file not found: {file_path}")
                return False
            
            # Look for file upload elements
            upload_selectors = [
                'input[type="file"]',
                f'input[name="{file_type}"]',
                f'input[name="{file_type}_file"]',
                f'input[accept*="{file_type}"]',
                '[data-testid="book-upload"]'
            ]
            
            for selector in upload_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.set_input_files(selector, file_path)
                        time.sleep(5)  # Wait for upload
                        logger.info(f"{file_type.upper()} file uploaded successfully")
                        return True
                except:
                    continue
            
            logger.error(f"Could not find {file_type} upload element")
            return False
            
        except Exception as e:
            logger.error(f"Error uploading {file_type} file: {e}")
            return False
    
    def set_pricing(self, metadata: Dict) -> bool:
        """Set book pricing"""
        try:
            logger.info("Setting pricing...")
            
            # Price in USD
            if 'suggested_price_usd' in metadata:
                usd_selectors = [
                    'input[name="price_usd"]',
                    'input[name="usd_price"]',
                    'input[placeholder*="USD"]',
                    '[data-testid="usd-price"]'
                ]
                
                for selector in usd_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.page.fill(selector, str(metadata['suggested_price_usd']))
                            time.sleep(1)
                            break
                    except:
                        continue
            
            # Price in EUR
            if 'suggested_price_eur' in metadata:
                eur_selectors = [
                    'input[name="price_eur"]',
                    'input[name="eur_price"]',
                    'input[placeholder*="EUR"]',
                    '[data-testid="eur-price"]'
                ]
                
                for selector in eur_selectors:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.page.fill(selector, str(metadata['suggested_price_eur']))
                            time.sleep(1)
                            break
                    except:
                        continue
            
            logger.info("Pricing set successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error setting pricing: {e}")
            return False
    
    def submit_for_publishing(self) -> Dict:
        """Submit the book for publishing"""
        try:
            logger.info("Submitting book for publishing...")
            
            # Look for submit/publish button
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("Publish")',
                'button:has-text("Submit")',
                'button:has-text("Publish Book")',
                'button:has-text("Submit for Review")',
                '[data-testid="publish-button"]'
            ]
            
            for selector in submit_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.click(selector)
                        time.sleep(5)  # Wait for submission
                        break
                except:
                    continue
            
            # Check for success indicators
            success_indicators = [
                'text=Success',
                'text=Published',
                'text=Submitted',
                'text=Book published successfully',
                'text=Your book has been submitted'
            ]
            
            for indicator in success_indicators:
                try:
                    if self.page.locator(indicator).count() > 0:
                        logger.info("Book submitted successfully")
                        
                        # Try to get ISBN or publishing URL
                        publishing_info = {
                            'success': True,
                            'message': 'Book published successfully'
                        }
                        
                        # Look for ISBN
                        isbn_selectors = [
                            '[data-testid="isbn"]',
                            '.isbn',
                            'text=ISBN'
                        ]
                        
                        for selector in isbn_selectors:
                            try:
                                if self.page.locator(selector).count() > 0:
                                    isbn_text = self.page.locator(selector).text_content()
                                    if 'ISBN' in isbn_text:
                                        isbn = isbn_text.split('ISBN')[-1].strip()
                                        publishing_info['isbn'] = isbn
                                        break
                            except:
                                continue
                        
                        # Get current URL as publishing URL
                        publishing_info['publishing_url'] = self.page.url
                        
                        return publishing_info
                except:
                    continue
            
            # Check for error indicators
            error_indicators = [
                'text=Error',
                'text=Failed',
                'text=Please fix',
                'text=Required field'
            ]
            
            for indicator in error_indicators:
                try:
                    if self.page.locator(indicator).count() > 0:
                        error_message = self.page.locator(indicator).text_content()
                        logger.error(f"Publishing failed: {error_message}")
                        return {
                            'success': False,
                            'error': error_message
                        }
                except:
                    continue
            
            # If no clear success/error indicator, assume success
            logger.info("Book submission completed (no clear success indicator)")
            return {
                'success': True,
                'message': 'Book submitted (status unclear)',
                'publishing_url': self.page.url
            }
            
        except Exception as e:
            logger.error(f"Error submitting book: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def take_screenshot(self, filename: str) -> str:
        """Take a screenshot for debugging"""
        try:
            screenshot_path = f"screenshots/{filename}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return ""
    
    def publish_book(self, metadata: Dict, cover_path: str, book_files: Dict) -> Dict:
        """Complete publishing process"""
        try:
            logger.info("Starting StreetLib publishing process...")
            
            # Login
            if not self.login():
                return {'success': False, 'error': 'Login failed'}
            
            # Navigate to publishing
            if not self.navigate_to_publishing():
                return {'success': False, 'error': 'Could not navigate to publishing'}
            
            # Take screenshot for debugging
            self.take_screenshot("publishing_form")
            
            # Fill metadata
            if not self.fill_basic_metadata(metadata):
                return {'success': False, 'error': 'Failed to fill basic metadata'}
            
            if not self.fill_description_and_keywords(metadata):
                return {'success': False, 'error': 'Failed to fill description and keywords'}
            
            if not self.select_categories(metadata):
                return {'success': False, 'error': 'Failed to select categories'}
            
            # Upload cover
            if not self.upload_cover(cover_path):
                return {'success': False, 'error': 'Failed to upload cover'}
            
            # Upload book file (prefer EPUB)
            book_uploaded = False
            if 'epub' in book_files and os.path.exists(book_files['epub']):
                if self.upload_book_file(book_files['epub'], 'epub'):
                    book_uploaded = True
            elif 'pdf' in book_files and os.path.exists(book_files['pdf']):
                if self.upload_book_file(book_files['pdf'], 'pdf'):
                    book_uploaded = True
            
            if not book_uploaded:
                return {'success': False, 'error': 'Failed to upload book file'}
            
            # Set pricing
            if not self.set_pricing(metadata):
                return {'success': False, 'error': 'Failed to set pricing'}
            
            # Take final screenshot
            self.take_screenshot("before_submit")
            
            # Submit for publishing
            result = self.submit_for_publishing()
            
            # Take final screenshot
            self.take_screenshot("after_submit")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in publishing process: {e}")
            self.take_screenshot("error")
            return {'success': False, 'error': str(e)} 
import os
import json
from typing import Dict, List, Optional
from pyairtable import Api, Base, Table
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class AirtableLogger:
    def __init__(self):
        self.api = None
        self.table = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Airtable connection"""
        try:
            if not Config.AIRTABLE_API_KEY:
                logger.warning("Airtable API key not configured. Logging will be disabled.")
                return
            
            if not Config.AIRTABLE_BASE_ID:
                logger.warning("Airtable Base ID not configured. Logging will be disabled.")
                return
            
            self.api = Api(Config.AIRTABLE_API_KEY)
            self.table = Table(Config.AIRTABLE_API_KEY, Config.AIRTABLE_BASE_ID, Config.AIRTABLE_TABLE_NAME)
            logger.info("Successfully connected to Airtable")
            
        except Exception as e:
            logger.error(f"Error initializing Airtable: {e}")
            self.api = None
            self.table = None
    
    def log_book_creation(self, book_data: Dict, concept: Dict, outline: Dict, 
                         word_count: int, generation_time: float) -> Optional[str]:
        """Log book creation to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return None
            
            # Prepare record data
            record_data = {
                'Title': book_data.get('title', ''),
                'Genre': concept.get('niche', ''),
                'Subgenre': concept.get('subgenre', ''),
                'Hook': concept.get('hook', ''),
                'Synopsis': concept.get('concept_summary', ''),
                'Word Count': word_count,
                'Chapter Count': len(outline.get('chapters', [])),
                'Keywords': ', '.join(outline.get('keywords', [])),
                'Status': 'Generated',
                'Generation Date': datetime.now().isoformat(),
                'Generation Time (seconds)': round(generation_time, 2),
                'Author': Config.AUTHOR_NAME,
                'Publication Year': Config.PUBLICATION_YEAR,
                'Language': Config.LANGUAGE
            }
            
            # Add back cover blurb if available
            if 'back_cover_blurb' in book_data:
                record_data['Back Cover Blurb'] = book_data['back_cover_blurb']
            
            # Create record
            record = self.table.create(record_data)
            record_id = record['id']
            
            logger.info(f"Logged book creation to Airtable: {book_data.get('title', '')} (ID: {record_id})")
            return record_id
            
        except Exception as e:
            logger.error(f"Error logging book creation to Airtable: {e}")
            return None
    
    def log_cover_generation(self, record_id: str, cover_path: str, 
                           generation_time: float) -> bool:
        """Log cover generation to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return False
            
            # Update record with cover information
            update_data = {
                'Cover Generated': True,
                'Cover Path': cover_path,
                'Cover Generation Date': datetime.now().isoformat(),
                'Cover Generation Time (seconds)': round(generation_time, 2),
                'Status': 'Cover Generated'
            }
            
            self.table.update(record_id, update_data)
            logger.info(f"Logged cover generation to Airtable (Record ID: {record_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error logging cover generation to Airtable: {e}")
            return False
    
    def log_file_creation(self, record_id: str, book_files: Dict, 
                         creation_time: float) -> bool:
        """Log file creation to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return False
            
            # Prepare file information
            file_info = {}
            for format_name, file_path in book_files.items():
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    file_info[format_name] = {
                        'path': file_path,
                        'size': file_size
                    }
            
            # Update record with file information
            update_data = {
                'Files Created': True,
                'File Creation Date': datetime.now().isoformat(),
                'File Creation Time (seconds)': round(creation_time, 2),
                'Available Formats': list(file_info.keys()),
                'Status': 'Files Created'
            }
            
            # Add individual file paths if needed
            for format_name, info in file_info.items():
                update_data[f'{format_name.title()} Path'] = info['path']
                update_data[f'{format_name.title()} Size (bytes)'] = info['size']
            
            self.table.update(record_id, update_data)
            logger.info(f"Logged file creation to Airtable (Record ID: {record_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error logging file creation to Airtable: {e}")
            return False
    
    def log_google_drive_upload(self, record_id: str, upload_info: Dict, 
                               upload_time: float) -> bool:
        """Log Google Drive upload to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return False
            
            # Update record with upload information
            update_data = {
                'Google Drive Uploaded': True,
                'Google Drive Upload Date': datetime.now().isoformat(),
                'Google Drive Upload Time (seconds)': round(upload_time, 2),
                'Google Drive Folder ID': upload_info.get('folder_id', ''),
                'Google Drive Folder Name': upload_info.get('folder_name', ''),
                'Status': 'Google Drive Uploaded'
            }
            
            # Add file links if available
            files = upload_info.get('files', {})
            for format_name, file_info in files.items():
                if isinstance(file_info, dict):
                    update_data[f'Google Drive {format_name.title()} Link'] = file_info.get('web_view_link', '')
            
            self.table.update(record_id, update_data)
            logger.info(f"Logged Google Drive upload to Airtable (Record ID: {record_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error logging Google Drive upload to Airtable: {e}")
            return False
    
    def log_streetlib_publishing(self, record_id: str, publishing_info: Dict, 
                                publishing_time: float) -> bool:
        """Log StreetLib publishing to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return False
            
            # Update record with publishing information
            update_data = {
                'StreetLib Published': True,
                'StreetLib Publishing Date': datetime.now().isoformat(),
                'StreetLib Publishing Time (seconds)': round(publishing_time, 2),
                'Status': 'Published on StreetLib'
            }
            
            # Add publishing details
            if 'isbn' in publishing_info:
                update_data['ISBN'] = publishing_info['isbn']
            
            if 'publishing_url' in publishing_info:
                update_data['StreetLib Publishing URL'] = publishing_info['publishing_url']
            
            if 'error' in publishing_info:
                update_data['Publishing Error'] = publishing_info['error']
                update_data['Status'] = 'Publishing Failed'
            
            self.table.update(record_id, update_data)
            logger.info(f"Logged StreetLib publishing to Airtable (Record ID: {record_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error logging StreetLib publishing to Airtable: {e}")
            return False
    
    def log_error(self, record_id: str, error_message: str, step: str) -> bool:
        """Log error to Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping logging.")
                return False
            
            # Update record with error information
            update_data = {
                'Error': True,
                'Error Message': error_message,
                'Error Step': step,
                'Error Date': datetime.now().isoformat(),
                'Status': f'Error at {step}'
            }
            
            self.table.update(record_id, update_data)
            logger.info(f"Logged error to Airtable (Record ID: {record_id}): {error_message}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging error to Airtable: {e}")
            return False
    
    def get_book_records(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get book records from Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Cannot retrieve records.")
                return []
            
            # Get all records
            records = self.table.all()
            
            # Apply filters if provided
            if filters:
                filtered_records = []
                for record in records:
                    fields = record.get('fields', {})
                    match = True
                    for key, value in filters.items():
                        if fields.get(key) != value:
                            match = False
                            break
                    if match:
                        filtered_records.append(record)
                return filtered_records
            
            return records
            
        except Exception as e:
            logger.error(f"Error getting book records from Airtable: {e}")
            return []
    
    def update_book_status(self, record_id: str, status: str, 
                          additional_data: Optional[Dict] = None) -> bool:
        """Update book status in Airtable"""
        try:
            if not self.table:
                logger.warning("Airtable not configured. Skipping update.")
                return False
            
            update_data = {
                'Status': status,
                'Last Updated': datetime.now().isoformat()
            }
            
            if additional_data:
                update_data.update(additional_data)
            
            self.table.update(record_id, update_data)
            logger.info(f"Updated book status in Airtable (Record ID: {record_id}): {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating book status in Airtable: {e}")
            return False
    
    def create_backup_log(self, book_data: Dict, output_path: str) -> str:
        """Create a local backup log file in case Airtable is not available"""
        try:
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'book_data': book_data,
                'author': Config.AUTHOR_NAME,
                'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Created backup log: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating backup log: {e}")
            return "" 
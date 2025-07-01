import os
import json
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging
from config import Config

logger = logging.getLogger(__name__)

class GoogleDriveUploader:
    def __init__(self):
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            # If modifying these scopes, delete the file token.json.
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            # The file token.json stores the user's access and refresh tokens
            if os.path.exists(Config.GOOGLE_DRIVE_TOKEN_FILE):
                self.credentials = Credentials.from_authorized_user_file(
                    Config.GOOGLE_DRIVE_TOKEN_FILE, SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not os.path.exists(Config.GOOGLE_DRIVE_CREDENTIALS_FILE):
                        logger.error(f"Credentials file not found: {Config.GOOGLE_DRIVE_CREDENTIALS_FILE}")
                        logger.info("Please download credentials.json from Google Cloud Console")
                        return
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        Config.GOOGLE_DRIVE_CREDENTIALS_FILE, SCOPES)
                    self.credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(Config.GOOGLE_DRIVE_TOKEN_FILE, 'w') as token:
                    token.write(self.credentials.to_json())
            
            self.service = build('drive', 'v3', credentials=self.credentials)
            logger.info("Successfully authenticated with Google Drive")
            
        except Exception as e:
            logger.error(f"Error authenticating with Google Drive: {e}")
            raise
    
    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> str:
        """Create a folder in Google Drive"""
        try:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            elif Config.GOOGLE_DRIVE_FOLDER_ID:
                folder_metadata['parents'] = [Config.GOOGLE_DRIVE_FOLDER_ID]
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            logger.info(f"Created folder: {folder_name} (ID: {folder_id})")
            return folder_id
            
        except Exception as e:
            logger.error(f"Error creating folder {folder_name}: {e}")
            raise
    
    def upload_file(self, file_path: str, folder_id: Optional[str] = None, 
                   filename: Optional[str] = None) -> Dict:
        """Upload a file to Google Drive"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Use provided filename or extract from path
            if not filename:
                filename = os.path.basename(file_path)
            
            # Determine MIME type based on file extension
            mime_type = self._get_mime_type(file_path)
            
            file_metadata = {
                'name': filename
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            elif Config.GOOGLE_DRIVE_FOLDER_ID:
                file_metadata['parents'] = [Config.GOOGLE_DRIVE_FOLDER_ID]
            
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink'
            ).execute()
            
            file_info = {
                'id': file.get('id'),
                'name': file.get('name'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': file.get('webContentLink')
            }
            
            logger.info(f"Uploaded file: {filename} (ID: {file_info['id']})")
            return file_info
            
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            raise
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        mime_types = {
            '.pdf': 'application/pdf',
            '.epub': 'application/epub+zip',
            '.mobi': 'application/x-mobipocket-ebook',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.json': 'application/json'
        }
        
        return mime_types.get(ext, 'application/octet-stream')
    
    def upload_book_files(self, book_title: str, book_files: Dict, 
                         cover_path: Optional[str] = None) -> Dict:
        """Upload all book files to Google Drive"""
        try:
            # Create a folder for the book
            folder_name = f"Book - {book_title}"
            folder_id = self.create_folder(folder_name)
            
            uploaded_files = {
                'folder_id': folder_id,
                'folder_name': folder_name,
                'files': {}
            }
            
            # Upload book files
            for format_name, file_path in book_files.items():
                if os.path.exists(file_path):
                    file_info = self.upload_file(file_path, folder_id)
                    uploaded_files['files'][format_name] = file_info
                else:
                    logger.warning(f"Book file not found: {file_path}")
            
            # Upload cover if available
            if cover_path and os.path.exists(cover_path):
                cover_info = self.upload_file(cover_path, folder_id, "cover.png")
                uploaded_files['files']['cover'] = cover_info
            
            # Make folder publicly accessible (optional)
            try:
                self.service.permissions().create(
                    fileId=folder_id,
                    body={'type': 'anyone', 'role': 'reader'},
                    fields='id'
                ).execute()
                logger.info(f"Made folder publicly accessible: {folder_name}")
            except Exception as e:
                logger.warning(f"Could not make folder public: {e}")
            
            return uploaded_files
            
        except Exception as e:
            logger.error(f"Error uploading book files: {e}")
            raise
    
    def get_folder_link(self, folder_id: str) -> str:
        """Get the web view link for a folder"""
        try:
            folder = self.service.files().get(
                fileId=folder_id,
                fields='webViewLink'
            ).execute()
            
            return folder.get('webViewLink', '')
            
        except Exception as e:
            logger.error(f"Error getting folder link: {e}")
            return ""
    
    def list_files_in_folder(self, folder_id: str) -> List[Dict]:
        """List all files in a folder"""
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id,name,mimeType,webViewLink,createdTime)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Found {len(files)} files in folder")
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in folder: {e}")
            return []
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"Deleted file: {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {e}")
            return False
    
    def delete_folder(self, folder_id: str) -> bool:
        """Delete a folder and all its contents from Google Drive"""
        try:
            # First, list all files in the folder
            files = self.list_files_in_folder(folder_id)
            
            # Delete all files
            for file in files:
                self.delete_file(file['id'])
            
            # Delete the folder
            self.service.files().delete(fileId=folder_id).execute()
            logger.info(f"Deleted folder: {folder_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting folder {folder_id}: {e}")
            return False 
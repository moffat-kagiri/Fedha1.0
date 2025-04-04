from core.gdrive.auth import authenticate_google_drive
from core.gdrive.sync import upload_file_to_drive, download_file_from_drive
from core.storage.storage import DataManager

class GoogleDriveService:
    def __init__(self, credentials_path, get_storage_path):
        self.credentials_path = credentials_path
        self.data_manager = DataManager(get_storage_path)
        self.drive_service = authenticate_google_drive(credentials_path)

    def sync_to_drive(self, filename, folder_id):
        """Upload a file to Google Drive."""
        file_path = self.data_manager.get_storage_path(filename)
        upload_file_to_drive(self.drive_service, file_path, folder_id)

    def sync_from_drive(self, file_id, filename):
        """Download a file from Google Drive."""
        file_path = self.data_manager.get_storage_path(filename)
        download_file_from_drive(self.drive_service, file_id, file_path)
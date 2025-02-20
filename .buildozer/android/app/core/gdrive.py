import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.auth import AuthenticationError
from googleapiclient.errors import HttpError

def authenticate_google_drive():
    try:
        gauth = GoogleAuth()
        # Try loading existing credentials
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        # Save credentials for future runs
        gauth.SaveCredentialsFile("mycreds.txt")
        return GoogleDrive(gauth)
    except AuthenticationError as e:
        print(f"Authentication failed: {str(e)}")
        # Implement retry logic or fallback
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def upload_file_to_drive(drive, file_path, folder_id=None):
    file_name = os.path.basename(file_path)
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]} if folder_id else {})
    gfile.SetContentFile(file_path)
    gfile['title'] = file_name
    gfile.Upload()
    gfile.Upload(param={'callback': progress_callback})

def download_file_from_drive(drive, file_id, dest_path):
    gfile = drive.CreateFile({'id': file_id})
    gfile.GetContentFile(dest_path)
    print(f"Downloaded file to {dest_path}.")

from android.storage import get_app_path

class DriveClient:
    def __init__(self):
        self.credentials_path = get_app_path("gdrive_creds.json")
        
    def sync_files(self):
        """Modified version of original gdrive.py with Android paths"""
        local_loans = get_app_path("loans.csv")
        self.upload_file(local_loans)
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def authenticate_google_drive(credentials_path):
    """
    Authenticate with Google Drive using a service account.

    Args:
        credentials_path (str): Path to the service account credentials JSON file.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Google Drive service object.
    """
    try:
        # Load credentials from the service account file
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        # Build the Google Drive service
        drive_service = build("drive", "v3", credentials=credentials)
        return drive_service

    except Exception as e:
        raise Exception(f"Failed to authenticate with Google Drive: {str(e)}")
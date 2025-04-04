from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

def upload_file_to_drive(drive_service, file_path, folder_id=None):
    """
    Upload a file to Google Drive.

    Args:
        drive_service (googleapiclient.discovery.Resource): Authenticated Google Drive service object.
        file_path (str): Path to the file to upload.
        folder_id (str, optional): ID of the folder to upload the file to. Defaults to None.

    Returns:
        str: ID of the uploaded file.
    """
    try:
        # Extract the file name from the file path
        file_name = file_path.split("/")[-1]

        # Define file metadata
        file_metadata = {
            "name": file_name,
        }

        # If a folder ID is provided, set the parent folder
        if folder_id:
            file_metadata["parents"] = [folder_id]

        # Create a media object for the file
        media = MediaFileUpload(file_path, resumable=True)

        # Upload the file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        # Return the file ID
        return file.get("id")

    except HttpError as e:
        raise Exception(f"Google Drive API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to upload file to Google Drive: {str(e)}")

def download_file_from_drive(drive_service, file_id, dest_path):
    """
    Download a file from Google Drive.

    Args:
        drive_service (googleapiclient.discovery.Resource): Authenticated Google Drive service object.
        file_id (str): ID of the file to download.
        dest_path (str): Path to save the downloaded file.

    Returns:
        None
    """
    try:
        request = drive_service.files().get_media(fileId=file_id)
        with open(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")

    except HttpError as e:
        raise Exception(f"Google Drive API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to download file from Google Drive: {str(e)}")
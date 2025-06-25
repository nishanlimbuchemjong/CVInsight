# drive_upload.py

# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# import os

# # Define the folder ID of your shared Google Drive folder
# FOLDER_ID = '15O2lnrWaej3w67JwyKN2JNYnrirRoSd7'  # <-- replace with actual ID

# # Load credentials
# SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SERVICE_ACCOUNT_FILE = 'credentials.json'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# # Build the Drive service
# drive_service = build('drive', 'v3', credentials=credentials)

# def upload_to_drive(file_path, filename):
#     file_metadata = {
#         'name': filename,
#         'parents': [FOLDER_ID]
#     }

#     media = MediaFileUpload(file_path, resumable=True)

#     file = drive_service.files().create(
#         body=file_metadata,
#         media_body=media,
#         fields='id'
#     ).execute()

#     return file.get('id')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = '15O2lnrWaej3w67JwyKN2JNYnrirRoSd7'  # e.g. '1abc2DEFghiJ3456KLM'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_to_drive(file_path, filename):
    file_metadata = {'name': filename, 'parents': [FOLDER_ID]}
    media = MediaFileUpload(file_path, resumable=True)
    uploaded = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id').execute()
    file_id = uploaded.get('id')
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

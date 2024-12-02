from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Path to your service account JSON key
SERVICE_ACCOUNT_FILE = 'secrets/psychic-linker-442914-b9-fb17182d5de1.json'

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/drive']
)

# Build the Google Drive service
service = build('drive', 'v3', credentials=credentials)

# Function to upload a file and get its shareable link
def upload_file(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # Make the file shareable
    file_id = file.get('id')
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    link = f"https://drive.google.com/file/d/{file_id}/view"
    return link

# Upload files in a folder and get links
folder_id = '1g5rvY9-eeowyWOq8LAMywdtRhw6uaNXz'
pdf_folder = '/Users/julius/Downloads/batch'
pdf_links = {}

for file_name in os.listdir(pdf_folder):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, file_name)
        link = upload_file(file_path, folder_id)
        pdf_links[file_name] = link

# Print the links
for name, link in pdf_links.items():
    print(f"{name}: {link}")

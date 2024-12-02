import os
import pandas as pd
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive Setup
SERVICE_ACCOUNT_FILE = 'secrets/psychic-linker-442914-b9-fb17182d5de1.json'
FOLDER_ID = '1g5rvY9-eeowyWOq8LAMywdtRhw6uaNXz'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)

# Function to upload a file to Google Drive
def upload_file_to_drive(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    # Generate shareable link
    file_id = uploaded_file.get('id')
    drive_service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()
    return f"https://drive.google.com/file/d/{file_id}/view"

# Function to normalize a title
def normalize_title(title):
    return re.sub(r'[^\w\s]', '', title).lower()

# Function to extract title from PDF file name
def extract_title_from_filename(file_name):
    parts = file_name.split(" - ")
    if len(parts) >= 3:
        return parts[2].strip()
    return file_name

# Load CSV
csv_path = 'results/Articles/journals_sample.csv'
articles = pd.read_csv(csv_path)

# Normalize CSV titles
articles['Normalized Title'] = articles['Title'].apply(normalize_title)

# Path to your folder containing PDFs
pdf_folder = '/Users/julius/Downloads/batch'

# Track results
matches = []
unmatched_pdfs = []
drive_links = []

# Process PDFs
for file_name in os.listdir(pdf_folder):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, file_name)
        extracted_title = extract_title_from_filename(os.path.splitext(file_name)[0])
        normalized_extracted_title = normalize_title(extracted_title)
        
        # Upload to Drive
        drive_link = upload_file_to_drive(file_path, FOLDER_ID)
        drive_links.append((file_name, drive_link))
        
        # Match with CSV
        match = articles[articles['Normalized Title'].str.startswith(normalized_extracted_title)]
        if not match.empty:
            matched_csv_index = match.index[0]
            articles.at[matched_csv_index, 'PDF Link'] = drive_link
            matches.append((articles.at[matched_csv_index, 'Title'], extracted_title))
        else:
            unmatched_pdfs.append((file_name, extracted_title, normalized_extracted_title))

# Save updated CSV
updated_csv_path = 'results/Articles/journals_sample_withlinks.csv'
articles.to_csv(updated_csv_path, index=False)

# Print results
print(f"Updated CSV saved to {updated_csv_path}")

print(f"\nUnmatched PDFs: {len(unmatched_pdfs)}")
for file_name, extracted_title, normalized_title in unmatched_pdfs:
    print(f"File: {file_name}")
    print(f"Extracted Title: {extracted_title}")
    print(f"Normalized Title: {normalized_title}")

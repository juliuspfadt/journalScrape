import os
import pandas as pd
import re

# Function to normalize a title by removing special characters and converting to lowercase
def normalize_title(title):
    """
    Removes special characters and converts the title to lowercase.
    
    Parameters:
        title (str): The title to normalize.
        
    Returns:
        str: The normalized title.
    """
    return re.sub(r'[^\w\s]', '', title).lower()

# Helper function to extract the title from the PDF file name
def extract_title_from_filename(file_name):
    """
    Extracts the title from a PDF file name by splitting on ' - '.
    
    Parameters:
        file_name (str): The name of the PDF file (without extension).
        
    Returns:
        str: The extracted title.
    """
    parts = file_name.split(" - ")
    if len(parts) >= 3:  # Ensure the file name has the expected format
        return parts[2].strip()  # The title is after the second ' - '
    return file_name  # Fallback to the full name if splitting fails

# Load the CSV
csv_path = 'results/Articles/journals_sample.csv'
articles = pd.read_csv(csv_path)

# Normalize the titles in the CSV
articles['Normalized Title'] = articles['Title'].apply(normalize_title)

# Path to your folder containing PDFs
pdf_folder = '/Users/julius/Downloads/batch'

# Track matches and unmatched PDFs
matches = []
unmatched_pdfs = []

# Process each PDF and attempt to match its normalized title to the CSV
for file_name in os.listdir(pdf_folder):
    if file_name.endswith('.pdf'):
        # Extract file name without extension and title
        file_name_no_ext = os.path.splitext(file_name)[0]
        extracted_title = extract_title_from_filename(file_name_no_ext)
        normalized_extracted_title = normalize_title(extracted_title)
        
        # Match based on "starts-with" logic
        match = articles[articles['Normalized Title'].str.startswith(normalized_extracted_title)]
        
        if not match.empty:
            # Matched successfully
            matched_csv_title = match.iloc[0]['Title']
            matches.append((matched_csv_title, extracted_title))
        else:
            # Log unmatched PDFs with normalized titles
            unmatched_csv_titles = articles['Normalized Title'].tolist()
            unmatched_pdfs.append((file_name, extracted_title, normalized_extracted_title, unmatched_csv_titles))

# Save the updated CSV
updated_csv_path = 'results/Articles/journals_sample_updated.csv'
articles.to_csv(updated_csv_path, index=False)

# Print the results
print(f"Updated CSV saved to {updated_csv_path}")

print(f"\nMatched {len(matches)} PDFs with CSV titles:")
for csv_title, extracted_title in matches:
    print(f"{csv_title} -> {extracted_title}")

print(f"\nUnmatched PDFs: {len(unmatched_pdfs)}")
for file_name, extracted_title, normalized_extracted_title, unmatched_csv_titles in unmatched_pdfs:
    print(f"File Name: {file_name}")
    print(f"Extracted Title: {extracted_title}")
    print(f"Normalized PDF Title: {normalized_extracted_title}")
    print("Normalized CSV Titles:")
    for csv_title in unmatched_csv_titles:
        print(f"  - {csv_title}")

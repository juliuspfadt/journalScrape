import os
import pandas as pd
from PyPDF2 import PdfReader

# Function to extract metadata from a PDF file
def extract_pdf_metadata(pdf_path):
    """
    Extracts metadata from a PDF file.
    
    Parameters:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        dict: The metadata dictionary from the PDF file.
    """
    try:
        reader = PdfReader(pdf_path)
        return reader.metadata
    except Exception as e:
        print(f"Error reading metadata from {pdf_path}: {e}")
        return None

# Load the CSV
csv_path = 'results/Articles/journals_sample.csv'
articles = pd.read_csv(csv_path)

# Path to your folder containing PDFs
pdf_folder = '/Users/julius/Downloads/batch'

# Track matches and unmatched results
matches = []
unmatched_pdfs = []
pdf_no_metadata = []

# Process each PDF and attempt to match its metadata title to the CSV
for file_name in os.listdir(pdf_folder):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_folder, file_name)
        pdf_metadata = extract_pdf_metadata(file_path)
        pdf_title = pdf_metadata.title.strip() if pdf_metadata and pdf_metadata.title else None

        if pdf_title:
            # Attempt to find a matching title in the CSV
            match = articles[articles['Title'].str.strip().str.lower() == pdf_title.lower()]
            if not match.empty:
                # Add matched CSV and PDF titles to the matches list
                matched_csv_title = match.iloc[0]['Title']
                matches.append((matched_csv_title, pdf_title))
            else:
                # Log unmatched PDFs with CSV title and full metadata
                unmatched_pdfs.append((file_name, pdf_metadata))
        else:
            pdf_no_metadata.append(file_name)

# Save the updated CSV
updated_csv_path = 'results/Articles/journals_sample_updated.csv'
articles.to_csv(updated_csv_path, index=False)

# Print the results
print(f"Updated CSV saved to {updated_csv_path}")

print(f"\nMatched {len(matches)} PDFs with CSV titles:")
for csv_title, pdf_metadata_title in matches:
    print(f"{csv_title} -> {pdf_metadata_title}")

print(f"\nUnmatched PDFs with full metadata: {len(unmatched_pdfs)}")
for csv_title, metadata in unmatched_pdfs:
    print(f"{csv_title}")
    print(f"Metadata: {metadata}")

print(f"\nPDFs with no extractable metadata: {len(pdf_no_metadata)}")
for csv_title in pdf_no_metadata:
    print(csv_title)

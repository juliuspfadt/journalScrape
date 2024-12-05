import requests
import os
import re
import pandas as pd


def sanitize_doi(doi):
    """
    Sanitize a DOI for use as a filename by replacing invalid characters with unique replacements.
    """
    replacements = {
        "/": "__",          # Replace forward slashes
        ":": "_COLON_",     # Replace colons
        "?": "_QUESTION_",  # Replace question marks
        "<": "_LT_",        # Replace less-than
        ">": "_GT_",        # Replace greater-than
        "|": "_PIPE_",      # Replace pipe
        '"': "_QUOTE_",     # Replace quotes
        "*": "_STAR_",      # Replace asterisks
        "\\": "_BACKSLASH_" # Replace backslashes
    }
    for char, replacement in replacements.items():
        doi = doi.replace(char, replacement)
    return doi


def download_pdf(pdf_url, output_dir, doi):
    """
    Download the PDF using the provided URL and save it locally with a sanitized DOI as the filename.
    """
    try:
        # Use only the actual DOI part (remove 'https://doi.org/')
        if doi.startswith("https://doi.org/"):
            doi = doi.split("https://doi.org/")[1]
        
        # Sanitize DOI for use in the file name
        sanitized_doi = sanitize_doi(doi)
        pdf_filename = os.path.join(output_dir, f"{sanitized_doi}.pdf")
        
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()
        
        # Save the PDF
        with open(pdf_filename, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        
        print(f"PDF saved: {pdf_filename}")
        return True
    except requests.RequestException as e:
        print(f"Error downloading PDF from {pdf_url}: {e}")
        return False


def process_pbr_articles(file_path):
    """
    Process all articles from the specified dataset and download their PDFs.
    """
    # Create a dedicated download directory
    output_dir = os.path.join(os.getcwd(), "pbr_downloads")
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Check if there is a previous progress file
    last_successful_index_file = "pbr_last_successful_index.txt"
    start_index = 0
    if os.path.exists(last_successful_index_file):
        with open(last_successful_index_file, "r") as f:
            saved_index = f.read().strip()
            if saved_index.isdigit():
                start_index = int(saved_index) + 1  # Start from the next article
                print(f"Resuming from index {start_index}")
            else:
                print("Progress file found, but it's corrupted. Restarting from the beginning.")
    
    # Process each article starting from the last successful index
    for index, row in df.iloc[start_index:].iterrows():
        doi = row['DOI']
        pdf_url = row['PDF Link']
        if pd.notnull(doi) and pd.notnull(pdf_url):
            # Use only the DOI for naming
            print(f"Processing DOI: {doi}, PDF URL: {pdf_url}")
            
            # Attempt to download the PDF
            success = download_pdf(pdf_url, output_dir, doi)
            if not success:
                # Record the last successful index and exit on failure
                print(f"Download failed. Last successful index: {index - 1}")
                with open(last_successful_index_file, "w") as f:
                    f.write(str(index - 1))
                break
            else:
                # Save the last successful index after each successful download
                with open(last_successful_index_file, "w") as f:
                    f.write(str(index))

    print("Processing complete.")


# Path to the input CSV file
file_path = "results/Journals/Springer/pbr_articles_cleaned.csv"  # Replace with your actual file path
process_pbr_articles(file_path)

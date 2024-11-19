import requests
import time
import pandas as pd

def fetch_citation_count(doi):
    """
    Fetches the citation count for a given DOI using CrossRef's REST API.
    """
    base_url = f"https://api.crossref.org/works/{doi}"
    
    try:
        response = requests.get(base_url, headers={"User-Agent": "mailto:ribose-parks.0f@icloud.com"})
        response.raise_for_status()
        
        data = response.json()
        # Extract the citation count if available
        citation_count = data['message'].get('is-referenced-by-count', None)
        return citation_count
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for DOI {doi}: {e}")
        return None

def process_dois_and_update_csv(file_path):
    """
    Reads DOIs from a CSV file, fetches citation counts, and appends the data to the CSV.
    """
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Check for a DOI column
    if 'DOI' not in df.columns:
        print("The CSV file does not contain a 'DOI' column.")
        return

    # Create a new column for citation counts
    df['Citation_Count'] = None

    # Process each DOI
    for index, row in df.iterrows():
        doi_url = row['DOI']
        if pd.notnull(doi_url):
            # Extract DOI from the URL
            if doi_url.startswith("https://doi.org/"):
                doi = doi_url.split("https://doi.org/")[1]
            else:
                doi = doi_url  # Handle cases where the DOI is not a full URL
            
            print(f"Fetching citation count for DOI: {doi}")
            count = fetch_citation_count(doi)
            df.at[index, 'Citation_Count'] = count
            # Be respectful of rate limits
            time.sleep(1)

    # Save the updated CSV
    output_file = file_path.replace('.csv', '_with_citations.csv')
    df.to_csv(output_file, index=False)
    print(f"Updated file saved as: {output_file}")

# Path to the uploaded CSV file
file_path = 'results/combined_journals.csv'

# Process the file
process_dois_and_update_csv(file_path)

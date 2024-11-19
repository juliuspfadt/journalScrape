import pandas as pd

# Load the full combined data
combined_df = pd.read_csv("results/combined_journals.csv")

# Get the current year
current_year = pd.Timestamp.now().year

# Filter articles from the last four years
filtered_df = combined_df[combined_df['Publication Year'] >= current_year - 4]

# Select up to 6 articles per journal
sampled_df = filtered_df.groupby('Journal').apply(lambda x: x.sample(n=min(len(x), 2), random_state=2)).reset_index(drop=True)

def format_authors(authors_str):
    """
    Properly format author names for RIS, with each author on a separate line.
    """
    if not pd.notna(authors_str) or not authors_str.strip():
        return []

    formatted_authors = []
    for author in authors_str.split(","):  # Adjust delimiter if necessary
        parts = [p.strip() for p in author.split() if p.strip()]  # Split and clean
        if len(parts) > 1:
            last_name = parts[-1]
            first_names = " ".join(parts[:-1])
            formatted_authors.append(f"{last_name}, {first_names}")
        elif len(parts) == 1:
            formatted_authors.append(parts[0])  # Single-word name, use as-is

    return formatted_authors

def clean_doi(doi_str):
    if not pd.notna(doi_str) or not doi_str.strip():
        return "", ""
    doi_str = doi_str.strip()
    if doi_str.startswith("https://doi.org/"):
        doi_number = doi_str[len("https://doi.org/"):]  # Extract DOI after the prefix
    else:
        doi_number = doi_str  # Assume the string is already just the DOI number
    return doi_number, doi_str

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def convert_to_ris(df, output_path):
    ris_entries = []
    for _, row in df.iterrows():
        authors = format_authors(row['Authors'])
        publication_year = safe_int(row['Publication Year'])
        volume = safe_int(row.get('Volume'))
        issue = safe_int(row.get('Issue'))
        doi_number, doi_link = clean_doi(row.get('DOI'))
        
        entry = [
            "TY  - JOUR",
            f"TI  - {row['Title']}",
        ]
        
        for author in authors:
            entry.append(f"AU  - {author}")

        entry.extend([
            f"JO  - {row['Journal']}" if pd.notna(row['Journal']) else "",
            f"DO  - {doi_number}" if doi_number else "",
            f"UR  - {doi_link}" if doi_link else "",
            f"PY  - {publication_year}" if publication_year else "",
            f"VL  - {volume}" if volume else "",
            f"IS  - {issue}" if issue else "",
            f"SP  - {row['Pages'].split('-')[0]}" if pd.notna(row['Pages']) else "",
            f"EP  - {row['Pages'].split('-')[1]}" if pd.notna(row['Pages']) and '-' in row['Pages'] else "",
            "ER  -"
        ])
        
        ris_entries.append("\n".join(filter(None, entry)))

    ris_content = "\n\n".join(ris_entries)
    
    with open(output_path, "w", encoding="utf-8") as ris_file:
        ris_file.write(ris_content)

# Create RIS file for subsample
convert_to_ris(sampled_df, "results/RIS/allJournals_subsample.ris")

import pandas as pd

# Load your cleaned DataFrame (replace with your actual file path)
dfXge = pd.read_csv("results/Journals/APA/xge_articles_cleaned.csv")
dfPss = pd.read_csv("results/Journals/Sage/pss_articles_cleaned.csv")
dfPbr = pd.read_csv("results/Journals/Springer/pbr_articles_cleaned.csv")
dfDs = pd.read_csv("results/Journals/Wiley/ds_articles_cleaned.csv")

# Print column names of each DataFrame
print("Columns in dfXge:", dfXge.columns.tolist())
print("Columns in dfPss:", dfPss.columns.tolist())
print("Columns in dfPbr:", dfPbr.columns.tolist())
print("Columns in dfDs:", dfDs.columns.tolist())

# Find common columns
common_columns = list(set(dfXge.columns) & set(dfPss.columns) & set(dfPbr.columns) & set(dfDs.columns))
print("Common columns:", common_columns)

# Combine data sets using only the common columns
combined_df = pd.concat([dfXge[common_columns], dfPss[common_columns], dfPbr[common_columns], dfDs[common_columns]], ignore_index=True)
print("Combined DataFrame shape:", combined_df.shape)

# Function to convert DataFrame to RIS format with additional details
def convert_to_ris(df, output_path):
    ris_entries = []
    for _, row in df.iterrows():
        entry = [
            "TY  - JOUR",  # Type of reference
            f"TI  - {row['Title']}",  # Title
            f"AU  - {row['Authors']}",  # Authors
            f"JO  - {row['Journal']}" if pd.notna(row['Journal']) else "",  # Journal Name
            f"DO  - {row['DOI']}" if pd.notna(row['DOI']) else "",  # DOI
            f"PY  - {row['Publication Year']}",  # Publication Year
            f"VL  - {row['Volume']}" if pd.notna(row['Volume']) else "",  # Volume
            f"IS  - {row['Issue']}" if pd.notna(row['Issue']) else "",  # Issue
            f"SP  - {row['Pages'].split('-')[0]}" if pd.notna(row['Pages']) else "",  # Start Page
            f"EP  - {row['Pages'].split('-')[1]}" if pd.notna(row['Pages']) and '-' in row['Pages'] else "",  # End Page
            "ER  -"  # End of entry
        ]
        ris_entries.append("\n".join(filter(None, entry)))  # Filter out empty fields

    # Join all entries with double line breaks
    ris_content = "\n\n".join(ris_entries)
    
    # Write to RIS file
    try:
        with open(output_path, "w", encoding="utf-8") as ris_file:
            ris_file.write(ris_content)
        print(f"RIS file successfully written to {output_path}")
    except Exception as e:
        print(f"Failed to write RIS file: {e}")
        return
    
    # Confirmation messages
    print(f"Total articles processed: {len(df)}")
    print(f"Output RIS file includes {len(ris_entries)} entries.")
    print(f"Journals included: {df['Journal'].nunique()}")
    print("Sample journals:", df['Journal'].unique()[:5])

# Call the function with the desired output path
convert_to_ris(combined_df, "results/RIS/output_file.ris")

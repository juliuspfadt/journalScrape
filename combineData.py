import pandas as pd
import json

# Load your cleaned DataFrame (replace with your actual file paths)
dfXge = pd.read_csv("results/Journals/APA/xge_articles_cleaned.csv")
dfPss = pd.read_csv("results/Journals/Sage/pss_articles_cleaned.csv")
dfPbr = pd.read_csv("results/Journals/Springer/pbr_articles_cleaned.csv")
dfDs = pd.read_csv("results/Journals/Wiley/ds_articles_cleaned.csv")
dfBrt = pd.read_csv("results/Journals/Elsevier/brt_articles_cleaned.csv")
dfJesp = pd.read_csv("results/Journals/Elsevier/jesp_articles_cleaned.csv")

# Find common columns
common_columns = list(set(dfXge.columns) & set(dfPss.columns) & set(dfPbr.columns) & set(dfDs.columns) 
                      & set(dfBrt.columns) & set(dfJesp.columns))

# Combine data sets using only the common columns
combined_df = pd.concat([dfXge[common_columns], dfPss[common_columns], dfPbr[common_columns], 
                         dfDs[common_columns], dfBrt[common_columns], dfJesp[common_columns]], ignore_index=True)

# Specify the desired order of columns
desired_columns = ['Journal', 'Volume', 'Issue', 'Publication Year', 'Title', 'Authors', 'Author Affiliations', 'Pages', 'DOI']

# Keep only the desired columns in the specified order
# Filter out unwanted columns like 'type' or 'pdf link' if they exist
combined_df = combined_df[[col for col in desired_columns if col in combined_df.columns]]

# Convert 'Volume', 'Issue', and 'Publication Year' to integers
for col in ['Volume', 'Issue', 'Publication Year']:
    if col in combined_df.columns:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').fillna(0).astype(int)

# Write combined_df to CSV
combined_df.to_csv("results/combined_journals.csv", index=False)

# Write combined_df to JSON using json.dump
with open("results/combined_journals.json", "w", encoding="utf-8") as json_file:
    json.dump(combined_df.to_dict(orient="records"), json_file, ensure_ascii=False, indent=4)

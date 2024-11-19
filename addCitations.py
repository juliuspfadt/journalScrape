import pandas as pd
import json

# Load the main dataset and the citations dataset
combined_journals_df = pd.read_csv("results/combined_journals.csv")
citations_df = pd.read_csv("results/citations.csv")

# Merge the datasets on the 'DOI' column, adding citations to the main dataset
merged_df = pd.merge(combined_journals_df, 
                     citations_df[['DOI', 'Citation_Count']], 
                     on='DOI', 
                     how='left')

# Rename 'Citation_Count' to 'Citations'
merged_df.rename(columns={'Citation_Count': 'Citations'}, inplace=True)

# Save the merged dataset to a new CSV file
merged_df.to_csv("results/combined_journals_with_citations.csv", index=False)

# Save the merged dataset to a new JSON file
with open("results/combined_journals_with_citations.json", "w", encoding="utf-8") as json_file:
    json.dump(merged_df.to_dict(orient="records"), json_file, ensure_ascii=False, indent=4)


print("Merged dataset saved with citations added.")

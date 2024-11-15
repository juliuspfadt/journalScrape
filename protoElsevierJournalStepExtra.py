# there were some missings from the previous step, this handles the missings in the DOIs
# should be run without access to the articles

import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome options to minimize loading resources
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")  # Block images
options.add_argument("--disable-javascript")  # Disable JavaScript if not essential
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
options.add_argument("--disable-background-networking")  # Minimize background tasks
options.add_argument("--disable-sync")  # Disable Chrome Sync

# Paths to input and output files
brt_articles_file = "results/Journals/Elsevier/brt_articles.csv"  # Replace with your path
brt_toc_articles_file = "results/Journals/Elsevier/brt_toc_articles.csv"  # Replace with your path
output_file = "results/Journals/Elsevier/updated_brt_articles.csv"  # Replace with your desired output path

# Load the input files
brt_articles_df = pd.read_csv(brt_articles_file)
brt_toc_articles_df = pd.read_csv(brt_toc_articles_file)

# Step 1: Find incomplete DOIs
incomplete_doi_df = brt_articles_df[brt_articles_df['DOI'] == 'https://doi.org/N/A']

# Step 2: Match titles with brt_toc_articles to get URLs
matched_df = pd.merge(incomplete_doi_df, brt_toc_articles_df[['Title', 'Article URL']], on='Title', how='inner')

# Step 3: Retrieve missing data for matched articles
driver = webdriver.Chrome(options=options)
retrieved_data = []

for index, row in matched_df.iterrows():
    try:
        driver.get(row['Article URL'])

        # Retrieve metadata from the article page
        metadata = driver.execute_script("""
            return {
                doi: document.querySelector('meta[name="citation_doi"]')?.content || "N/A",
                volume: document.querySelector('meta[name="citation_volume"]')?.content || "N/A",
                issue: document.querySelector('meta[name="citation_issue"]')?.content || "N/A",
                publicationYear: document.querySelector('meta[name="citation_publication_date"]')?.content?.split('/')[0] || "N/A",
                journal: document.querySelector('meta[name="citation_journal_title"]')?.content || "N/A",
                firstPage: document.querySelector('meta[name="citation_firstpage"]')?.content || "N/A",
                lastPage: document.querySelector('meta[name="citation_lastpage"]')?.content || "N/A",
                citations: document.querySelector('#preview-section-cited-by-item .anchor-text')?.innerText || "N/A"
            };
        """)

        # Combine first and last pages into a single field
        pages = (
            f"{metadata['firstPage']}-{metadata['lastPage']}"
            if metadata['firstPage'] != "N/A" and metadata['lastPage'] != "N/A"
            else "N/A"
        )

        # Collect retrieved data
        retrieved_data.append({
            "Title": row['Title'],
            "DOI": f"https://doi.org/{metadata['doi']}" if metadata['doi'] != "N/A" else "N/A",
            "Journal": metadata['journal'],
            "Volume": metadata['volume'],
            "Issue": metadata['issue'],
            "Publication Year": metadata['publicationYear'],
            "Citations": metadata['citations'].replace("Cited by (", "").replace(")", "") if metadata['citations'] != "N/A" else "N/A",
            "Pages": pages
        })

        print(f"Successfully retrieved data for: {row['Title']}")

        # Add a random delay to avoid detection
        time.sleep(random.uniform(0.5, 1.5))

    except Exception as e:
        print(f"Failed to retrieve data for: {row['Title']}. Error: {e}")

# Close the driver after processing
driver.quit()

# Step 4: Update brt_articles_df with retrieved data
retrieved_df = pd.DataFrame(retrieved_data)
updated_brt_articles_df = brt_articles_df.merge(retrieved_df, on='Title', how='left', suffixes=('', '_retrieved'))

# Replace original columns with retrieved data where available
columns_to_update = ['DOI', 'Journal', 'Volume', 'Issue', 'Publication Year', 'Citations', 'Pages']
for column in columns_to_update:
    updated_brt_articles_df[column] = updated_brt_articles_df[f"{column}_retrieved"].combine_first(updated_brt_articles_df[column])
    updated_brt_articles_df.drop(columns=[f"{column}_retrieved"], inplace=True)

# Save the updated DataFrame to a new file
updated_brt_articles_df.to_csv(output_file, index=False)
print(f"Updated brt_articles saved to: {output_file}")

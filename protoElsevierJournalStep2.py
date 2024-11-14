import time
import random
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

# Chrome options to minimize loading resources
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")  # Block images
options.add_argument("--disable-javascript")  # Disable JavaScript if not essential
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
options.add_argument("window-size=1920,1080")
options.add_argument("--disable-background-networking")  # Minimize background tasks
options.add_argument("--disable-sync")  # Disable Chrome Sync

# Paths to input and output files
input_file = "results/Journals/Elsevier/brt_toc_articles.csv"
output_file = "results/Journals/Elsevier/brt_articles.csv"

# Load the CSV with article data
toc_df = pd.read_csv(input_file).head

# Check if an output file already exists and load it to resume progress
if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    processed_titles = set(existing_df['Title'].tolist())
    print(f"Resuming from previous run, {len(processed_titles)} articles already processed.")
else:
    existing_df = pd.DataFrame()
    processed_titles = set()
    print("Starting a fresh run.")

# Initialize the Chrome WebDriver (ensure ChromeDriver is in PATH)
driver = webdriver.Chrome(options=options)
detailed_articles = []  # Accumulate new articles in this list

# Process each article sequentially
for index, row in toc_df.iterrows():
    if row['Title'] in processed_titles:
        print(f"Skipping already processed article: {row['Title']}")
        continue  # Skip articles that have already been processed

    article_data = {
        "Journal": "N/A",
        "Volume": "N/A",
        "Issue": "N/A",
        "Publication Year": "N/A",
        "Title": row['Title'],
        "Authors": row['Authors'],
        "Author Affiliations": "Pending",
        "Pages": "N/A",
        "Type": row['Article Type'],
        "DOI": "N/A",
        "PDF Link": row.get('PDF Link', "N/A"),
        "Citations": "N/A"
    }

    try:
        driver.get(row['Article URL'])

        # Retrieve all necessary data at once with execute_script
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

        # Populate article_data with retrieved metadata
        article_data['DOI'] = f"https://doi.org/{metadata['doi']}"
        article_data['Volume'] = metadata['volume']
        article_data['Issue'] = metadata['issue']
        article_data['Publication Year'] = metadata['publicationYear']
        article_data['Journal'] = metadata['journal']
        article_data['Pages'] = f"{metadata['firstPage']}-{metadata['lastPage']}" if metadata['firstPage'] != "N/A" and metadata['lastPage'] != "N/A" else "N/A"
        article_data['Citations'] = metadata['citations'].replace("Cited by (", "").replace(")", "")

        # Check if essential fields (Journal and Publication Year) are missing
        if article_data['Journal'] == "N/A" or article_data['Publication Year'] == "N/A":
            print(f"Essential data missing for article '{article_data['Title']}'. Exiting to save progress.")
            break  # Exit the loop if essential data is missing

        print(f"Processed {index + 1}/{len(toc_df)}: {article_data['Title']}")
    except Exception as e:
        print(f"Error processing article '{row['Title']}': {e}")
        break  # Exit the loop if any other error occurs

    # Append data to list and save incrementally
    detailed_articles.append(article_data)
    updated_df = pd.concat([existing_df, pd.DataFrame(detailed_articles)], ignore_index=True)
    updated_df.to_csv(output_file, index=False, encoding="utf-8")

    # Add article title to processed_titles to avoid re-processing in future runs
    processed_titles.add(row['Title'])

    # Add a random, shorter delay to avoid detection
    time.sleep(random.uniform(0.5, 1.5))

# Close the driver once all articles are processed
driver.quit()

# Final save to JSON format, ensuring all entries are marked as "N/A" where applicable
final_df = pd.read_csv(output_file).fillna("N/A")  # Reload to ensure all data is included

with open("results/Journals/Elsevier/brt_articles.json", "w", encoding="utf-8") as f:
    json.dump(detailed_articles, f, ensure_ascii=False, indent=4)

print("Detailed article data saved.")

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the driver with options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# Function to extract metadata from an article page
def extract_article_metadata(article_url):
    try:
        response = requests.get(article_url, timeout=5)
        response.raise_for_status()
        article_soup = BeautifulSoup(response.content, "html.parser")

        # Extract article metadata
        title = article_soup.find("meta", {"name": "dc.title"})["content"] if article_soup.find("meta", {"name": "dc.title"}) else "N/A"
        doi = article_soup.find("meta", {"name": "citation_doi"})["content"] if article_soup.find("meta", {"name": "citation_doi"}) else "N/A"
        doi = f"https://doi.org/{doi}" if doi != "N/A" else "N/A"

        publication_date = article_soup.find("meta", {"name": "citation_publication_date"})["content"] if article_soup.find("meta", {"name": "citation_publication_date"}) else "N/A"
        publication_year = publication_date.split("/")[0] if publication_date != "N/A" else "N/A"

        authors = [meta["content"] for meta in article_soup.find_all("meta", {"name": "citation_author"})]
        article_type = article_soup.find("meta", {"name": "citation_article_type"})["content"] if article_soup.find("meta", {"name": "citation_article_type"}) else "N/A"
        journal_title = article_soup.find("meta", {"name": "citation_journal_title"})["content"] if article_soup.find("meta", {"name": "citation_journal_title"}) else "N/A"
        volume = article_soup.find("meta", {"name": "citation_volume"})["content"] if article_soup.find("meta", {"name": "citation_volume"}) else "N/A"
        issue = article_soup.find("meta", {"name": "citation_issue"})["content"] if article_soup.find("meta", {"name": "citation_issue"}) else "N/A"

        # Extract page numbers
        start_page = article_soup.find("meta", {"name": "prism.startingPage"})["content"] if article_soup.find("meta", {"name": "prism.startingPage"}) else "N/A"
        end_page = article_soup.find("meta", {"name": "prism.endingPage"})["content"] if article_soup.find("meta", {"name": "prism.endingPage"}) else "N/A"
        pages = f"{start_page}-{end_page}" if start_page != "N/A" and end_page != "N/A" else "N/A"

        # Extract PDF link
        pdf_link = article_soup.find("meta", {"name": "citation_pdf_url"})["content"] if article_soup.find("meta", {"name": "citation_pdf_url"}) else "N/A"

        # Extract affiliations
        affiliations = []
        author_info_section = article_soup.find("div", {"id": "author-information-content"})
        if author_info_section:
            affiliation_items = author_info_section.find_all("p", class_="c-article-author-affiliation__address")
            affiliations = [affiliation.text.strip() for affiliation in affiliation_items]
        author_affiliations = "; ".join(affiliations) if affiliations else "N/A"

        # Structuring data as per the required order
        return {
            "Journal": journal_title,
            "Volume": volume,
            "Issue": issue,
            "Publication Year": publication_year,
            "Title": title,
            "Authors": ", ".join(authors),
            "Author Affiliations": author_affiliations,
            "Pages": pages,
            "Type": article_type,
            "DOI": doi,
            "PDF Link": pdf_link
        }
    except (requests.RequestException, AttributeError) as e:
        print(f"Error fetching article details from {article_url}: {e}")
        return None

# Function to extract article links from the current page and fetch metadata asynchronously
def process_articles_on_page(soup):
    articles = soup.find_all("li", {"data-test": "search-result-item"})
    if not articles:
        return []  # Stop if no articles are found on the page
    
    article_metadata_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(extract_article_metadata, "https://link.springer.com" + article.find("a", {"data-track-action": "view Article"})["href"])
            for article in articles if article.find("a", {"data-track-action": "view Article"})
        ]
        for future in as_completed(futures):
            article_metadata = future.result()
            if article_metadata:
                article_metadata_list.append(article_metadata)
    
    return article_metadata_list

# Initialize a list to store all article data across years
all_article_data = []

# Specify the year range for processing
start_year = 2004
end_year = 2024

# Loop through each year in the desired range
for year in range(start_year, end_year + 1):
    print(f"Processing articles for the year {year}...")
    base_url = "https://link.springer.com"
    driver.get(f"{base_url}/search?new-search=true&facet-journal-id=13423&query=*&content-type=article&date=custom&dateFrom={year}&dateTo={year}&sortBy=oldestFirst")
    
    while True:
        # Parse articles on the current page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        all_article_data.extend(process_articles_on_page(soup))
        print(f"Total articles processed so far: {len(all_article_data)}")

        # Check for "Next" page link and navigate directly
        next_button = soup.find("a", {"rel": "next"})
        if next_button:
            next_page_url = base_url + next_button["href"]
            driver.get(next_page_url)
            time.sleep(2)  # Allow time for the page to load
        else:
            print(f"No more pages for the year {year}.")
            break

# Close the driver
driver.quit()

# Save data to JSON and CSV
with open("results/Journals/Springer/pbr_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_article_data, f, ensure_ascii=False, indent=4)

df = pd.DataFrame(all_article_data)
df.to_csv("results/Journals/Springer/pbr_articles.csv", index=False, encoding="utf-8")

print("Data saved.")

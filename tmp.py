from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
]

# Initialize the Chrome webdriver with options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=" + random.choice(USER_AGENTS))
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

base_url = "https://journals.sagepub.com"
current_issue_url = f"{base_url}/toc/pssa/11/1"
journal_name = "Psychological Science"

articles = []

# Function to extract article details from the TOC page
def extract_article_data(article, volume, issue_number, journal_name):
    title = article.find("h5", class_="issue-item__heading").text.strip()
    authors = [author.text.strip() for author in article.find_all("span", id=lambda x: x and x.startswith("author"))]
    doi_suffix = article.find("a", href=True)["href"]
    doi_link = base_url + doi_suffix
    pages = article.find("span", string=lambda x: x and "pp." in x).text.strip() if article.find("span", string=lambda x: x and "pp." in x) else "N/A"
    publication_date = article.find("span", string=lambda x: x and "First published" in x)
    pub_year = publication_date.text.replace("First published ", "").split()[-1] if publication_date else "N/A"
    
    return {
        "Journal": journal_name,
        "Publication Year": pub_year,
        "Volume": volume,
        "Issue": issue_number,
        "Title": title,
        "Authors": authors,
        "DOI": doi_link,
        "Pages": pages,
    }

# Function to fetch additional data from individual article pages asynchronously
def fetch_article_details(article_data):
    response = requests.get(article_data["DOI"], headers={"User-Agent": random.choice(USER_AGENTS)})
    article_soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract citation count if available
    crossref_citation_span = article_soup.find("span", class_="cross-ref-count font-weight-semibold")
    crossref_citations = ''.join(filter(str.isdigit, crossref_citation_span.text.strip())) if crossref_citation_span else "N/A"
    
    article_data["Crossref Citations"] = crossref_citations
    return article_data

# Process each issue
issue_count = 1
while current_issue_url:
    driver.get(current_issue_url)
    time.sleep(1)  # Shorter delay; adjust if needed

    # Parse the TOC page
    toc_soup = BeautifulSoup(driver.page_source, "html.parser")
    issue_title = toc_soup.find("div", class_="spd__title").get_text(strip=True)
    volume_issue_info = issue_title.replace("Volume ", "").replace("Issue ", "").split(", ")
    volume = volume_issue_info[0].split()[0] if len(volume_issue_info) > 0 else "N/A"
    issue_number = volume_issue_info[0].split()[1] if len(volume_issue_info[0].split()) > 1 else "N/A"

    # Extract data for each article
    for article in toc_soup.find_all("div", class_="issue-item"):
        article_data = extract_article_data(article, volume, issue_number, journal_name)
        articles.append(article_data)

    print(f"Processed {len(articles)} articles in Issue {issue_number} of Volume {volume}")

    # Find the "Next issue" link
    next_issue_link = toc_soup.find("a", class_="content-navigation__btn--next")
    if next_issue_link:
        current_issue_url = base_url + next_issue_link.get("href")
        issue_count += 1
    else:
        print("No more issues.")
        current_issue_url = None

# Close the driver
driver.quit()

# Fetch additional article details concurrently
with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
    future_to_article = {executor.submit(fetch_article_details, article): article for article in articles}
    for future in as_completed(future_to_article):
        updated_article = future.result()

# Save data to JSON and CSV
with open("articles_sage.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
df = pd.DataFrame(articles)
df.to_csv("articles_sage.csv", index=False, encoding="utf-8")

print("Data saved to articles_sage.json and articles_sage.csv.")

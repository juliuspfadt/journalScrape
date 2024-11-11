import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json

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
wait = WebDriverWait(driver, 20)  # Increased timeout

base_url = "https://journals.sagepub.com"
current_issue_url = f"{base_url}/toc/pssa/15/1"
journal_name = "Psychological Science"
articles = []

# Function to extract article details from the TOC page
def extract_article_data(article, volume, issue_number, journal_name, pub_year):
    title = article.find("h5", class_="issue-item__heading").text.strip()
    authors = [author.text.strip() for author in article.find_all("span", id=lambda x: x and x.startswith("author"))]
    doi_suffix = article.find("a", href=True)["href"]
    doi_link = base_url + doi_suffix
    pages = article.find("span", string=lambda x: x and "pp." in x).text.strip() if article.find("span", string=lambda x: x and "pp." in x) else "N/A"
    
    article_type = article.find("span", class_="issue-item-access").find_next_sibling("span").text.strip() if article.find("span", class_="issue-item-access") else "N/A"
    pdf_link = article.find("a", {"title": "download"})
    pdf_url = base_url + pdf_link["href"] if pdf_link else "N/A"

    return {
        "Journal": journal_name,
        "Volume": volume,
        "Issue": issue_number,
        "Publication Year": pub_year,
        "Title": title,
        "Authors": ", ".join(authors),
        "Author Affiliations": "Pending",
        "Pages": pages,
        "Type": article_type,
        "DOI": doi_link,
        "PDF Link": pdf_url
    }

# Function to fetch additional data from individual article pages
def fetch_article_details(article_data, index, total, retries=3):
    for attempt in range(retries):
        try:
            driver.get(article_data["DOI"])
            print(f"Fetching details for article {index + 1} of {total}: {article_data['Title']} (Attempt {attempt + 1})")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            page_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Extract citation count
            citation_count = page_soup.find("span", class_="cross-ref-count font-weight-semibold")
            article_data["Citations"] = citation_count.text.split(":")[1].strip() if citation_count else "N/A"

            # Extract affiliations, separated by semicolons
            affiliations = []
            affiliation_section = page_soup.find("section", id="tab-contributors")
            if affiliation_section:
                affiliations = [
                    aff.find("span", property="name").text.strip()
                    for aff in affiliation_section.find_all("div", property="affiliation")
                    if aff.find("span", property="name")
                ]
            article_data["Author Affiliations"] = "; ".join(affiliations) if affiliations else "N/A"
            return article_data  # Success; exit function
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {article_data['Title']}: {e}")
            time.sleep(2 + random.random() * 2)  # Short delay before retry
    article_data["Citations"] = "Error"
    article_data["Author Affiliations"] = "Error"
    return article_data

# Loop through issues
while current_issue_url:
    try:
        driver.get(current_issue_url)
        time.sleep(0.5)

        # Parse the TOC page
        toc_soup = BeautifulSoup(driver.page_source, "html.parser")
        volume_issue_info = toc_soup.find("div", class_="spd__title").get_text(strip=True).replace("Volume ", "").replace("Issue ", "").split(", ")
        volume = volume_issue_info[0].split()[0] if len(volume_issue_info) > 0 else "N/A"
        issue_number = volume_issue_info[0].split()[1] if len(volume_issue_info[0].split()) > 1 else "N/A"
        publication_date = toc_soup.find("span", string=lambda x: x and "First published" in x)
        pub_year = publication_date.text.replace("First published ", "").split()[-1] if publication_date else "N/A"

        for article in toc_soup.find_all("div", class_="issue-item"):
            article_data = extract_article_data(article, volume, issue_number, journal_name, pub_year)
            articles.append(article_data)

        print(f"Processed issue {volume}, Issue {issue_number} with {len(articles)} articles so far.")
        next_issue_link = toc_soup.find("a", class_="content-navigation__btn--next")
        current_issue_url = base_url + next_issue_link.get("href") if next_issue_link and next_issue_link.get("href") else None
    except urllib3.exceptions.ReadTimeoutError:
        print(f"Timeout occurred while accessing {current_issue_url}. Retrying...")
        time.sleep(5)  # Wait before retrying
        continue

# Fetch citation details and affiliations
for idx, article in enumerate(articles):
    fetch_article_details(article, idx, len(articles))

# Save data
df = pd.DataFrame(articles)
df.to_csv("results/Sage/articles.csv", index=False, encoding="utf-8")
with open("results/Sage/articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("Data saved to articles.csv and articles.json.")
driver.quit()

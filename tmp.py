from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

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
    
    # Extract the article type
    article_type = article.find("span", class_="issue-item-access").find_next_sibling("span").text.strip() if article.find("span", class_="issue-item-access") else "N/A"
    
    return {
        "Journal": journal_name,
        "Publication Year": pub_year,
        "Volume": volume,
        "Issue": issue_number,
        "Title": title,
        "Authors": ", ".join(authors),
        "DOI": doi_link,
        "Pages": pages,
        "Article Type": article_type
    }

# Function to fetch additional data from individual article pages and extract Crossref citation count
def fetch_article_details(article_data):
    driver.get(article_data["DOI"])
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extract Crossref citation count
        crossref_citation = page_soup.find("span", class_="cross-ref-count font-weight-semibold")
        if crossref_citation:
            article_data["Crossref Citations"] = crossref_citation.text.split(":")[1].strip()
            print(f"Crossref Citations for {article_data['Title']}: {article_data['Crossref Citations']}")
        else:
            article_data["Crossref Citations"] = "N/A"
            print(f"No Crossref citation found for {article_data['Title']}")
    except Exception as e:
        print(f"Error accessing {article_data['Title']}: {e}")
        article_data["Crossref Citations"] = "Error"
    
    return article_data

# Process each issue with a limit of 3 clicks on the "Next issue" button
issue_count = 1
while current_issue_url and issue_count <= 3:
    driver.get(current_issue_url)
    time.sleep(1)  # Adjust delay as needed

    # Parse the TOC page
    toc_soup = BeautifulSoup(driver.page_source, "html.parser")
    volume_issue_info = toc_soup.find("div", class_="spd__title").get_text(strip=True).replace("Volume ", "").replace("Issue ", "").split(", ")
    volume = volume_issue_info[0].split()[0] if len(volume_issue_info) > 0 else "N/A"
    issue_number = volume_issue_info[0].split()[1] if len(volume_issue_info[0].split()) > 1 else "N/A"

    # Extract data for each article
    for article in toc_soup.find_all("div", class_="issue-item"):
        article_data = extract_article_data(article, volume, issue_number, journal_name)
        articles.append(article_data)

    print(f"Processed {len(articles)} articles in Issue {issue_number} of Volume {volume}")

    # Find the "Next issue" link
    next_issue_link = toc_soup.find("a", class_="content-navigation__btn--next")
    if next_issue_link and next_issue_link.get("href"):
        current_issue_url = base_url + next_issue_link.get("href")
        issue_count += 1
    else:
        print("No more issues.")
        current_issue_url = None

# Fetch Crossref citation details for each article
for article in articles:
    fetch_article_details(article)

# Convert to DataFrame and save data
df = pd.DataFrame(articles)
df.to_csv("results/Sage/articles_with_citations.csv", index=False, encoding="utf-8")
print("Data saved with Crossref citations.")

# Close the driver
driver.quit()

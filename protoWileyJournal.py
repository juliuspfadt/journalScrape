import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import random
import json

# List of User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
]

# Initialize WebDriver options
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")  # Block images
options.add_argument("--disable-javascript")  # Disable JavaScript if not essential
options.add_argument("--disable-background-networking")  # Minimize background tasks
options.add_argument("--disable-sync")  # Disable Chrome Sync
options.add_argument("user-agent=" + random.choice(USER_AGENTS))

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 5)

# Base URL and article storage
base_url = "https://onlinelibrary.wiley.com"
articles = []

# Function to retrieve issues for a specific year
def retrieve_issues(year_url):
    driver.get(year_url)
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "loi__issues")))
    except Exception as e:
        print(f"Error waiting for issue list: {e}")
        return

    year_soup = BeautifulSoup(driver.page_source, "html.parser")
    issues = year_soup.find_all("div", class_="loi__issue")

    # Sort issues based on issue number
    sorted_issues = sorted(
        issues,
        key=lambda x: int(x.find("h4").text.strip().split("Issue ")[1])
    )

    for issue in sorted_issues:
        issue_link = issue.find("a", href=True)["href"]
        issue_url = base_url + issue_link
        issue_label = issue.find("h4").text.strip()
        
        retrieve_articles_from_issue(issue_url, issue_label)

# Function to retrieve articles from an issue
def retrieve_articles_from_issue(issue_url, issue_label):
    driver.get(issue_url)
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toc-wrapper")))
    except Exception as e:
        print(f"Error waiting for articles: {e}")
        return
    
    issue_soup = BeautifulSoup(driver.page_source, "html.parser")
    sections = issue_soup.find_all("div", class_="issue-items-container")

    for section in sections:
        article_type = section.find("h3", class_="toc__heading").text.strip() if section.find("h3", class_="toc__heading") else "Unknown"
        articles_in_section = section.find_all("div", class_="issue-item")
        
        for article in articles_in_section:
            title = article.find("h2").text.strip() if article.find("h2") else "N/A"
            authors = ", ".join([author.text.strip() for author in article.find_all("span", class_="author-style")])
            # Extract the DOI link correctly
            doi_suffix = article.find("a", class_="issue-item__title", href=True)["href"]
            # Extract only the actual DOI part of the URL
            doi_suffix = doi_suffix.split("/doi/")[-1]  # This ensures only the DOI part is kept
            doi_link = f"https://doi.org/{doi_suffix}" if doi_suffix else "N/A"
            page_range = article.find("li", class_="page-range").find_all("span")[1].text if article.find("li", class_="page-range") else "N/A"
            pdf_link = article.find("a", title="EPDF")["href"] if article.find("a", title="EPDF") else "N/A"

            # Extract the full article URL by combining base_url with the href
            article_link = article.find("a", class_="issue-item__title", href=True)
            article_url = base_url + article_link["href"] if article_link else "N/A"

            # Fetch additional article details from article page
            additional_info = retrieve_article_details(article_url)

            articles.append({
                "Journal": "Developmental Science",
                "Volume": issue_label.split(",")[0].replace("Volume ", ""),
                "Issue": issue_label.split(",")[1].replace("Issue ", ""),
                "Publication Year": additional_info.get("publication_year", "N/A"),
                "Title": title,
                "Authors": authors,
                "Author Affiliations": additional_info.get("affiliations", "Pending"),
                "Pages": page_range,
                "Type": article_type,
                "DOI": doi_link,
                "PDF Link": pdf_link if pdf_link != "N/A" else "N/A",
                "Citations": additional_info.get("citations", "N/A"),
                "Article URL": article_url
            })
            print(f"Added article: {title}")

# Function to retrieve additional article details from the article page
def retrieve_article_details(article_url):
    details = {}
    driver.get(article_url)
    
    article_soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Extract 'Publication Year' from metadata
    publication_year = article_soup.find("meta", {"name": "citation_publication_date"})
    details["publication_year"] = publication_year["content"].split("/")[0] if publication_year else "N/A"
    
    # Extract the citations count, keeping only the number
    citations = article_soup.find("div", class_="cited-by-count")
    if citations:
        # Split the text to get only the number part
        details["citations"] = citations.text.strip().split(": ")[-1]
    else:
        details["citations"] = "N/A"
    
    # Extract affiliations
    author_affiliations = []
    for meta_tag in article_soup.find_all("meta", {"name": "citation_author_institution"}):
        author_affiliations.append(meta_tag["content"])
    details["affiliations"] = "; ".join(author_affiliations) if author_affiliations else "N/A"

    return details

# Loop through the range of years + 1
for year in range(2004, 2025):  # Modify range as needed
    print(f"Processing articles for the year {year}...")
    retrieve_issues(f"{base_url}/loi/14677687/year/{year}")

# Save to CSV and JSON
df = pd.DataFrame(articles)
df.to_csv("results/Journals/Wiley/ds_articles.csv", index=False, encoding="utf-8")
with open("results/Journals/Wiley/ds_articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("Data saved to CSV and JSON.")
driver.quit()

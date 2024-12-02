
# change the links for different journals
# for getting the pdf links, one needs to have authorization, aka, a license
# if there is no authorization, the pdf links will be empty

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment for headless mode if desired
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

# Define the target TOC page URL
# toc_url = 'https://www.sciencedirect.com/journal/behaviour-research-and-therapy/vol/42/issue/1'
# or 
toc_url = 'https://www.sciencedirect.com/journal/journal-of-experimental-social-psychology/vol/40/issue/1'

driver.get(toc_url)
time.sleep(3)  # Wait for page to load

# List to store article data
toc_articles = []
page_count = 1  # Track the number of pages navigated

while True:
    print(f"Processing page {page_count}...")

    # Locate all articles in the TOC
    articles = driver.find_elements(By.CSS_SELECTOR, "li.js-article-list-item.article-item")

    # Parse each article entry for the desired details
    for article in articles:
        try:
            # Initialize an empty dictionary to hold article data
            article_data = {}

            # Extract Title and Article URL
            title_element = article.find_element(By.CSS_SELECTOR, "h3.text-m a.anchor")
            article_data['Title'] = title_element.text
            article_data['Article URL'] = title_element.get_attribute("href")

            # Extract Authors
            try:
                authors = article.find_element(By.CSS_SELECTOR, "dd.js-article-author-list").text
                article_data['Authors'] = authors
            except:
                article_data['Authors'] = "N/A"

            # Extract PDF link
            try:
                pdf_link_element = article.find_element(By.CSS_SELECTOR, "a.pdf-download")
                article_data['PDF Link'] = pdf_link_element.get_attribute("href")
            except:
                article_data['PDF Link'] = "N/A"

            # Extract Article Type
            try:
                article_type = article.find_element(By.CSS_SELECTOR, "span.js-article-subtype").text
                article_data['Article Type'] = article_type
            except:
                article_data['Article Type'] = "N/A"

            # Append the article data to the list
            toc_articles.append(article_data)

        except Exception as e:
            print(f"Error processing article: {e}")

    # Check if the "Next vol/issue" button is disabled
    try:
        next_issue_button = driver.find_element(By.CSS_SELECTOR, "div.navigation-next a")
        is_disabled = next_issue_button.get_attribute("aria-disabled")
        
        if is_disabled == "true":
            print("No further issues to navigate to.")
            break  # Exit the loop if "Next vol/issue" button is disabled
        else:
            print(f"Moving to the next issue (Page {page_count + 1})...")
            next_issue_button.click()
            time.sleep(3)  # Wait for the next page to load
            page_count += 1  # Increment the page count
    except:
        print("Next vol/issue button not found.")
        break

# Close the driver
driver.quit()

# Save TOC data to CSV
toc_df = pd.DataFrame(toc_articles)
# toc_df.to_csv("results/Journals/Elsevier/brt_toc_articles.csv", index=False)
toc_df.to_csv("results/Journals/Elsevier/jesp_toc_articles.csv", index=False)

print("TOC data saved to toc_articles.csv")

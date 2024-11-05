import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define the base URL for the journal (replace with the actual journal's URL)
base_url = 'https://psycnet.apa.org/PsycARTICLES/journal/xge/153/11'

# Define the period for which to collect articles
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

def fetch_article_titles(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Update selectors based on website structure
    articles = []
    for article in soup.select('div.article'):  # Adjust based on actual HTML tags
        title = article.select_one('h3.article-title').get_text(strip=True)  # Adjust selector as needed
        date_str = article.select_one('span.date').get_text(strip=True)  # Adjust selector as needed
        
        # Convert date string to datetime object
        article_date = datetime.strptime(date_str, '%Y-%m-%d')  # Update format as needed
        if start_date <= article_date <= end_date:
            articles.append((title, article_date))
    
    return articles

def main():
    all_articles = []
    
    # Loop through pages (update range and URL as needed)
    for page in range(1, 6):  # Example: iterate through 5 pages
        page_url = f"{base_url}?page={page}"
        articles = fetch_article_titles(page_url)
        if not articles:
            break
        all_articles.extend(articles)
        print(f"Fetched {len(articles)} articles from page {page}")
    
    # Print or save the collected articles
    for title, date in all_articles:
        print(f"{date}: {title}")

if __name__ == '__main__':
    main()

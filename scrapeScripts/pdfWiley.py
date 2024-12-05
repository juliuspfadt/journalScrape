import requests
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def setup_driver():
    """
    Set up the Selenium WebDriver.
    """
    chrome_options = Options()
    # Uncomment for headless mode
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_path = "/opt/homebrew/bin/chromedriver"  # Replace with your ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def extract_headers_and_cookies(driver, sample_article_url):
    """
    Extract headers and cookies from a Selenium session after visiting a sample article page.
    """
    driver.get(sample_article_url)
    print(f"Accessing {sample_article_url}")

    # Wait for the page to load completely
    driver.implicitly_wait(20)

    # Extract cookies
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

    # Create headers
    headers = {
        "User-Agent": driver.execute_script("return navigator.userAgent;"),
        "Referer": sample_article_url,
        "Accept": "application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "Connection": "keep-alive"
    }
    return headers, cookies


def sanitize_doi(doi):
    """
    Sanitize a DOI for use as a filename by replacing invalid characters with unique replacements.
    """
    replacements = {
        "/": "__",
        ":": "_COLON_",
        "?": "_QUESTION_",
        "<": "_LT_",
        ">": "_GT_",
        "|": "_PIPE_",
        '"': "_QUOTE_",
        "*": "_STAR_",
        "\\": "_BACKSLASH_"
    }
    for char, replacement in replacements.items():
        doi = doi.replace(char, replacement)
    return doi


def download_pdf(pdf_url, headers, cookies, output_dir, doi):
    """
    Download the PDF using the provided URL and save it locally with a sanitized DOI as the filename.
    """
    try:
        # Use only the actual DOI part (remove 'https://doi.org/')
        if doi.startswith("https://doi.org/"):
            doi = doi.split("https://doi.org/")[1]

        # Sanitize DOI for use in the file name
        sanitized_doi = sanitize_doi(doi)
        pdf_filename = os.path.join(output_dir, f"{sanitized_doi}.pdf")

        response = requests.get(pdf_url, headers=headers, cookies=cookies, stream=True)
        response.raise_for_status()

        # Save the PDF
        with open(pdf_filename, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)

        print(f"PDF saved: {pdf_filename}")
        return True
    except requests.RequestException as e:
        print(f"Error downloading PDF from {pdf_url}: {e}")
        return False


def transform_pdf_link(epdf_link):
    """
    Transform the `PDF Link` (epdf) to the `pdfdirect` download link.
    """
    return epdf_link.replace("/epdf/", "/pdfdirect/") + "?download=true"


def process_articles(file_path, resume=False, limit=20):
    """
    Process articles from the specified dataset and download their PDFs (limited to 20 for debugging).
    """
    # Create a dedicated download directory
    output_dir = os.path.join(os.getcwd(), "ds_downloads")
    os.makedirs(output_dir, exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Limit processing to the first 20 rows for debugging
    df = df.head(limit).reset_index()

    # Check for resuming
    last_successful_index_file = "wiley_last_successful_index.txt"
    start_index = 0
    if resume and os.path.exists(last_successful_index_file):
        with open(last_successful_index_file, "r") as f:
            saved_index = f.read().strip()
            if saved_index.isdigit():
                start_index = int(saved_index) + 1
                print(f"Resuming from index {start_index}")

    # Set up Selenium WebDriver
    driver = setup_driver()

    # Extract headers and cookies using the first article link
    first_article_url = df.iloc[0]["PDF Link"]
    headers, cookies = extract_headers_and_cookies(driver, first_article_url)

    # Close the Selenium WebDriver
    driver.quit()

    # Process each article starting from the last successful index
    for index, row in df.iloc[start_index:].iterrows():
        epdf_link = row["PDF Link"]
        doi = row["DOI"]

        if pd.notnull(epdf_link) and pd.notnull(doi):
            pdf_link = transform_pdf_link(epdf_link)
            print(f"Processing DOI: {doi}, PDF Link: {pdf_link}")

            success = download_pdf(pdf_link, headers, cookies, output_dir, doi)
            if not success:
                print(f"Download failed. Last successful index: {index - 1}")
                with open(last_successful_index_file, "w") as f:
                    f.write(str(index - 1))
                break
            else:
                with open(last_successful_index_file, "w") as f:
                    f.write(str(index))

    print("Processing complete.")


# Example usage
file_path = "results/Journals/Wiley/ds_articles_cleaned.csv"  # Replace with your CSV file path
process_articles(file_path, resume=True, limit=2000)

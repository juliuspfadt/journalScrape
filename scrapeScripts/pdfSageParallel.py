from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import os
import re
import pandas as pd
from multiprocessing import Pool, Manager


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


def extract_headers_and_cookies(driver, sample_epub_url):
    """
    Extract headers and cookies from a Selenium session after visiting a sample EPUB page.
    """
    driver.get(sample_epub_url)
    print(f"Accessing {sample_epub_url}")
    driver.implicitly_wait(10)
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
    headers = {
        "User-Agent": driver.execute_script("return navigator.userAgent;"),
        "Referer": sample_epub_url,
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


def download_pdf_with_requests(task):
    """
    Download the PDF using requests with extracted headers and cookies.
    """
    pdf_url, headers, cookies, output_dir, doi, index, success_list = task
    try:
        sanitized_doi = sanitize_doi(doi)
        pdf_filename = os.path.join(output_dir, f"{sanitized_doi}.pdf")
        response = requests.get(pdf_url, headers=headers, cookies=cookies, stream=True)
        response.raise_for_status()
        with open(pdf_filename, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"PDF saved: {pdf_filename}")
        success_list[index] = True
    except requests.RequestException as e:
        print(f"Error downloading PDF from {pdf_url}: {e}")
        success_list[index] = False


def process_articles_parallel(file_path, resume=False):
    """
    Process all articles from the specified journal in parallel, with failure handling and progress tracking.
    """
    output_dir = os.path.join(os.getcwd(), "pss_downloads")
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)
    journal_name = "Psychological Science"
    psych_sci_articles = df[df['Journal'] == journal_name].reset_index()

    # Resume from failed indexes if needed
    if resume and os.path.exists("failed_indexes_sage.txt"):
        with open("failed_indexes_sage.txt", "r") as f:
            failed_indexes = list(map(int, f.read().strip().split(",")))
        psych_sci_articles = psych_sci_articles.iloc[failed_indexes]

    driver = setup_driver()
    first_doi_url = psych_sci_articles.iloc[0]['DOI']
    sample_epub_url = f"https://journals.sagepub.com/doi/epub/{first_doi_url.split('https://doi.org/')[1]}"
    headers, cookies = extract_headers_and_cookies(driver, sample_epub_url)
    driver.quit()

    tasks = []
    manager = Manager()
    success_list = manager.dict()

    for index, row in psych_sci_articles.iterrows():
        doi_url = row['DOI']
        if pd.notnull(doi_url):
            doi = doi_url.split('https://doi.org/')[1]
            pdf_url = f"https://journals.sagepub.com/doi/pdf/{doi}?download=true"
            tasks.append((pdf_url, headers, cookies, output_dir, doi, index, success_list))

    with Pool(processes=4) as pool:
        pool.map(download_pdf_with_requests, tasks)

    failed_indexes = [index for index, success in success_list.items() if not success]
    if failed_indexes:
        print(f"Failed downloads at rows: {failed_indexes}")
        with open("failed_indexes_sage.txt", "w") as f:
            f.write(",".join(map(str, failed_indexes)))
    else:
        print("All downloads completed successfully.")
        if os.path.exists("failed_indexes_sage.txt"):
            os.remove("failed_indexes_sage.txt")


if __name__ == "__main__":
    # Path to the input CSV file
    file_path = "results/Articles/combined_journals.csv"

    # Set resume to True to pick up where it left off
    process_articles_parallel(file_path, resume=True)

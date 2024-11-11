import requests
import json
import pandas as pd

# Persistent session setup
session = requests.Session()
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Origin": "https://psycnet.apa.org",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "_ga=GA1.2.284430323.1731156832; _ga_H2KGDH2XNS=GS1.1.1731333575.6.1.1731335410.0.0.0; _gid=GA1.2.2122662503.1731333576; nlbi_2377601_2147483392=mDCOS3LCtD8tFpl7RZi9EAAAAADRjFomxspvcM7ADuFDL0F3; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+11+2024+15%3A30%3A10+GMT%2B0100+(Central+European+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=af09d6d1-1099-4935-9c02-aa36e5c266c0&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false&geolocation=NL%3BNH; reese84=3:PiFQyW4oxJCawufTR9VjTg==:O9f8R90upEmDQYVYbNLN3ArsdcRTwG/imUJQrZilCAiexak1KxoWIZ5qJHE0Rt6ca/iWfxfsmd2MhwVzPPqhyq9YxdhOPn3v1ZPL8L4lv0mlhBy7UjoO5uq+2DHTVDRLe28hnYgELLMiyFJpAkUemNi37qrk7Anw5QkGavvvUw361C0dQBUSfPUC9WE1V6aRhigDGWGASzzoiTV8gtIvwSZArnOa2dPbUdUwa0QM6K8nmUvQQ1OgRBBJczOQECOaPg/DmWmfGEpXErEFiawVSPUoUBJ073P6FSThas1FRy/2pwxlfoDO0Z10wYg3pS77u8hb7zbdmUJdv9pSQ6bLmZFW86wnkEAkSltTsvtjQ6XUQBTRZ1w3IG+AhZv6hSZTJx6OeAjeaEHim1bZ4zd6B60hsW5xEM162poBOMT7Cywyis+IeoWnClD/z8zEEzwKnAxvUJlk7efpvC5UIWnn0w==:DqIMa9gikXzzHpADXFUey5SM5R1xxTQjhbtic/fXflc=; cId=71dc670e-253a-48a2-8c38-62a1c4aac68f; _dc_gtm_UA-10493335-18=1; incap_ses_699_2624409=5FaNWgtWXzL50zTd9VizCekUMmcAAAAArbsTgaDcu9+7oReGoLY1XQ==; nlbi_2377603_2147483392=+sy8WywGnD5zvz6b900V4wAAAAC1NK77xCPr8Usb+E+IL3x+; incap_ses_420_2624409=f7X+IqZYBRGDktPm9CPUBQ4RMmcAAAAATizMQreQoesRzegV8ftxXg==; incap_ses_410_2624409=CWUfE//0RRbyzg53Ap2wBQMRMmcAAAAAkiqPMCkBe767xvXwsqAm0Q==; incap_ses_349_2624409=kBGHWNz2uTgL5Yo61eXXBMIOMmcAAAAAji6jOJtixOynv0SAHsQgVQ==; PN_RC=true; incap_ses_679_2624409=VBqZcv+KiwOhj4n5EEtsCf0NMmcAAAAAq8PB+Qdkaz1Fmizq34Ha2g==; nlbi_2624409=quUEH2OuNhVGwiGQzJKtcwAAAAAtp06ksmvs84A+JEmIQ8ps; cart_my_apa_org=92e7bb16-0ba2-4b29-9368-ae99e2ac355e; incap_ses_6524_2624409=3P1WYrbwPnpqjcF8m+eJWsYNMmcAAAAAhKQtNjLEKBiGSMlLBAD3Cw==; visid_incap_2624409=s1C+rYfqSnSBj9z+U2p8VcYNMmcAAAAAQUIPAAAAAAB+4jxVRzR6TpHTdSBkrP50; incap_ses_1687_2377601=IlXAZR6tGAc/yC7GqW1pF8YNMmcAAAAAwx6m9dLUYnZvceV0F363Iw==; nlbi_2377601=jyAiE+1hQxDH+JoRRZi9EAAAAAAHMhGYg63qzPMBWhCeT9+g; PN_HOST=https%3A%2F%2Fpsycnet.apa.org; connect.sid=s%3ANpaHS-aGKtdYeTQODXrLZIhBJsh02mP9.tuOrGNH6PecXETFqip7KOdtoY64uBfhCQYnvr8kStvc; csId=e6a74c61-650f-4006-9158-7c55801df8f0; incap_ses_1687_2377603=4bTeZFCiEjb8vS7GqW1pF8MNMmcAAAAAnM8VoVFXanPzXHMIb1wCBw==; nlbi_2377603=pWSfDYAluGNfsxBg900V4wAAAACPIwMtQQ4J8LMepVwgei1B; _ga_SZXLGDJGNB=GS1.1.1731162489.1.0.1731162490.59.0.0; _gcl_au=1.1.894300664.1731162489; visid_incap_2624412=n6nSMdzwTGy9qMxBxa+ShHhxL2cAAAAAQUIPAAAAAAA1+G3doyfkgylK56398OCK; OptanonAlertBoxClosed=2024-11-09T12:53:51.504Z; visid_incap_2377601=f+Ow2L9GTGyyPhM6c+s81lQABWcAAAAAQUIPAAAAAAAMTtEFYdPkqwj2KA6PzSdZ; visid_incap_2377603=4OR7OJjtTNmG/QfoEA8JZlUABWcAAAAAQUIPAAAAAADfTIEoJvpWu5CXKy1ybFGE"
}

# Function to get volumes and years within a specified range
def get_volumes(start_year=2004, end_year=2024):
    url = "https://psycnet.apa.org/api/request/browsePA.getVolumes"
    payload = {
        "api": "browsePA.getVolumes",
        "params": {"code": "xge"}
    }
    response = session.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        volumes = response.json().get("response", {}).get("facet", {}).get("values", [])
        return [
            {"volume": vol["Volume"], "year": vol["Year"]}
            for vol in volumes
            if start_year <= int(vol["Year"]) <= end_year
        ]
    else:
        print(f"Failed to get volumes: {response.status_code} - {response.text}")
        return []

# Function to get issues for a specific volume
def get_issues(volume):
    url = "https://psycnet.apa.org/api/request/browsePA.getIssues"
    payload = {
        "api": "browsePA.getIssues",
        "params": {"code": "xge", "volume": volume}
    }
    response = session.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        issues = response.json().get("response", {}).get("facet", {}).get("doc", [])
        issue_numbers = sorted(
            [issue.get("str")[0]["value"] for issue in issues if issue.get("str")],
            key=lambda x: int(x) if x.isdigit() else x
        )
        return issue_numbers  # Sorted as strings for correct API format
    else:
        print(f"Failed to get issues for volume {volume}: {response.status_code} - {response.text}")
        return []

# Function to get articles for a specific volume and issue
def get_articles(volume, issue, year, retries=3):
    url = "https://psycnet.apa.org/api/request/browsePA.getArticles"
    payload = {
        "api": "browsePA.getArticles",
        "params": {
            "code": "xge",
            "volume": volume,
            "issue": str(issue)  # Ensure issue is a string for the API request
        }
    }
    for attempt in range(retries):
        response = session.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            docs = response.json().get("response", {}).get("result", {}).get("doc", [])
            
            articles = []
            for doc in docs:
                authors = ', '.join(doc.get("AuthorOrig", []))
                pages = f"{doc.get('PAFirstPage', 'N/A')}-{doc.get('Pagination', 'N/A')}" if doc.get("PAFirstPage") else "N/A"
                
                # Format DOI and PDF Link as URLs
                doi = doc.get("DOI", "N/A")
                doi_link = f"https://doi.org/{doi}" if doi and not doi.startswith("http") else doi
                pdf_link = doc.get("PDFLink", "N/A")
                pdf_link = f"https://psycnet.apa.org{pdf_link}" if pdf_link and not pdf_link.startswith("http") else pdf_link

                article_data = {
                    "Journal": doc.get("PIJournalTitle", "N/A"),
                    "Volume": volume,
                    "Issue": issue,
                    "Publication Year": year,
                    "Title": doc.get("GivenDocumentTitle", "N/A"),
                    "Authors": authors,
                    "Pages": pages,
                    "Type": doc.get("SubjectHeadingList", {}).get("SubjectHeadingLevel1", "N/A"),
                    "DOI": doi_link,
                    "PDF Link": pdf_link
                }
                articles.append(article_data)
            print(f"  Retrieved {len(articles)} articles from volume {volume}, issue {issue}.")
            return articles
        else:
            print(f"Attempt {attempt + 1} failed for volume {volume}, issue {issue}: {response.status_code} - {response.text}")
            time.sleep(2)  # Wait before retrying
    print(f"Failed to access articles for volume {volume}, issue {issue} after {retries} attempts.")
    return []

# Main process to retrieve data and save to CSV and JSON
all_data_csv = []  # Initialize for CSV
all_data_json = {}  # Initialize for JSON

# Retrieve volumes and issues within the specified range in chronological order
print("Starting data retrieval...")
volumes = sorted(get_volumes(), key=lambda x: int(x["year"]))
print(f"Found {len(volumes)} volumes between 2004 and 2024.")

for vol_info in volumes:
    volume = vol_info["volume"]
    year = vol_info["year"]
    print(f"Processing volume {volume} for year {year}...")
    issues = get_issues(volume)
    print(f"  Found {len(issues)} issues in volume {volume}.")
    all_data_json[volume] = {}  # Initialize volume in JSON structure
    for issue in issues:
        articles = get_articles(volume, issue, year)
        all_data_json[volume][issue] = articles  # Save to JSON structure
        for article in articles:
            # Append flattened article data for CSV
            all_data_csv.append({
                "Journal": article["Journal"],
                "Volume": volume,
                "Issue": issue,
                "Publication Year": year,
                **article
            })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_data_csv)
df.to_csv("results/APA/articles.csv", index=False)
print("Data saved to articles.csv")

# Save all data to JSON file
with open('results/APA/articles.json', 'w') as file:
    json.dump(all_data_json, file, indent=4)
print("All data saved to 'articles.json'")
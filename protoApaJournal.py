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
    "Cookie": "_ga_H2KGDH2XNS=GS1.1.1731174065.4.1.1731176349.0.0.0; cId=71dc670e-253a-48a2-8c38-62a1c4aac68f; nlbi_2377601_2147483392=7f1cLY0yjWUjwHW/RZi9EAAAAACIWdzGZkuuu95apcHueIZ8; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Nov+09+2024+19%3A19%3A09+GMT%2B0100+(Central+European+Standard+Time)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=af09d6d1-1099-4935-9c02-aa36e5c266c0&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1&AwaitingReconsent=false&geolocation=NL%3BNH; reese84=3:Ei9Y+g4w3XcAIVOdXFIaYg==:tHr+ZmxMErMxMn4PhDl9CwN6ersJFbLG9vhescCvXG+pL2pW4aq+PDBce1Z2cWjsdoGDgfpNuqBQHttINLvxl46bduH8jZX1VkPi5aGC2fyK6oC/NrR2HsButiuZkfXJ6u6jSfqg9+3fsD5dXjgoepPD3I1VvGr0LTjozQTN2wnsAQJuMUmihv5NwCFYG021U7nbTb3Id8SchCbQag+Dxulzhzpx9qlMldJcp8W7XXEvcQu3X1Xgaiu8fQkjTI1X1V9fWgRISrhV5LuwsEPmAeurzArcYAoPKEf4tALJ/wB/Dmm+9EFZHEdw/Rr+utC7o2GpacNRS4oFUPuM80gP9Sl/N2vJ4B7ooA3Oqrq4b9UIqTiRKl8AipZRgCiomL0+QRDnlVtDnlut6LhnBu3MBmCC4MvOhHdZqiFxSVXqjaMDY/fscmBmEheVZdg1QKNANwgHd98uN0nta+0prFbpDQ==:zXnQQvHrd//OJQQvpzcnzYiXrlG4LHYTahuYGbbjM5c=; _ga=GA1.2.284430323.1731156832; _gid=GA1.2.1782037811.1731156832; incap_ses_502_2624409=g29icAm9o1X7GsNgg3b3Bk+iL2cAAAAAVqAcCeN2cQJeSjJXH4DBtQ==; incap_ses_1782_2377603=og9YCcDngGgNcx7suO+6GE+iL2cAAAAAV4n1wwWoz2PejS+1WUWjnA==; incap_ses_336_2624409=rcZOUAgiMy0R3zKEa7apBLGeL2cAAAAApBQsU64nRg+ibiiY65+dpA==; PN_HOST=https%3A%2F%2Fpsycnet.apa.org; PN_RC=false; connect.sid=s%3AFOX82w214iqtVNx-FfbXB9TDFYw_Jbza.0pMHaTDp9p3qwKQPJgqXZRxQ7nkbjfjRrg1nAcY%2Fx4o; incap_ses_7232_2624409=yxGFZo9VZ0YhFXrc2DldZOCOL2cAAAAAViayXpD68El2aBC8nJL8dQ==; incap_ses_261_2624409=drQKZbMPAg3ERWxESkKfA2KOL2cAAAAAXPEZUsQL/SuD9jurysFukw==; incap_ses_419_2624409=8F3MJHfKaHtMyNT1c5bQBZCML2cAAAAAaHlWKLKOKlRPT+OTCebVAg==; incap_ses_333_2624409=AxIGJ41P7yk6b5o1Ag6fBOmLL2cAAAAApheH38qtyISyNpW6hhT+yw==; nlbi_2624409=AAZnVN9GRVVbaLHOzJKtcwAAAADcKCG/JXSNsCC9U90qr8Qt; incap_ses_1782_2377601=CWabcyMdeFCI4xTsuO+6GOmLL2cAAAAAF2LB9+VbTwQssEbazYnPFg==; nlbi_2377601=zqQYVATeuVSQiIpbRZi9EAAAAABXSM9ZLTFbQa4g+1+HmjXr; nlbi_2377603_2147483392=0D7zFbAUTDM1ij6S900V4wAAAADXp1/rdlWySU2/6N6m1dAV; csId=94fa063d-7d9c-44fd-bc93-8fdbfa16280b; nlbi_2377603=yErYTki+R3pa8AY7900V4wAAAABEdgchhsMOyqVvYhC8T9yT; _ga_SZXLGDJGNB=GS1.1.1731162489.1.0.1731162490.59.0.0; _gcl_au=1.1.894300664.1731162489; visid_incap_2624412=n6nSMdzwTGy9qMxBxa+ShHhxL2cAAAAAQUIPAAAAAAA1+G3doyfkgylK56398OCK; OptanonAlertBoxClosed=2024-11-09T12:53:51.504Z; cart_my_apa_org=87161e35-13e4-457b-806b-596f73efa7e3; visid_incap_2624409=h0Yo2IutRXStB1w+KKtKm169KGcAAAAAQUIPAAAAAAC7a7FTUlrHt2KzMJ4HcVXL; visid_incap_2377601=f+Ow2L9GTGyyPhM6c+s81lQABWcAAAAAQUIPAAAAAAAMTtEFYdPkqwj2KA6PzSdZ; visid_incap_2377603=4OR7OJjtTNmG/QfoEA8JZlUABWcAAAAAQUIPAAAAAADfTIEoJvpWu5CXKy1ybFGEE"
}

# Function to get volumes and years within a specified range
def get_volumes(start_year=2000, end_year=2024):
    url = "https://psycnet.apa.org/api/request/browsePA.getVolumes"
    payload = {
        "api": "browsePA.getVolumes",
        "params": {"code": "xge"}
    }
    response = session.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        volumes = response.json().get("response", {}).get("facet", {}).get("values", [])
        # Filter for specified years
        return [
            {"volume": vol["Volume"], "year": vol["Year"]}
            for vol in volumes
            if start_year <= int(vol["Year"]) <= end_year
        ]
    else:
        print(f"Failed to get volumes: {response.status_code}")
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
        issue_numbers = []
        for issue in issues:
            for detail in issue.get("str", []):
                if detail["name"] == "Issue":
                    issue_numbers.append(detail["value"])
                    break
        return issue_numbers
    else:
        print(f"Failed to get issues for volume {volume}: {response.status_code}")
        return []

# Function to get articles for a specific volume and issue
def get_articles(volume, issue):
    url = "https://psycnet.apa.org/api/request/browsePA.getArticles"
    payload = {
        "api": "browsePA.getArticles",
        "params": {
            "code": "xge",
            "volume": volume,
            "issue": issue
        },
        "logs": {
            "eventType": "Journal TOC",
            "pageId": "B_PA_TOC"
        }
    }
    response = session.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        docs = response.json().get("response", {}).get("result", {}).get("doc", [])
        
        articles = []
        for doc in docs:
            # Convert authors list to comma-separated string without brackets or quotes
            authors = ', '.join(doc.get("AuthorOrig", []))

            article_data = {
                "title": doc.get("GivenDocumentTitle"),
                "authors": authors,
                "DOI": doc.get("DOI"),
                "journal_title": doc.get("PIJournalTitle"),
                "publication_year": doc.get("PublicationYear"),
                "volume": doc.get("PAVolume"),
                "issue": doc.get("PAIssue"),
                "first_page": doc.get("PAFirstPage"),
                "pagination": doc.get("Pagination"),
                "month_season": doc.get("MonthSeason"),
                "abstract_available": doc.get("HasAbstract") == "true",
                "open_access": doc.get("HasOpenAccess") == "true",
                "subject_headings": doc.get("SubjectHeadingList", {}).get("SubjectHeadingLevel1"),
                "cited_by_count": doc.get("CitedByCount"),
                "impact_statement_available": doc.get("HasImpactStatement") == "true",
                "full_text_available": doc.get("HasFullText") == "true",
                "PIReleaseDate": doc.get("PIReleaseDate"),
                "UID": doc.get("UID"),
                "ProductCode": doc.get("ProductCode"),
                "XMLLink": doc.get("XMLLink"),
                "PDFLink": doc.get("PDFLink"),
                "PAIssueCode": doc.get("PAIssueCode"),
                "PAJournalCode": doc.get("PAJournalCode"),
                "AuthorObjects": doc.get("AuthorObjects", []),
                "HasCitations": doc.get("HasCitations"),
                "HasInfographic": doc.get("HasInfographic"),
                "SFXOpenURL": doc.get("SFXOpenURL"),
                "JournalEditors": doc.get("JournalEditors", []),
                "ContributorList": doc.get("ContributorList", []),
                "isRetracted": doc.get("isRetracted"),
                "RightsLink": doc.get("RightsLink"),
                "HasAccess": doc.get("HasAccess"),
                "MayAccessRecordDetails": doc.get("MayAccessRecordDetails"),
                "HasAcceptedManuscript": doc.get("HasAcceptedManuscript")
            }
            articles.append(article_data)
        return articles
    else:
        print(f"Failed to get articles for volume {volume}, issue {issue}: {response.status_code}")
        return []

# Main process to retrieve data and save to CSV and JSON
all_data_csv = []  # Initialize for CSV
all_data_json = {}  # Initialize for JSON

volumes = get_volumes()  # Gets volumes between 2000 and 2024
for vol_info in volumes:
    volume = vol_info["volume"]
    year = vol_info["year"]
    issues = get_issues(volume)
    all_data_json[volume] = {}  # Initialize volume in JSON structure
    for issue in issues:
        articles = get_articles(volume, issue)
        all_data_json[volume][issue] = articles  # Save to JSON structure
        for article in articles:
            # Append flattened article data for CSV
            all_data_csv.append({
                "journal_title": article["journal_title"],  # First element in CSV rows
                "volume": volume,
                "year": year,
                "issue": issue,
                **article
            })


# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_data_csv)
df.to_csv("results/articles_wide_format.csv", index=False)
print("Data saved to articles_wide_format.csv")

# Save all data to JSON file
with open('results/all_articles.json', 'w') as file:
    json.dump(all_data_json, file, indent=4)
print("All data saved to 'all_articles.json'")

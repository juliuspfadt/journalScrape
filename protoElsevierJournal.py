import cloudscraper

# Initialize cloudscraper, which can handle Cloudflare protection
scraper = cloudscraper.create_scraper()

# Set up the API URL and parameters
url = "https://www.sciencedirect.com/search/api?cid=271799&date=2004-2004&pub=Behaviour%20Research%20and%20Therapy&show=100&sortBy=date&t=b2bea8931965191740cebf4326a31a21c4702b6189ecfc4834eca439039c02f3b31e31d6f3c7875cddaff1ea5e64cc6bb6ead2dbdc558d419228e4307723f952a73f53b89aa7c586928044fae7a11b8b31b9e02aa3f189ab7fb57868e07f184514cbf85106eba2be3cae9a054f2bb164&hostname=www.sciencedirect.com"
params = {
    'cid': '271799',
    'date': '2004-2004',
    'pub': 'Behaviour Research and Therapy',
    'show': '100',
    'sortBy': 'date',
    't': 'b2bea8931965191740cebf4326a31a21c4702b6189ecfc4834eca439039c02f3b31e31d6f3c7875cddaff1ea5e64cc6bb6ead2dbdc558d419228e4307723f952a73f53b89aa7c586928044fae7a11b8b31b9e02aa3f189ab7fb57868e07f184514cbf85106eba2be3cae9a054f2bb164',
    'hostname': 'www.sciencedirect.com',
}

# Headers, including User-Agent and Referer
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    'Accept': 'application/json',
    'Referer': 'https://www.sciencedirect.com/search?pub=Behaviour%20Research%20and%20Therapy&cid=271799&date=2004-2004&sortBy=date&show=100',
}

# Make the API request with cloudscraper
response = scraper.get(url, headers=headers, params=params)

# Check the response
if response.status_code == 200:
    print("Data retrieved successfully!")
    data = response.json()
    print(data)
else:
    print("Failed to retrieve data:", response.status_code)

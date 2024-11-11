from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if desired
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the URL
url = "https://www.sciencedirect.com/search/api?cid=271799&date=2004-2004&pub=Behaviour%20Research%20and%20Therapy&show=100&sortBy=date&t=f3a58e0e7e3f991d8630b44327aa4de2c4702b6189ecfc4834eca439039c02f3b31e31d6f3c7875cddaff1ea5e64cc6bb6ead2dbdc558d419228e4307723f952a73f53b89aa7c586928044fae7a11b8b50fa47c73a2f0530c1f7871f041b6c7714cbf85106eba2be3cae9a054f2bb164&hostname=www.sciencedirect.com"
driver.get(url)

# Wait for the page to fully load
time.sleep(5)  # Adjust as needed

# Retrieve the page source or specific elements
page_source = driver.page_source
print(page_source)  # For debugging purposes; see if the desired content is available

# Close the driver
driver.quit()

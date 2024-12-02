
# journalScrape

Scrape specific journal websites for article types, titles, authors, years, volumes, issues, page numbers, and DOIs. 

# Setup
- I am using: 
  - macOS arm64 system
  - vscode for editing and running python script
  - python3 and pip installed through homebrew and added to vscode
- create venv and choose homebrew installed python3 as the interpreter

# Disclaimer
The following is a somewhat overpowered setup. If the interest lies only with common article metadata, it is easiest to adjust the script in the scrapeScripts subfolder [metadata from Crossref](scrapeScripts/getCitationCountFromCrossref.py). With that script most metadata can be easily collected if some best practices from Crossref are adhered to. For instance, an email address and some patience in accessing the site.

Since we are also interested in the article type so we can exclude the non-empirical articles (for our research purpose), we are going through the journal websites and record the article type from the ToCs. However, anyone wanting to replicate this should be aware that accessing the journal websites in such a fashion will result in being blocked and sometimes getting a formal warning from publishers.

# Workflow for APA journal
- use API requests in a python script. The requests are not easy to be found, but eventually I extracted them from the journal website page source
- in order for that to work we need to access the journal website in a browser and get the data:
  - using safari go to the website > Develop > Show Page Source > Network > Reload > filter results for type 'xhr' > find the getArticles request > Headers > fill your own information into the headers in the script. Not entirely certain which headers are needed; depends a bit on the website, the headers in my script seemed to be enough even though I needed to refresh the cookie sometimes when trying to rerun the script. Probably fewer headers are also fine.
- run the script

# Workflow for Sage, Springer, Wiley, and Elsevier
- run the scripts

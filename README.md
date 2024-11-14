# journalScrape

Scrape specific journal websites for article titles, authors, years, volumes, issues, page numbers, and dois.

# Setup
- I am using: 
  - macOS arm64 system
  - vscode for editing and running python script
  - python3 and pip installed through homebrew and added to vscode
- create venv and choose homebrew installed python3 as the interpreter


# Workflow for APA journal
- use API requests in a python script. The requests are not easy to be found, but eventually I extracted them from the journal website page source
- in order for that to work we need to access the journal website in a browser and get the data:
  - using safari go to the website > Develop > Show Page Source > Network > Reload > filter results for type 'xhr' > find the getArticles request > Headers > fill your own information into the headers in the script. Not entirely certain which headers are needed; depends a bit on the website, the headers in my script seemed to be enough even though I needed to refresh the cookie sometimes when trying to rerun the script. Probably fewer headers are also fine.
- run the script

# Workflow for Sage, Springer, Wiley, and Elsevier
- run the scripts

# DOGE Scraper

This is a project to scrape the Department of Government Efficiency website to grab useful information for ease of processing. 

## dogeAPIScrape.py
* There's actually an api to scrape from the doge.gov website at [https://api.doge.gov](https://api.doge.gov)
* This script will go through the api endpoints and create large csvs from all of the endpoints provided
* This should be the main script that should be used to scrape the DOGE data, but the web scraping functionality from the other scripts can be used as a fallback

## dogeScrape.py
* dogeScrape handles accessing doge.gov to grab all of the data and download the raw html from each of the tables
* As of now, the scraper manually clicks on every pagination link for each table and simply downloads the entire selected paginated table

## tableParse.py
* After the html files are scraped, the tableParse script will actually process all of the html data and turn it into csv files

## exploreData.py
* This is sort of my data playgroud that I use to test the scripts, make a report, etc.


## Notes
- There are a lot of FPDS links that has some missing data. The missing data is denoted by a lack of text in a table cell. You can take a look at the exploreData script to see the rows that have missing data. 
- The web scraping is rendered basically useless given that there is an api to grab all of the data already, but sometimes the api may not work (payments api wasn't working on April 11th), so the web scraping functionality can be useful to use as a fallback in case the api isn't up.



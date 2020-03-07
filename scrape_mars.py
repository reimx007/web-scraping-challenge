# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url1 = "https://mars.nasa.gov/news/"
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3 = "https://twitter.com/marswxreport?lang=en"
    url4 = "https://space-facts.com/mars/"
    # browser.visit(url1)

    # SCRAPE THE 1ST SITE!
    time.sleep(1)
    response1 = requests.get(url1)
    # Scrape page into Soup
    html1 = response1.text
    soup1 = bs(html1, "html.parser")
    news_title = soup1.find_all('div', class_="content_title")[0].text
    news_p = soup1.find('div', class_="rollover_description_inner").text

    # SCRAPE THE 2ND SITE using splinter!
    browser = init_browser()
    browser.visit(url2)
    time.sleep(1)
    # Scrape page into Soup
    html2 = browser.html
    soup2 = bs(html2, "html.parser")
    partial_url = soup2.find_all('img')[3]["src"]
    categories = soup2.find_all('article')
    image_url = "https://www.jpl.nasa.gov" + partial_url

    # SCRAPE THE 3RD SITE!  //// unsuccessful /////
    response3 = requests.get(url3)
    time.sleep(1)
    # # Scrape page into Soup
    html3 = response3.text
    soup3 = bs(html3, "html.parser")
    tweet = soup3.find_all('p', class_='TweetTextSize')[0].text

    # SCRAPE THE 4TH SITE AND GRAB AN HTML TABLE!
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Attribute', 'Value']
    df.set_index('Attribute', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('mars_facts.html')

    # Create a dictionary of some more photo links!
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    ]

    # Store all this wonderful data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p" : news_p,
        "image_url": image_url,
        "tweet": tweet,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
# print("runs through successfully")

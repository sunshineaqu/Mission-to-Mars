from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}
    
    # news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    print(soup)
    
    news_mars = soup.find('div', class_='list_text')
    mars["news_title"] = news_mars.find('a').text
    mars["news_p"] = news_mars.find('div', class_='article_teaser_body').text

    # Space images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #??? this need to be double checked
    featured_image = soup.find('article', class_='carousel_item')['style']
    start = featured_image.find('(') + 2
    end = featured_image.find(')') - 1
    mars["featured_image_url"] = ("https://www.jpl.nasa.gov" + featured_image[start:end])

    # Weather
    url = 'https://twitter.com/marswxreport'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # locate the first weather report (newest)
    mars["mars_weather"] = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description',inplace=True)
    mars["html_table"] = df.to_html()
    # html_table.replace('\n', '')

    # Mars Hemispheres; ???this can be simplified
    title = []
    image_url = []

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser') 

    hemi_title = soup.find('h2', class_='title').text
    title.append(hemi_title)    
    downloads = soup.find_all('div', class_='downloads')
    for image in downloads:
        hemi_url= image.find('a', string='Original')['href']
        image_url.append(hemi_url)
    time.sleep(20)

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
    hemi_title = soup.find('h2', class_='title').text
    title.append(hemi_title)    
    downloads = soup.find_all('div', class_='downloads')
    for image in downloads:
        hemi_url= image.find('a', string='Original')['href']
        image_url.append(hemi_url)
    time.sleep(20)

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
    hemi_title = soup.find('h2', class_='title').text
    title.append(hemi_title)    
    downloads = soup.find_all('div', class_='downloads')
    for image in downloads:
        hemi_url= image.find('a', string='Original')['href']
        image_url.append(hemi_url)
    time.sleep(20)

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
    hemi_title = soup.find('h2', class_='title').text
    title.append(hemi_title)    
    downloads = soup.find_all('div', class_='downloads')
    for image in downloads:
        hemi_url= image.find('a', string='Original')['href']
        image_url.append(hemi_url)
    time.sleep(20)

    #????dic inside dic
    mars['hemisphere_image_urls'] = dict(zip(title, image_url))

    return mars


# Dependencies
import os
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd
from selenium import webdriver

#Initiate browser helper function
def init_browser():
    exec_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **exec_path, headless=False)

#List of URLs to explore and scrape
url1 = 'https://mars.nasa.gov/news/'
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url3 = 'https://twitter.com/marswxreport?lang=en'
url4 = 'http://space-facts.com/mars/'
url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


def scrape ():
    mars_data = {}

    # NASA Mars News

    # Mars News URL (url1)
    browser = init_browser()
    browser.visit(url1)

    # Retrieve page with the requests module
    html = requests.get(url1)
    time.sleep(1)
    html = browser.html

    ## Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'html.parser')

    # Get title & description
    news_title_1 = soup.find('div', 'content_title', 'a').text
    news_p_1 = soup.find('div', 'rollover_description_inner').text

    news_title = news_title_1.strip()
    news_title

    news_p = news_p_1.strip()
    news_p

    # Return results
    #return news_title

    #return news_p

    # Store results in dictionary

    mars_data["news_title"] = news_title

    mars_data["news_p"] = news_p


    # JPL Mars Space Images

    # Mars Featured Image (url2)
    browser = init_browser()
    browser.visit(url2)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    time.sleep(1)

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{img_relative}'
        #print (featured_image_url)
    
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA17440_ip.jpg'
    
        # Capture Image
    img = jpl_soup.find('img', {'id':'main_image'})['src']  
    featured_image = {
            "featured_image_url": img,
        }
    
    # Return results
    #return featured_image

    # Store results in dictionary
    mars_data["featured_image_url"] = featured_image_url
    mars_data ["featured_image"] = featured_image

    # Mars Weather

    # Mars Weather URL (url3)
    browser = init_browser()
    browser.visit(url3)
    time.sleep(1)

    # Get weather using BeautifulSoup
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, "html.parser")

    # tweets = mars_weather_soup.find('ol', class_='stream-items')
    # mars_weather = tweets.find('p', class_="tweet-text").text
    
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break
    
        #print(mars_weather)

    # Return results
    #return mars_weather

    # Store results in dictionary
    mars_data["mars_weather"] = mars_weather

    # Mars Facts URL
    browser = init_browser()        
    browser.visit(url4)
    time.sleep(1)
    mars_facts_html = browser.html
    mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    facets = []
    values = []

    for row in column1:
        facet = row.text.strip()
        facets.append(facet)
            
    for row in column2:
        value = row.text.strip()
        values.append(value)
            
    mars_facts = pd.DataFrame({
        "Facet":facets,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)
    mars_facts

    # Return results
    #return mars_facts

    # Store results in directory
    mars_data["mars_facts"] = mars_facts

    # Mars Hemispheres URL (url5) & Dictionary to store results
    hemi_dicts = []

    for i in range(1,9,2): 
        hemi_dict = {}
        browser.visit(url5)
        time.sleep(1)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(1)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(1)
        
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']
        #print(hemi_name)
        hemi_dict['title'] = hemi_name.strip()
        #print(hemi_img_path)
        hemi_dict['img_url'] = hemi_img_path
        hemi_dicts.append(hemi_dict)

    # Store data in dictionary
    
        mars_data["hemi_dicts"] = hemi_dicts

    browser.quit()

return mars_data


if __name__ == "__main__":
    print(scrape())
from bs4 import BeautifulSoup as bs
import requests
from flask_pymongo import pymongo
import pandas as pd
import time
import os
import json
from splinter import Browser
from selenium import webdriver


#intialize the browser
def init_browser():
    #path to chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)
  
def scrape():
    browser = init_browser()
    # Create empty dictionary to insert into mongodb
    mars_data = {}
    #Nasa Mars News
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    
    # Display mars news title and news paragraph
    html = browser.html
    soup = bs(html, 'html.parser')

    news_titles = soup.find('div', class_="content_title").text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    print(f"News Title : {news_titles}")
    print(f"News Content : {news_paragraph} ")
    mars_data["news_title"] = news_titles
    mars_data["news_content"] = news_paragraph

    
    #JPL Mars Space Images-Featured Images
    #url_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    browser.find_link_by_partial_text("FULL IMAGE").click()
    time.sleep(10)
    browser.find_link_by_partial_text("more info").click()
    time.sleep(5)
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    img_url=  soup.find('img',class_="main_image")["src"]
    
    mars_data["Featured_Image_Url"] = "https://www.jpl.nasa.gov/" + img_url
    
    
    #Mars Weather from twitter
    weather_info_dict = []
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")

    time.sleep(3)
    tweets = soup.find_all("div",class_='js-tweet-text-container')
    mars_weather=""
    for tweet in tweets:
        if tweet.p.get_text().startswith("Sol "):
            mars_weather = tweet.p.get_text()
            break
 
    mars_data["Latest_Mars_Weather"] = mars_weather
    
    #Mars Facts
    url_facts = "https://space-facts.com/mars/"
    fact_df = pd.read_html(url_facts)
    
    mars_fact_df = fact_df[0]
    mars_fact_df.columns =["Description","Value"]
    #print(mars_fact_df)
    mars_fact_table = mars_fact_df.to_html(na_rep = " ",classes="table table-sm table-striped", justify="left",col_space=0)
   #mars_fact_table = mars_fact_table.replace("\n","")
    print(mars_fact_table)
    mars_data["Mars_Facts"] = mars_fact_table
    
    #collection of title and images for Mars hemispheres
    #collection of title and images for Mars hemispheres
    hemisphere_image_urls = []
    
    hemisphere_names = ['cerberus%20enhanced', 'schiaparelli%20enhanced','syrtis%20major%20enhanced','valles%20marineris%20enhanced']
    for hemis in hemisphere_names:
        base ='https://astrogeology.usgs.gov/search/map/Mars/Viking/' + hemis
        browser.visit(base)
        html_hm = browser.html
        soup3 = bs(html_hm,'html.parser')
        #hemisphere_image_urls["image_url"] = soup3.find('img',class_='wide-image')['src']
        imagelist = soup3.find('div',class_="wide-image-wrapper").find_all('li')
        img_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"+ hemis.replace("%20","_") + ".tif/full.jpg"
        hemisphere_image_urls.append({"hems_title" : soup3.find('h2',class_='title').text,"image_url": img_url} )

    mars_data["Mars_Hemisphere_urls"] = hemisphere_image_urls
    browser.quit()

    return mars_data

if __name__ == "__main__":
    print(scrape())
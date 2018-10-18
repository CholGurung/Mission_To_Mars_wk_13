from bs4 import BeautifulSoup as bs
import requests
from flask_pymongo import pymongo
import pandas as pd
import time
import os
from splinter import Browser


#intialize the browser
def init_browser():
    #path to chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
  
def scrape():
    browser = init_browser()
    # Create empty dictionary to insert into mongodb
    mars_data = {}
    #Nasa Mars News
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    
    # Display mars news title and news paragraph
    html = browser.html
    soup = bs(html, "lxml")

    news_titles = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    print(f"News Title : {news_titles}")
    print(f"News Content : {news_paragraph} ")
    mars_data["news_title"] = news_titles
    mars_data["news_content"] = news_paragraph

    
    #JPL Mars Space Images-Featured Images
    url_images = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_images)
    
    #get the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_images))
    print(base_url)

    #Design an xpath selector to grab the images
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    #use splinter to bring images
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = base_url + img_url
    print(featured_image_url)
    mars_data["Featured_Image_Url"] = featured_image_url
    
    
    #Mars Weather from twitter
    weather_info_dict = []
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")

    for mars_weather in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_info_dict.append(mars_weather.text)
    
    print('Latest Mars Weather: ' +  weather_info_dict[8])
    mars_data["Latest_Mars_Weather"] = weather_info_dict[8]
    
    #Mars Facts
    url_facts = "https://space-facts.com/mars/"
    fact_df = pd.read_html(url_facts)
    mars_fact_df = fact_df[0]
    #print(mars_fact_df)
    mars_fact_table = mars_fact_df.to_html()
    mars_fact_table = mars_fact_table.replace("\n","")
    print(mars_fact_table)
    mars_data["Mars_Facts"] = mars_fact_table
    
    #collection of title and images for Mars hemispheres
    hemisphere_image_urls = []
    hemisphere_dict = {"title": [] , "image_url": []}

    base_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(base_url)
    time.sleep(3)
    usgs_html = browser.html

    usgs_html_soup = bs(usgs_html, "html.parser")
    results = usgs_html_soup.find_all("h3")

    # Use splinter to parse title and image urls
    for result in results:
        title = result.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        image_url = browser.find_link_by_partial_href("download")["href"]
        hemisphere_dict = {"title": title, "image_url": image_url}
        hemisphere_image_urls.append(hemisphere_dict)
        time.sleep(1)
        browser.visit(usgs_url)
    print(hemisphere_img_urls)
    mars_data["Mars_Hemisphere_urls"] = hemisphere_img_urls
    browser.quit()

    return mars_data

if __name__ == "__main__":
    print(scrape())
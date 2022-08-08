#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies
import pandas as pd
import time
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def scrape():
    
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visiting the site for NASA's news
    url ="https://redplanetscience.com/"

    # open the url
    browser.visit(url)
    
    # empty dictionary for listings to save to mongo
    data_mars = {}

    # basically let the page load
    time.sleep(1)

    # scrape the page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # get latest news title and paragraph
    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()

    # Mars image url
    url = 'https://spaceimages-mars.com/'

    # open the url
    browser.visit(url)

    # basically let the page load
    time.sleep(1)

    # scrape page the into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find the image
    featured_image = soup.find_all('img')[2]["src"]

    #create the url for the image
    image = url + featured_image

    # NASA's mars facts url
    url = 'https://galaxyfacts-mars.com/'

    # parse the url
    table = pd.read_html(url)

    # converting to df and renaming columns
    facts = table[0]
    facts.columns=['Description', 'Mars', 'Earth']
    facts = facts.drop([0])

    # converting to html
    fact_table = facts.to_html()
    fact_table.replace('\n','')

    # Mars Hemispheres url
    url = 'https://marshemispheres.com/'
    
    # open the url
    browser.visit(url)
    
    # basically let the page load
    time.sleep(1)

    # new list to hold titles and images
    hemisphere_urls = []

    # loop through the data to find title and url info
    for item in range(4):
        # browse through each article
        browser.links.find_by_partial_text('Hemisphere')[item].click()

        # parse the HTML
        html = browser.html
        hemi_soup = BeautifulSoup(html,'html.parser')

        # scraping
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')

        # store findings into a dictionary and append to list
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_urls.append(hemispheres)

        # browse back to repeat
        browser.back()

    # create mars data dictionary to hold above scraped data
    mars_data = {
        "news_title": news_title,
        "paragraph" : news_p,
        "featured_image_url": image,
        "html_table": fact_table,
        "hemisphere_img_urls": hemisphere_urls
        }

    # close the browser after scraping
    browser.quit()

    # return our dictionary
    return data_mars


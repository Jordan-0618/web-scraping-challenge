#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Dependencies
import pandas as pd
import os
import time
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():

#path to driver
    executable_path = {'executable_path':r'C:\Users\Jordan\OneDrive\Desktop\chromedriver'}
    return Browser('chrome', **executable_path, headless = False)

data = {}

#### NASA Mars News

def scrape_info():
    browser = init_browser()
#Visit URL
    url = 'https://redplanetscience.com/'
    browser.visit(url)


#HTML Object
    html = browser.html

#Parse with beatiful soup
    soup = bs(html, 'html.parser')


#collect the latest News Title and Paragraph Text
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    data['news_title'] = news_title
    data['news_paragraph'] = news_p


#### JPL Mars Space Images - Featured Image

#Visit URL
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)


#HTML Object
    image_html = browser.html

#Parse with beautiful soup
    image_soup =  bs(image_html, 'html.parser')

#Find image url full size
    image_path = image_soup.find_all('img')[3]["src"]

#Find image link
    featured_image_url = image_url + image_path
    
    
    data['featured_image_url'] = featured_image_url


#### Mars Facts

#Visit URL
    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)



#Use Pandas to scrape the table containing facts about the planet
    table = pd.read_html(facts_url)
    table


#Create dataframe
    facts_df = table[0]
    facts_df

    mars_facts_df = facts_df.drop(labels=0, axis=0)
    mars_facts_df


    mars_facts_df.columns = ['Description','Mars', 'Earth']
    mars_facts_df

#convert the data to a HTML table string
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_df.to_html('mars_facts_df.html')

    data['mars_facts'] = mars_facts_html


#### Mars Hemispheres


#Visit URL
    astro_url = 'https://marshemispheres.com/'
    browser.visit(astro_url)



#HTML Object
    hemisphere_html = browser.html

#Parse with beautiful soup
    hemisphere_soup = bs(hemisphere_html, 'html.parser')



#Retrieve all items
    hemispheres = hemisphere_soup.find_all('div', class_='item')

# #Create empty list
    hemisphere_img_urls = []

# # #Main URL for loop
    hemi_url = 'https://marshemispheres.com/'

    for i in hemispheres:
        title = i.find('h3').text
        hemispheres_img = i.find('a', class_='itemLink product-item')['href']

# Visit full image website link
        browser.visit(hemi_url + hemispheres_img)

# HTML Object
        hemi_img_html = browser.html
        hemi_info = bs(hemi_img_html, 'html.parser')

# Create full image url
        img_url = hemi_url + hemi_info.find('img', class_='wide-image')['src']
        hemisphere_img_urls.append({'title' : title, 'img_url' : img_url})

        data['hemisphere_img_urls'] = hemisphere_img_urls

    browser.quit()

    return data





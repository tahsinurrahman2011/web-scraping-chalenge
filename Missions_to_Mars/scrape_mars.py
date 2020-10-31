#!/usr/bin/env python
# coding: utf-8

# In[130]:


from bs4 import BeautifulSoup
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[114]:

def scrape():
    mars_dic = {}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    news_soup = BeautifulSoup(browser.html,'html.parser')
    news_title_tag = news_soup.find_all('div', class_ = 'content_title')[1].find('a')
    news_div = news_soup.find('div', class_ = 'article_teaser_body')

    news_title = news_title_tag.text
    news_parag = news_div.text 
    
    mars_dic['news_title'] = news_title
    mars_dic['news_parag'] = news_parag

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    image_soup = BeautifulSoup(browser.html,'html.parser')
    featured_div = image_soup.find(class_='carousel_items')
    img_rel_path = featured_div.find('article')['style'].split("'")[1]
    featured_image_url = f"https://www.jpl.nasa.gov{img_rel_path}"
    mars_dic['featured_img_link'] = featured_image_url

    mars_facts_url = "https://space-facts.com/mars/" 
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    html_table = df.to_html(index = False, header = False)
    table_string = html_table.replace('\n', '')

    mars_dic['facts'] = table_string

    ast_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(ast_url)
    ast_soup = BeautifulSoup(browser.html,'html.parser')
    link_divs = ast_soup.find_all('div', class_='description')
    url_list = []
    for link in link_divs:
        a_tag = link.find('a')
        title = a_tag.text
        url = f"https://astrogeology.usgs.gov{a_tag['href']}"
        browser.visit(url)
        time.sleep(1)
        res_soup = BeautifulSoup(browser.html,'html.parser')
        high_res_url = res_soup.find(class_="downloads").find("a")["href"]
        url_list.append({'title':title,'img_url':high_res_url})
    
    mars_dic['img_urls'] = url_list
    browser.quit()

    return mars_dic

from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import random
import time
import re
import os

def get_soup(url):

    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    }

    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def get_images(soup, keyword):

    images = []

    for img in soup.find_all('img'):

        try:

            img_url = img.attrs['src']

            if img_url.startswith('http'):

                images.append(img_url)

        except:

            pass

    return images

def download_images(images, keyword):

    if not os.path.exists(f'../data/scraped/{keyword}'):

        os.makedirs(f'../data/scraped/{keyword}')

    for i, img_url in enumerate(images):

        try:

            img_name = f'output/{keyword}/{keyword}_{i}.jpg'
            urllib.request.urlretrieve(img_url, img_name)

        except:

            pass

def scrape_images(keyword):

    # https://duckduckgo.com/?q=chair&iax=images&ia=images&iaf=type%3Atransparent
    url = f'https://www.google.com/search?q={keyword}&tbm=isch'
    soup = get_soup(url)
    images = get_images(soup, keyword)
    download_images(images, keyword)

    print(f'Scraped {len(images)} images of {keyword}.')

# Anieesh Saravanan, 3, 2025
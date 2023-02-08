from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import json
import os

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# Create a new instance of the Firefox driver
options = Options()
options.headless = True

for link in config['links']:
    driver = webdriver.Firefox(options=options)
    print('Scraping ' + link['name'] + '...')

    # Navigate to the page
    driver.get(link['url'])

    # Parse the page HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the image elements
    images = soup.select("ul.vignette-list img")

    # create a folder to store the images
    folder = 'images/' + link['name']
    print("Creating folder " + folder)
    if not os.path.exists(folder):
        os.makedirs(folder)

    print("Downloading " + str(len(images)) + " images")
    # Loop through the images and download them
    num = 0
    for image in images:
        num += 1
        img_url = image['src']
        
        # save the image
        img_data = requests.get(img_url).content
        with open(folder + "/" + str(num) + '.jpg', 'wb') as handler:
            handler.write(img_data)

    # Close the browser
    driver.quit()

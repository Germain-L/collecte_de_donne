from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Use Selenium to load the HTML content
driver = webdriver.Firefox()

columns = ["make_model", "odometer", "drive", "transmission", "paint color", "size", "type", "fuel", "title_status", "condition", "cylinders"]

head = "make_model,odometer,drive,transmission,paint color,size,type,fuel,title_status,condition,cylinders"
print(head)
keys = []


data = []
for i in range(0, 5):
    url = f"https://boston.craigslist.org/search/boston-ma/cta#search=1~gallery~{i}~0"
    driver.get(url)

    # await for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gallery-card")))

    html_content = driver.page_source

    # Convert the HTML content to a BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the div with the id "search-results-page-1" and extract the list items
    div = soup.find("div", {"id": "search-results-page-1"})
    ol = div.find("ol")
    lis = ol.find_all("li")

    # Create an empty list to store the href values
    href_list = []

    # Extract the href values from each list item
    for li in lis:
        a = li.find("a")
        href = a.get("href")
        href_list.append(href)

    done = []

    # Only keep the some of the href values to speed up the process
    href_list = href_list[:15]

    for href in href_list:
        if href in done:
            continue
            
        done.append(href)
        # Navigate to the page
        driver.get(href)

        # await for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "attrgroup")))

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        # Page contains 2 divs with class attrgroup
        atr = soup.find_all("p", {"class": "attrgroup"})

        # First div contains the name of the car
        name = atr[0].find("span").text
        attributes = {}

        
        # Second div contains the attributes of the car
        for i in range(1, len(atr[1])):
            try:
                # html looks like this : cylinders: <b>4 cylinders</b>
                # so we need to get the text after the <b> tag after  the :
                # remove after :
                key = atr[1].find_all("span")[i].text
                key = key.split(":")[0]
                
                if key not in keys:
                    keys.append(key)

                value = atr[1].find_all("b")[i].text
                attributes[key] = value
            except:
                pass
        
        line = ""

        attributes["make_model"] = name

        for col in columns:
            if col in attributes:
                line += attributes[col] + ","
            else:
                line += '"",'
        
        print(line)

# Close the web driver
driver.quit()
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

url = r"https://twitter.com/DWD_klima/likes"

url1 = "https://www.dnb.com/business-directory/top-results.html?term=dalmer&page=1"


def selenium(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        executable_path=r"C:/Users/Sangamithra/Desktop/twitter/geckodriver.exe",
        options=options,
    )
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.close()
    html = BeautifulSoup(html)
    return html


soup = selenium(url)

print(soup)

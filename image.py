import requests
from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome("C:/Users/exces/Downloads/chromedriver.exe", chrome_options=options)


url = 'https://media.discordapp.net/attachments/777207889424941116/796157629364830218/ba051517170b2463660981ce3ea1767d71-lorde.png'
r = requests.get(url, allow_redirects=True)

# open('lorde.jpg', 'wb').write(r.content)

def tin(url: str):
        return "https://www.tineye.com/search?url={}".format(parse.quote_plus(url))

titles_element = driver.find_elements_by_xpath("//h4")

print(tin(url))
print(titles_element)




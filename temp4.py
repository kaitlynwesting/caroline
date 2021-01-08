from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

url = 'https://www.tineye.com'
chrome_driver_path = 'C:/Users/exces/Downloads/chromedriver.exe'
#CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
#GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1260, 600")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')


webdriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# default search query
search_query = "https://media.discordapp.net/attachments/730415274003529769/796414444804505600/image0.webp?width=446&height=669"

if (len(sys.argv) >= 2):
  search_query = sys.argv[1]
  print(search_query)

i = 0

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 10)

    # retrive url in headless browser
    driver.get(url)

    # find search box

    wait.until(EC.presence_of_element_located((By.XPATH, "//input [@id='url_box']")))
    
    search = driver.find_element_by_xpath("//input [@id='url_box']") 
    search.send_keys(search_query + Keys.RETURN)
    
    wait.until(presence_of_element_located((By.XPATH, "//div[@id='results-div']")))
    time.sleep(3)
    results = driver.find_elements_by_xpath("//h4")

    for item in results:
    
      print(f"{results[i].text}")
      # print(rating[i])

      i = i + 1

    """ for quote in results:
      quoteArr = quote.text.split('\n')
      print(quoteArr)
      print() """

    # must close the driver after task finished
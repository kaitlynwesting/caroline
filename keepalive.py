from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys
from urllib import parse

url = 'https://media.discordapp.net/attachments/730415274003529769/796414444804505600/image0.webp?width=446&height=669'
chrome_driver_path = 'C:/Users/exces/Downloads/chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

def tin(url: str):
  result = "https://www.tineye.com/search?url={}".format(parse.quote_plus(url))
  return result

print(tin(url))

with webdriver as driver:
    # Set timeout time
    wait = WebDriverWait(driver, 10) 
    

    # retrive url in headless browser
    driver.get(tin(url))
  
    # time.sleep(3)
    wait.until(presence_of_element_located((By.ID, "results-div")))

    results = driver.find_elements_by_class_name('commercial-info')

    print(results)
    """ for quote in results:
      quoteArr = quote.text.split('\n')
      print(quoteArr)
      print() """

    # must close the driver after task finished
    # driver.close()
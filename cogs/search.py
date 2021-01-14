from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import time
import discord
import traceback
import sys
import random
from discord.ext import commands

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=["doc", "d", "search"])
    async def docs(self, ctx, *, query):

        await ctx.send("Fetching most relevant results from Adobe help centre, just for you. Please allow a few seconds...")
        print("Okay")   
        url = 'https://helpx.adobe.com/support.html'
        # chromedriver_path = 'C:/Users/exces/Downloads/chromedriver.exe'
        chromedriver_path = '/app/.chromedriver/bin/chromedriver.'
        google_chrome_bin = '/app/.apt/usr/bin/google-chrome'
        
        chrome_options = Options()
        chrome_options.binary_location = google_chrome_bin
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1260, 600")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

        print(query)
        search_query = str(query)

        with driver as driver:
            
            print("searching now...")
            # Set timeout time 
            wait = WebDriverWait(driver, 10)

            # retrive url in headless browser
            driver.get(url)

            wait.until(EC.presence_of_element_located((By.XPATH, "//h1 [@class = 'page-title']")))
            
            search = driver.find_element_by_xpath("//input [@id='uss-search-input']") 
            search.send_keys(f"photoshop {search_query}" + Keys.RETURN)
            
            
            wait.until(presence_of_element_located((By.XPATH, "//h3[@class = 'spectrum-Heading spectrum-Heading--subtitle2 ResultsListTitle-scopeName']")))

            driver.find_element_by_xpath("//input [@value = 'Adobe Photoshop']").click()

            time.sleep(1)
            titles = driver.find_elements_by_xpath("//div [@class = 'ResultsListItem-title--clamped']")
            results = driver.find_elements_by_xpath("//div [@class = 'ResultsListItem-content-excerpt-text']")
            links = driver.find_elements_by_xpath("//a [@class = 'spectrum-Link spectrum-Link--quiet ResultsListItem-content-excerpt-footer-link']")
            # total = results = driver.find_elements_by_xpath("//div [@class = 'ResultsListStackShort']")

            print(type(results))
            urlNow = driver.current_url
            tempStr = ""
            resultNum = 0       

            for i, content in enumerate(results):
            
                try:
                
                    overflow = len(str(tempStr)) + len(titles[1].text) + len(content.text)
                    print(overflow)

                    if overflow < 1010:
                        print("This will do!")
                        resultNum = resultNum + 1                
                        tempStr = tempStr + f"\n[__{titles[i].text}__]({links[i].text})\n{content.text}"
                    else:
                        print("Overflow reached, terminating")
                        break
                except:
                    break
                    
            parsed = search_query.replace(" ", "+")
            parsedUrl = f"https://helpx.adobe.com/search.html?q={parsed}"
            print(parsedUrl)

            embed=discord.Embed(
                title = f"Your search for \"{str(query)}\" returned the following:",
                url = parsedUrl,
                color=0x349feb
                )
            
            embed.add_field(
                name=f"Displaying {resultNum} results from the quicksearch.", 
                value=f"{tempStr[:1010]}... (continued)", # [:1000]
                inline=False)
            embed.set_thumbnail(url="https://filebin.net/i643ziupi21lvy9x/Ice-melting-experiment-1.jpg?t=2y35f7p1")

            await ctx.send(embed=embed) 
                

def setup(bot):
    bot.add_cog(Search(bot))
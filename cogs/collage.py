from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import os
import time
import discord
import traceback
import sys
import random
import urllib.request
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO

class Collage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def collage(self, ctx, name, dimension):

        try:
            dimension = int(dimension)
        except:
            raise commands.ArgumentParsingError()
    
        await ctx.send("📨 Creating your one-of-a-kind **rainbow collage**, please allow up to one minute.")
        print("Okay")   
        url = 'https://thechurchofkoen.com/lastfm/rainbowcollage/'
        #chromedriver_path = 'C:/Users/exces/Downloads/chromedriver.exe' # for local
        chromedriver_path = '/app/.chromedriver/bin/chromedriver.' # for heroku
        google_chrome_bin = '/app/.apt/usr/bin/google-chrome' # for heroku

        chrome_options = Options()
        chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN') # for heroku
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1260, 600")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        #driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)# for local
        driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=chrome_options) # for heroku

        with driver as driver:
            
            print("Searching now...")
            # Set timeout time 
            wait = WebDriverWait(driver, 20)
            smallWait = WebDriverWait(driver, 3)
            invalid = False

            driver.get(url)

            wait.until(EC.presence_of_element_located((By.XPATH, "//input [@name='LastFM_username']")))
            
            # LASTFM USERNAME
            search = driver.find_element_by_xpath("//input [@name='LastFM_username']") 
            search.send_keys(f"{str(name)}")
            
            # X AXIS
            search = driver.find_element_by_xpath("//input [@name='nr_of_albums_x_Axis']") 
            search.send_keys(f"{str(dimension)}")

            # Y AXIS
            search = driver.find_element_by_xpath("//input [@name='nr_of_albums_y_Axis']") 
            search.send_keys(f"{str(dimension)}")

            driver.find_element_by_xpath("//button [@type = 'submit']").click()

            wait.until(EC.presence_of_element_located((By.XPATH, "//button [@class = 'collage-result-back-btn']")))

            try:
                driver.find_element_by_xpath("//p [@class = 'status']")
                await ctx.send("An error occurred. This could be due to a bad username, or not having enough scrobbles.")
            except:
                image = driver.find_element_by_xpath("//img [@alt ='Rainbow Collage']") 
                url = image.get_attribute("src")
                print(url)
                #driver.save_screenshot("screenshot.png")
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                img.save("temp.png")

                await ctx.send(file=discord.File("temp.png"))
                print("Process done!")
    
def setup(bot):
    bot.add_cog(Collage(bot))  
        

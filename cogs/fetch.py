import asyncio

import discord
from discord.ext import commands

import pyppeteer
from pyppeteer import input, launch, connect
import random
import time

# COG USING ASYNC PYPPETEER LIBRARY TO FETCH RESULTS

class Fetch(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["helpcenter", "docs", "doc"])
    async def helpcentre(self, ctx, *, query):
        
        print(f"Currently searching for: {query}...")
        await ctx.send("📨 Fetching most relevant results from **Adobe help centre**, just for you. Please allow up to five seconds...")

        browser = await launch(
            headless=True,
            args=['--start-maximized', '--no-sandbox'],
            autoClose=True
        )

        # Open a new Chromium page and enter the help desk url.
        page = await browser.newPage()
        await page.setViewport({'width': 1536, 'height': 600})
        await page.goto('https://helpx.adobe.com/support.html', {'waitUntil' : 'domcontentloaded'})

        # Enter the query into the search bar.
        search = await page.xpath("//input [@id='uss-search-input']") # Search bar.
        await page.evaluate(f"""() => {{
        document.getElementById('uss-search-input').value = '{query}';
        }}""")

        # Click the search button.
        # await page.waitForSelector('input[id="uss-submit-button"]', timeout=60000),
        await page.click('input[id="uss-submit-button"]')

        # Grab the search results page url.
        url = await page.evaluate("() => window.location.href")

        print("Test I'm here.")
        # Wait for the search results to load.
        time.sleep(3)
        await page.waitForSelector("input[value = 'Adobe Photoshop']", timeout=60000),
        await page.click("input[value = 'Adobe Photoshop']")

        for country in (("US", "FR"), ("CA", "FR"), ("UK", "FR")):
            url = url.replace(*country)
        
        # Check if no results appeared (no results has .EmptyState class).
        bad = await page.querySelector('.EmptyState-suggestions')

        # Send an "Oh noes" error message.
        if bad is not None:
            embed=discord.Embed(
                    title = f"Your search for \"{str(query)}\" returned the following:",
                    url = url,
                    color=0x349feb
                    )
                
            embed.add_field(
                name=f"**🚫 OH NOES!** We were unable to find any matching results. ", 
                value=f'• Ensure all search words are spelled correctly.\n• Try using quotes to search for an entire phrase, such as "crop an image".',
                inline=False)
            
            await ctx.send(embed=embed)
        
        # If results are visible...
        else:
            
            # Get list of ElementHandles - titles, detail paragraphs, and links to posts.
            titles = await page.querySelectorAll('.ResultsListItem-title--clamped')
            details = await page.querySelectorAll('.ResultsListItem-content-excerpt-text')
            links = await page.xpath("//a [@class='spectrum-Link']")

            titlesText, detailsText, linksText = ([] for i in range(3))

            # Convert pesky ElementHandles to readable text.
            for count, t in enumerate(titles):
                content = await page.evaluate('(element) => element.textContent', t)
                titlesText.append(content)

                content = await page.evaluate('(element) => element.textContent', details[count])
                detailsText.append(content)

                content = await page.evaluate('(links) => links.href', links[count])
                linksText.append(content)
            
            contentMessage = ""
            resultNum = 0

            for count in range(len(titlesText)):
                print(count)
                
                length = len(contentMessage) + len(titlesText[count]) + len(detailsText[count]) + len(linksText[count]) 
                print(length)

                if length < 1001:
                    print("This will do!")
                    resultNum = resultNum + 1                
                    contentMessage = contentMessage + f"\n[__{titlesText[count]}__]({linksText[count]})\n{detailsText[count]}"
                else:
                    print("Overflow reached, terminating.")
                    break
            
            embed=discord.Embed(
                    title = f"Your search for \"{str(query)}\" returned the following:",
                    url = url,
                    color=0x349feb
                    )
                
            embed.add_field(
                name=f"Displaying {resultNum} results from the quicksearch.", 
                value=f"{contentMessage}... (continued)", # [:1000]
                inline=False)
            
            logos = []
            embed.set_thumbnail(url="https://i.postimg.cc/mrB2Trx9/Adobe1.jpg")
            await ctx.send(embed=embed)

            print("All done!")
            
            await browser.disconnect()

    # asyncio.get_event_loop().run_until_complete(fetch())

def setup(bot):
    bot.add_cog(Fetch(bot))
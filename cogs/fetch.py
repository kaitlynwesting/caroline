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
        
        print(f"Currently searching for: {query}")
        await ctx.send("📨 Fetching most relevant results from **Adobe help centre**, just for you. Please allow up to five seconds...")

        browser = await launch(
            headless=True,
            args=['--start-maximized', '--no-sandbox'],
            autoClose=True
        )

        page = await browser.newPage()
        await page.setViewport({'width': 1536, 'height': 600})
        await page.goto('https://helpx.adobe.com/support.html', {'waitUntil' : 'domcontentloaded'})

        search = await page.xpath("//input [@id='uss-search-input']") # Search bar.
        print(search)
        await page.evaluate(f"""() => {{
        document.getElementById('uss-search-input').value = '{query}';
        }}""")

        await page.waitForSelector('input[id="uss-submit-button"]', timeout=60000),
        await page.click('input[id="uss-submit-button"]')

        await page.waitForSelector("input[value = 'Adobe Photoshop']", timeout=60000),
        await page.click("input[value = 'Adobe Photoshop']")

        # Wait for the search results to load.
        time.sleep(3)
        url = await page.evaluate("() => window.location.href")

        """ for country in (("US", "FR"), ("CA", "FR"), ("UK", "FR")):
            url = url.replace(*country) """
        
        # Find no results found text, if applicable.
        bad = await page.querySelector('.EmptyState-suggestions')
        if bad is not None:

            embed=discord.Embed(
                title = f"Your search for \"{str(query)}\" returned the following:",
                url = url,
                color=0x349feb
            )
                
            embed.add_field(
                name=f"**🚫 OH NOES!** We were unable to find any matching results. ", 
                value=f'• Ensure all search words are spelled correctly.\n• Try using quotes to search for an entire phrase, such as "crop an image".',
                inline=False
            )
            
            embed.set_thumbnail(url="https://i.postimg.cc/prG85X5G/Adobe2.jpg")
            
            await ctx.send(embed=embed)
        
        # If results were able to be found...
        else:

            titles = await page.querySelectorAll('.ResultsListItem-title--clamped')
            results = await page.querySelectorAll('.ResultsListItem-content-excerpt-text')
            links = await page.xpath("//a [@class='spectrum-Link']")

            titlesText = []
            resultsText = []
            linksText = []

            for count, t in enumerate(titles):
                content = await page.evaluate('(element) => element.textContent', t)
                titlesText.append(content)

                content = await page.evaluate('(element) => element.textContent', results[count])
                resultsText.append(content)

                content = await page.evaluate('(links) => links.href', links[count])
                linksText.append(content)
            
            contentMessage = ""
            resultNum = 0

            for count in range(len(titlesText)):
                print(count)
                
                length = len(contentMessage) + len(titlesText[count]) + len(resultsText[count]) + len(linksText[count]) 
                print(length)

                if length < 1001:
                    print("This will do!")
                    resultNum = resultNum + 1                
                    contentMessage = contentMessage + f"\n[__{titlesText[count]}__]({linksText[count]})\n{resultsText[count]}"
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
                inline=False
            )
            
            embed.set_thumbnail(url="https://i.postimg.cc/mrB2Trx9/Adobe1.jpg")
            await ctx.send(embed=embed)

            print("All done!")
            
            await page.close()
            await browser.close()

    # asyncio.get_event_loop().run_until_complete(fetch())


def setup(bot):
    bot.add_cog(Fetch(bot))
    
    
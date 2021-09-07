import asyncio
import aiohttp
from urllib.parse import urlparse, parse_qs
import sqlite3
import scrapy
from scrapy.http import Request, Response

parsed = urlparse("""https://helpx.adobe.com/search.html?q=masks&start_index=0&country=CA&activeScopes=%5B%22helpx
%3Ahelp%22%5D&scopeConfigs=%5B%7B%22value%22%3A%22helpx%3Ahelp%22%2C%22renderStyle%22%3A%22vert%22%2C%22seeMoreLink
%22%3Anull%2C%22isSelectable%22%3Atrue%7D%2C%7B%22value%22%3A%22helpx%3Acommunities%22%2C%22renderStyle%22%3A
%22vert%22%2C%22seeMoreLink%22%3Anull%2C%22isSelectable%22%3Atrue%7D%2C%7B%22value%22%3A%22helpx%3Alearn%22%2C
%22renderStyle%22%3A%22horiz%22%2C%22seeMoreLink%22%3Anull%2C%22isSelectable%22%3Atrue%7D%2C%7B%22value%22%3A
%22adobe_com%3Aproduct%22%2C%22renderStyle%22%3A%22vert%22%2C%22seeMoreLink%22%3Anull%2C%22isSelectable%22%3Atrue
%7D%5D&filters=%7B%22products%22%3A%5B%22Adobe+Photoshop%22%5D%7D&banners=%7B%22aboveResults%22%3A%7B%22count%22
%3A1%2C%22ids%22%3A%5B%22auto%22%5D%7D%2C%22sidebar%22%3A%7B%22count%22%3A0%2C%22ids%22%3A%5B%5D%7D%7D&ctrls=%7B
%22prodFilts%22%3Atrue%7D""")
#
parsed_dict = parse_qs(parsed.query)
print(parsed_dict)


# [\"helpx:help\",\"helpx:communities\",\"helpx:learn\",\"adobe_com:product\"]
async def main():
    params = {
        "q": "layer masks",
        "start_index": "0",
        "country": "UK",
        "activeScopes": "[\"helpx:help\"]",
        "scopeConfigs":
            "[{\"value\":\"helpx:help\",\"renderStyle\":\"vert\",\"seeMoreLink\":null,\"isSelectable\":true},"
            "{\"value\":\"helpx:communities\",\"renderStyle\":\"vert\",\"seeMoreLink\":null,\"isSelectable\":true},"
            "{\"value\":\"helpx:learn\",\"renderStyle\":\"horiz\",\"seeMoreLink\":null,\"isSelectable\":true},"
            "{\"value\":\"adobe_com:product\",\"renderStyle\":\"vert\",\"seeMoreLink\":null,\"isSelectable\":true}]",
        "filters": "{\"products\":[\"Adobe Photoshop\"]}",
        "banners": "{\"aboveResults\":{\"count\":1,\"ids\":[\"auto\"]},\"sidebar\":{\"count\":0,\"ids\":[]}}",
        "ctrls": "{\"prodFilts\":true}"
        }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://helpx.adobe.com/search.html',
                               params=params) as r:
            print(r.url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#
# link = f'https://helpx.adobe.com/search.html?{urlencode(pretty)}'
#
# print(link)

# conn = sqlite3.connect('guild.db')
# c = conn.cursor()


# c.execute("""CREATE TABLE event_votes (
#             user_id INTEGER DEFAULT 0,
#             season_number INTEGER DEFAULT 0,
#             total_votes INTEGER DEFAULT 0,
#             UNIQUE(user_id)
#             )""")

# c.execute("""INSERT INTO config VALUES(
#             'season_number',
#             2
#             )""")

# FOR INSERTS
# c.execute("""UPDATE badges_master
#             SET position = position+1
#             WHERE id >= 8""")
#
# c.execute("""INSERT INTO badges_master VALUES(
#             '8',
#             'Season finalist!',
#             'Be a season finalist.',
#             'https://media.discordapp.net/attachments/822229241511936090/864592892147138600/Season_Finalist.png
#             ?width=654&height=676',
#             '8'
#             )""")

# FOR REMOVALS
# c.execute("""UPDATE badges_master
#             SET position = position+1
#             WHERE id >= 8""")
#
# c.execute("""INSERT INTO badges_master VALUES(
#             '8',
#             'Season finalist!',
#             'Be a season finalist.',
#             'https://media.discordapp.net/attachments/822229241511936090/864592892147138600/Season_Finalist.png
#             ?width=654&height=676',
#             '8'
#             )""")

# rows = c.execute("""SELECT *
#                     FROM badges_master
#                     ORDER BY position ASC""").fetchall()

# c.execute("""INSERT INTO Destination SELECT * FROM Source""")
# print(rows)

# c.execute("""ALTER TABLE badges_users_stats ADD wants_notifications INTEGER""")

# conn.commit()
#
# conn.close()

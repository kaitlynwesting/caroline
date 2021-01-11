import requests, json, time
from bs4 import BeautifulSoup
import requests

tips = []
count = input("Current number: (Number to be displayed)")
tip = int(input("Tip number: "))
URL = 'https://www.creativebloq.com/photo-editing/photoshop-tips-and-fixes-612316/' + str(4)
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')
headings = soup.find_all('h2')
headings.pop(0); headings.pop(-1)

for heading in headings:
    paragraph = heading.next_element.next_element
    if paragraph.name == "p":
      tips.append(paragraph.getText())

data = {}

data["embeds"] = []
embed = {}
embed["description"] = tips[tip]
embed["title"] = "Tip of the day: #" + str(count)
data["embeds"].append(embed)

data["content"] = "<@&787092173283131402>"
data["allowed_mentions"] = {
            "parse": ["roles"],
}


result = requests.post("https://discord.com/api/webhooks/788515489344782346/OYQD9ULu6l5XTGk0A5sKnj_f0Qr6pfZCHGxFtY9QOu-1lYdjgOAm-enfl-z0t3jQCrFn", data=json.dumps(data), headers={"Content-Type": "application/json"})
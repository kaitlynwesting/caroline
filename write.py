from bs4 import BeautifulSoup
import requests

URL = 'https://www.creativebloq.com/photo-editing/photoshop-tips-and-fixes-612316/' + str(pageNumber)
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')
headings = soup.find_all('h2')
headings.pop(0); headings.pop(-1)

for heading in headings:
    paragraph = heading.next_element.next_element
    if paragraph.name == "p":
      print(paragraph.getText())
      print("=======")
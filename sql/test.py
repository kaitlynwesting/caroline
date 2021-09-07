import requests

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36',
    'x-api-key': 'helpxcomprod',
    'content-type': 'application/vnd.adobe.search-request+json',
    'Accept': '*/*',
    'Origin': 'https://helpx.adobe.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://helpx.adobe.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    }

data = '{' \
   '"scope":["helpx"],' \
   '"subscope":[],' \
   '"serp_content_type":["help"],' \
   '"q":"masks",' \
   '"limit":10,' \
   '"locale":"en_us",' \
   '"start_index":0,' \
   '"sort_orderby":"relevancy",' \
   '"sort_order":"desc",' \
   '"facets_fields":["applicable_products"],' \
   '"post_facet_filters":{"applicable_products":["Adobe Photoshop"]},' \
   '"enable_spelling_correction":true,' \
   '"request_region":"CA"' \
   '}'

response = requests.post('https://adobesearch-uss-enterprise.adobe.io/universal-search-enterprise/search',
                         headers=headers,
                         data=data)
dumped = response.json()

# List of all the relevant result items
results = dumped["result_sets"][0]['items']

for count, item in enumerate(results):
    if count == 5:
        break

    print(item['excerpt'])

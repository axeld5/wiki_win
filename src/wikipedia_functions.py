import requests
import re

def get_random_page(random_count:int) -> list[str]:
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=0&rnlimit={random_count}"
    response = requests.get(url)
    data = response.json()
    titles = [data['query']['random'][i]['title'] for i in range(random_count)]
    return titles

def get_page_content(title:str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={title}&rvslots=*&rvprop=content&formatversion=2"
    response = requests.get(url)
    data = response.json()
    document = data['query']['pages'][0]['revisions'][0]['slots']['main']['content']
    pattern = r'\[\[(.*?)\]\]'
    matches = re.findall(pattern, document)
    extracted_texts = [match.split('|')[0] for match in matches]
    clickable_links = list(set(extracted_texts))
    return clickable_links

print(get_page_content('United States'))
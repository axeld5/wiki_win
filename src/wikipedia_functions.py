import requests
import re

def get_random_page(random_count:int) -> list[str]:
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=0&rnlimit={random_count}"
    response = requests.get(url)
    data = response.json()
    titles = [data['query']['random'][i]['title'] for i in range(random_count)]
    return titles

def remove_special_links(links:list[str]) -> list[str]:
    return [link for link in links if not link.startswith("Category:")]

def get_page_links(title:str) -> str:
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={title}&rvslots=*&rvprop=content&formatversion=2"
    response = requests.get(url)
    data = response.json()
    document = data['query']['pages'][0]['revisions'][0]['slots']['main']['content']
    pattern = r'\[\[(.*?)\]\]'
    matches = re.findall(pattern, document)
    extracted_links = [match.split('|')[0] for match in matches]
    uniform_links = list(set(extracted_links))
    clickable_links = remove_special_links(uniform_links)
    return clickable_links


def check_wikipedia_pages_existence(titles):
    url = "https://en.wikipedia.org/w/api.php"
    results = {}
    slice_size = 50
    sublists = []
    for i in range(0, len(titles), slice_size):
        sublist = titles[i:i+slice_size]
        sublists.append(sublist)
    for title_list in sublists:
        params = {
            "action": "query",
            "format": "json",
            "titles": "|".join(title_list),
            "prop": "info",
            "inprop": "url"
        }
        response = requests.get(url, params=params)
        data = response.json()
        page_info = data["query"]["pages"]
        for key in page_info:
            if int(key) < 0:
                studied_title = page_info[key]['title']
                results[studied_title] = False
            else:
                studied_title = page_info[key]['title']
                results[studied_title] = True
        for title in title_list:
            if title not in results:
                results[title] = False
    return results

def get_page_content(title:str):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={title}&explaintext=1"
    response = requests.get(url)
    data = response.json()
    page_id = list(data['query']['pages'].keys())[0]
    page_content = data['query']['pages'][page_id]['extract']
    return page_content


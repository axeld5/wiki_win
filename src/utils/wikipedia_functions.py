"""Gets functions related to wikipedia API"""
import re
import requests

def get_random_page(random_count:int) -> list[str]:
    """
    Gets a random amount of title pages from Wikipedia.
    
    Args:
        random_count (int): count of random pages that need to be fetched
    
    Returns:
        titles (list[str]): titles of pages to be fetched
    """
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnnamespace=0&rnlimit={random_count}"
    response = requests.get(url)
    data = response.json()
    titles = [data['query']['random'][i]['title'] for i in range(random_count)]
    return titles

def remove_special_links(links:list[str]) -> list[str]:
    """
    Performs removal of identified special, unusable links.

    Args:
        links (list[str]): list of links

    Returns:
        list[str]: filtered list of links
    """
    return [link for link in links if not link.startswith("Category:") and not link.startswith("File:")]

def get_page_links(title:str) -> list[str]:
    """
    From page title, queries wikipedia API to get a list of unique links found on the page.

    Args:
        title (str): title of the studied page

    Returns:
        clickable_links (list[str]): list of clickable links found from the page
    """
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

def check_wikipedia_pages_existence(titles:list[str]) -> dict[str, bool]:
    """
    Uses wikipedia API to check if there if the wikipedia pages assigned to a list of titles are empty or not.

    Args:
        titles (list[str]): list of titles that provide followable links
    
    Returns:
        results (dict[str, bool]): dict that assigns to each title a bool saying if the wikipedia page is missing or not.
    """
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


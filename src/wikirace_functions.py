import os
import yaml
from sentence_transformers import SentenceTransformer
from langchain_anthropic import ChatAnthropic
from wikipedia_functions import get_page_links, get_page_content, check_wikipedia_pages_existence
from chain_functions import get_crawler_chain, get_summarize_chain, get_explain_links_chain, get_broad_links_chain
from answer_functions import answer_broad_links, answer_crawler, answer_explain_links, answer_summarize
from matching_functions import find_closest_documents

def load_anthropic_key():
    """Loads anthropic key and adds it within the environment"""
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    anthropic_key = config["anthropic_key"]
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key

def get_valid_links(current_page:str, trajectory:list[str]):
    """
    Gets links from a page which are valid given a page title and a trajectory.
    Trajectory is here to avoid repetition of links, as per wiki game rules.
    
    Args:
        current_page (str): Page the agentic system is currently at
        trajectory (list[str]): List of explored pages
        
    Returns:
        valid_links (list[str]): List of valid links to be checked
    """
    start_links = get_page_links(current_page)
    checked_links = check_wikipedia_pages_existence(start_links)
    valid_links = [link for link in start_links if checked_links[link] and link not in trajectory]
    return valid_links

def full_wikirace(start_page:str, end_page:str, n_iterations:int=10) -> None:
    """
    Performs wikipedia race game given a start_page and an end_page.

    The wikipedia race game process solving goes as follows:
    1- Setup models & chains
    2- Summarize the end page's content to give information to the agents
    3- Initiate page, trajectory and links
    4- Perform the agentic process for each iteration

    Args:
        start_page (str): Title of starting page
        end_page (str): Title of end page
        n_iterations (int): Amount of iterations allowed to solve the challenge. Set to 10.
    
    Returns:
        None
    """
    #Setup models & chains
    load_anthropic_key()
    embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    haiku = ChatAnthropic(temperature=0, model_name="claude-3-haiku-20240307")
    crawler_chain = get_crawler_chain(haiku)
    summarize_chain = get_summarize_chain(haiku)
    explain_links_chain = get_explain_links_chain(haiku)
    broad_links_chain = get_broad_links_chain(haiku)

    #Summarization of end page content
    end_page_full_content = get_page_content(end_page)
    end_page_content = answer_summarize(summarize_chain, end_page_full_content)

    #Initiate page, trajectory and links
    current_page = start_page
    trajectory = []
    current_links = get_valid_links(current_page, trajectory)

    #Loop iteration
    for i in range(n_iterations):
        trajectory.append(current_page)
        if end_page in current_links:
            print(f"{end_page} in {current_page}'s links \nPage reached in {i+1} iterations!")
            break
        else:
            closest_links = find_closest_documents(embedding_model, current_links, end_page, end_page_content)
            broad_links = answer_broad_links(broad_links_chain, current_links, end_page, end_page_content)
            current_links = list(set([link for link in closest_links + broad_links if link in current_links]))
            reasonings = answer_explain_links(explain_links_chain, current_links, end_page, end_page_content)
            current_page = answer_crawler(crawler_chain, current_page, current_links, reasonings, end_page, end_page_content).strip()
            current_links = get_valid_links(current_page, trajectory)
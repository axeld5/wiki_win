"""Functions related to getting the chain's answers and postprocessing them."""

import re

def answer_summarize(summarize_chain, end_page_full_content:str) -> str:
    """
    Gets the answer from the summarizing agent and postprocesses it.
    
    Args:
        summarize_chain: summarize chain obtained from chain_functions
        end_page_full_content (str): full content of the wikipedia page to reach
        
    Returns:
        end_page_content (str): summarized content of the wikipedia page to reach
    """
    end_summary = summarize_chain.invoke(
        {
            "end_page_full_content": end_page_full_content
        }
    )
    model_output = end_summary.content
    pattern = r'<summary>(.*?)</summary>'
    matches = re.findall(pattern, model_output)
    end_page_content = matches[0]
    return end_page_content

def answer_broad_links(broad_links_chain, current_links:list[str], end_page:str, end_page_content:str) -> list[str]:
    """
    Gets the answer from the agent tasked to identify broad links and postprocesses it.
    
    Args:
        broad_links_chain: broad_links chain obtained from chain_functions
        current_links (list[str]): list of links available to pick from
        end_page (str): name of the page to reach
        end_page_content (str): summarized content of the wikipedia page to reach
        
    Returns:
        broad_links (list[str]): links identified by the agent
    """
    broad_links = broad_links_chain.invoke({
        "current_links": current_links,
        "end_page": end_page,
        "end_page_content": end_page_content
    })
    model_output = broad_links.content
    pattern = r'<output>(.*?)</output>'
    matches = re.findall(pattern, model_output)
    broad_links = [link.strip() for link in matches[0].split(",")]
    return broad_links

def answer_explain_links(explain_links_chain, current_links:list[str], end_page:str, end_page_content:str) -> str:
    """
    Gets the answer from the agent tasked to explain chosen links and postprocesses it.
    
    Args:
        explain_links_chain: explain_links chain obtained from chain_functions
        current_links (list[str]): list of links chosen to pick from
        end_page (str): name of the page to reach
        end_page_content (str): summarized content of the wikipedia page to reach
        
    Returns:
        reasonings (str): reasonings for each link on why they would be interesting to be picked
    """
    explain_links = explain_links_chain.invoke({
        "current_links": current_links,
        "end_page": end_page,
        "end_page_content": end_page_content
    })
    reasonings = explain_links.content
    return reasonings

def answer_crawler(crawler_chain, current_page:str, current_links:list[str], reasonings:str, end_page:str, end_page_content:str):
    """
    Gets the answer from the crawler agent on which link would be the best to choose and postprocesses it.
    
    Args:
        crawler_chain: crawler chain obtained from chain_functions
        current_page (str): page to choose from
        current_links (list[str]): list of links chosen to pick from
        reasonings (str): reasonings for each of the chosen links
        end_page (str): name of the page to reach
        end_page_content (str): summarized content of the wikipedia page to reach
        
    Returns:
        new_page (str): chosen page to go to
    """
    crawler_text = crawler_chain.invoke(
        {
            "current_page": current_page,
            "current_links": current_links,
            "reasonings": reasonings,
            "end_page": end_page,
            "end_page_content": end_page_content
        }
    )
    model_output = crawler_text.content
    print(model_output)
    pattern = r'<output>(.*?)</output>'
    matches = re.findall(pattern, model_output)
    new_page = matches[0]
    return new_page
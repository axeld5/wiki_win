"""Functions related to the wikirace solving process"""
from typing import Optional, List
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_anthropic import ChatAnthropic

from agents.answer_functions import answer_broad_links, answer_crawler, answer_explain_links, answer_summarize
from agents.chain_functions import get_crawler_chain, get_summarize_chain, get_explain_links_chain, get_broad_links_chain
from utils.matching_functions import find_closest_documents
from utils.wikipedia_functions import get_page_links, get_page_content, check_wikipedia_pages_existence

def get_valid_links(current_page:str, trajectory:List[str]) -> List[str]:
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

def full_wikirace(start_page:str, end_page:str, n_iterations:int=10, model_used:str="haiku", on_streamlit:bool=False, st_text:Optional[classmethod]=None) -> None:
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
        on_streamlit (bool): If function is used for streamlit, adds streamlit functions to make prints
    
    Returns:
        None
    """
    #Setup models & chains
    if on_streamlit:
        with st_text:
            st.markdown("Setting up...")
    load_dotenv()
    embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    if model_used == "haiku":
        llm = ChatAnthropic(temperature=0, model_name="claude-3-haiku-20240307")
    elif model_used == "sonnet":
        llm = ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
    elif model_used == "opus":
        llm = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")
    crawler_chain = get_crawler_chain(llm)
    summarize_chain = get_summarize_chain(llm)
    explain_links_chain = get_explain_links_chain(llm)
    broad_links_chain = get_broad_links_chain(llm)

    #Summarization of end page content
    if on_streamlit:
        with st_text:
            st.markdown("Summarizing End Page Content...")
    end_page_full_content = get_page_content(end_page)
    end_page_content = answer_summarize(summarize_chain, end_page_full_content)
    if on_streamlit:
        with st_text:
            st.markdown(f"Summary of end page content: {end_page_content}")

    #Initiate page, trajectory and links
    current_page = start_page
    trajectory = []
    current_links = get_valid_links(current_page, trajectory)
    if on_streamlit:
        with st_text:
            st.markdown("Initializing search...")

    #Loop iteration
    for i in range(n_iterations):
        trajectory.append(current_page)
        if on_streamlit:
            with st_text:
                st.markdown(f"Search iteration: {i+1}")
                st.markdown(f"Current Page: {current_page}")
                st.markdown(f"Current Trajectory: {' > '.join(trajectory)}")
        if end_page in current_links:
            if on_streamlit:
                with st_text:
                    st.markdown("---------FOUND!----------")
                    st.markdown(f"{end_page} in {current_page}'s links!")
                    st.markdown(f"Page reached in {i+1} iterations")
            else:
                print(f"{end_page} in {current_page}'s links \nPage reached in {i+1} iterations!")
            break
        elif i == n_iterations - 1:
            if on_streamlit:
                with st_text:
                    st.markdown("---------NOT FOUND----------")
                    st.markdown(f"'{end_page}' page could not be reached in {i+1} iterations")
            else:
                print(f"'{end_page}' page could not be reached in {i+1} iterations")
        else:
            closest_links = find_closest_documents(embedding_model, current_links, end_page, end_page_content)
            broad_links = answer_broad_links(broad_links_chain, current_links, end_page, end_page_content)
            current_links = list(set([link for link in closest_links + broad_links if link in current_links]))
            reasonings = answer_explain_links(explain_links_chain, current_links, end_page, end_page_content)
            current_page, crawler_reasoning = answer_crawler(crawler_chain, current_page, current_links, reasonings, end_page, end_page_content)
            if on_streamlit:
                with st_text:
                    st.markdown(f"Crawler Reasoning: \n{crawler_reasoning}")
            current_links = get_valid_links(current_page, trajectory)
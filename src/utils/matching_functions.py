"""Functions related to matching links with the end document"""

import numpy as np
from sentence_transformers import SentenceTransformer

def find_closest_documents(model: SentenceTransformer, current_links:list[str], end_page:str, end_page_content:str, n_returned:int=5) -> list[str]:
    """
    Uses open source embedding model to evaluate closest links to wikipedia target page.
    
    Args:
        model (SentenceTransformer): embedding model
        current_links (list[str]): list of links to pick from
        end_page (str): name of the page to reach
        end_page_content (str): summarized content of the wikipedia page to reach
        n_returned (int): amount of integers to return
        
    Returns:
        closest_links (list[str]): selection of links closest semantically to the objective page
    """
    wikipedia_pages = [f"search_query: From what wikipedia page is the wikipedia page for '{link.lower()}' close to?" for link in current_links]
    doc = [f"search_document: {end_page.lower()} & \n Page summary: {end_page_content}"]
    doc_embedding = model.encode(doc)
    link_embeddings = model.encode(wikipedia_pages)
    closest_embedding_idxs = find_closest_embeddings(doc_embedding, link_embeddings, n_returned)
    closest_links = [current_links[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs]
    return closest_links

def find_closest_embeddings(doc_embedding:np.ndarray, link_embeddings:np.ndarray, n_returned:int) -> np.ndarray:
    """
    From an embedding of a document and of query links, find the n closest embeddings.

    Args:
        doc_embedding (np.ndarray): embedding of the end page with its summarized content
        link_embeddings (np.ndarray): embeddings of the links we want to find whether or not they're interesting to click on
        n_returned (int): number of indices we return

    Returns:
        chosen_indices (np.ndarray): 1D array of integers of length (n_returned) containing indices of links closest to the document
    """
    embedding_differences = np.asarray([np.linalg.norm(doc_embedding - link_embedding) for link_embedding in link_embeddings])
    chosen_indices = np.argsort(embedding_differences)[:n_returned]
    return chosen_indices

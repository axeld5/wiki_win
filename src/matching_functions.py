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
    closest_embedding_idxs = np.argsort(np.asarray([np.linalg.norm(doc_embedding - link_embedding) for link_embedding in link_embeddings]))
    closest_links = [current_links[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs[:n_returned]]
    return closest_links

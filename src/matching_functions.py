import numpy as np
from sentence_transformers import SentenceTransformer

def find_closest_documents(model: SentenceTransformer, goal_page:str, links:list[str], n_returned:int=5) -> list[str]:
    query = [f"search_query: {goal_page}"]
    wikipedia_pages = [f"search_document: {link}" for link in links]
    query_embedding = model.encode(query)
    link_embeddings = model.encode(wikipedia_pages)
    closest_embedding_idxs = np.argsort(np.asarray([np.linalg.norm(query_embedding - document_embedding) for document_embedding in link_embeddings]))
    closest_links = [links[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs[:n_returned]]
    return closest_links

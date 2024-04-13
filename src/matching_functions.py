import numpy as np
from sentence_transformers import SentenceTransformer

def find_closest_documents(model: SentenceTransformer, end_page:str, current_links:list[str], n_returned:int=5) -> list[str]:
    query = [f"search_query: {end_page}"]
    wikipedia_pages = [f"search_document: {link}" for link in current_links]
    query_embedding = model.encode(query)
    link_embeddings = model.encode(wikipedia_pages)
    closest_embedding_idxs = np.argsort(np.asarray([np.linalg.norm(query_embedding - document_embedding) for document_embedding in link_embeddings]))
    closest_links = [current_links[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs[:n_returned]]
    return closest_links

import numpy as np
from sentence_transformers import SentenceTransformer

def find_closest_documents(model: SentenceTransformer, current_links:list[str], end_page:str, end_page_content:str, n_returned:int=5) -> list[str]:
    wikipedia_pages = [f"search_query: {link}" for link in current_links]
    doc = [f"search_document: {end_page}" + "\n" + f"{end_page_content}"]
    doc_embedding = model.encode(doc)
    link_embeddings = model.encode(wikipedia_pages)
    closest_embedding_idxs = np.argsort(np.asarray([np.linalg.norm(doc_embedding - document_embedding) for document_embedding in link_embeddings]))
    closest_links = [current_links[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs[:n_returned]]
    return closest_links

query = ["search_query: United States"]
wikipedia_pages = ["search_document: Porsche",
             "search_document: Switzerland",
             "search_document: Wild Cats",
             "search_document: High School Musical",
             "search_document: Barack Obama",
             "search_document: Imagine Dragons",
             "search_document: United States"]
query_embedding = model.encode(query)
wikip_embeddings = model.encode(wikipedia_pages)

closest_embedding_idxs = np.argsort(np.asarray([np.linalg.norm(query_embedding - document_embedding) for document_embedding in wikip_embeddings]))
closest_embedding = [wikipedia_pages[closest_embedding_idx] for closest_embedding_idx in closest_embedding_idxs[:3]]
print(closest_embedding)
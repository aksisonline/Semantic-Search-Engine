from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import os

# Environment variables
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('API_KEY')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def search_qdrant(query):
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    encoder = SentenceTransformer(os.getenv('EMBEDDINGS_MODEL_MULTI'))
    query_vector = encoder.encode(query).tolist()
    
    search_request = models.SearchRequest(
        vector=query_vector,
        top=5  # Number of results to retrieve
    )
    
    response = client.search(collection_name=COLLECTION_NAME, search_request=search_request)
    results = response.records
    for result in results:
        print(result.payload['title'])  # Assuming 'title' is a key in your metadata
        
# Example usage
if __name__ == '__main__':
    query = input("Enter your search query: ")
    search_qdrant(query)

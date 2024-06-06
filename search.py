from qdrant_client import QdrantClient
from dotenv import dotenv_values
import time

class NeuralSearcher:

    def __init__(self, collection_name: str):
        # Load the environment variables from .env file
        env_vars = dotenv_values()

        # Get the api_key and qdrant_url from the environment variables
        api_key = env_vars.get('API_KEY')
        qdrant_url = env_vars.get('QDRANT_URL')

        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=qdrant_url, api_key=api_key, prefer_grpc=True)

    def search_vector(self, query_vector, top_k):
        start_time = time.time()
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        print(f"Search took {time.time() - start_time} seconds")
        return [hit.metadata for hit in hits]

    def search_query(self, query, top_k):
        start_time = time.time()
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=query,
            limit=top_k
        )
        print(f"Search took {time.time() - start_time} seconds")
        return [hit.metadata for hit in hits]
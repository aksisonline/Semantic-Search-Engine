from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from qdrant_client.models import Filter
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
api_key = os.getenv('API_KEY')

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url, api_key=api_key)
        # Initialize Hugging Face summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    def parse_query_with_huggingface(self, query):
        response = self.summarizer(query, max_length=50, min_length=1, do_sample=False)
        print(response)
        parsed_text = response[0]['summary_text']
        return parsed_text
    
    def search(self, text: str, top_k: int = 5):
        # Parse the query using Hugging Face
        parsed_query = self.parse_query_with_huggingface(text)
        
        # Convert the query to a vector representation
        vector = self.model.encode(parsed_query).tolist()
        
        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k,  # Get top_k results directly
            with_payload=True
        )
        
        # Sort results by the scores
        sorted_results = sorted(search_result, key=lambda x: x.score, reverse=True)
        
        # Return the top_k results
        return [result.payload for result in sorted_results[:top_k]]
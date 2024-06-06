import os
from dotenv import load_dotenv
import pandas as pd
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer, util

# Load environment variables from .env file
load_dotenv()

def ingest_csv_data(qdrant_url, api_key, collection_name):
    # Load CSV data into a DataFrame
    csv_path = os.getenv('CSV_FILE_PATH')
    df = pd.read_csv(csv_path)
    df = df.head(200)

    # Initialize QdrantClient with your cloud URL and API key
    client = QdrantClient(url=qdrant_url, api_key=api_key)

    # Load pre-trained Sentence Transformer model
    model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
    

    # Check if the collection already exists
    if not client.collection_exists(collection_name):
        # Create a new collection in Qdrant
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )

    # Index items into Qdrant
    vectors = []
    for index, row in df.iterrows():
        text = row['overview']  # Use the 'overview' column as the text data
        if isinstance(text, str):  # Ensure 'overview' is a non-empty string
            vector = model.encode(text)  # Calculate the vector representation
            vectors.append(vector)

    # Upload vectors to Qdrant
    client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload=dict(row[1])  # Unpack the tuple to get the row (row[1]) as a dictionary
        )
        for idx, vector, row in zip(range(len(vectors)), vectors, df.iterrows())
    ]
)
def semantic_search(query, qdrant_url, api_key, collection_name, top_k=5):
    # Initialize QdrantClient with your cloud URL and API key
    client = QdrantClient(host=qdrant_url, api_key=api_key)

    # Load pre-trained Sentence Transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Search for similar items in the specified collection
    search_results = client.search(collection_name, query_embedding.cpu().numpy(), top_k=top_k)

    return search_results

# Example usage
qdrant_url = os.getenv('QDRANT_URL')
api_key = os.getenv('API_KEY')
collection_name = 'IMDB_movies'

# DATA INGESTED
# ingest_csv_data(qdrant_url, api_key, collection_name)

# Perform semantic search
query = "a scifi old movie with aliens and spaceships"
results = semantic_search(query, qdrant_url, api_key, collection_name)
for result in results:
    print(result)

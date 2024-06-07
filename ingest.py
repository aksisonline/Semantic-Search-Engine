import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
api_key = os.getenv('API_KEY')

# Initialize SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Read the CSV file using pandas
data = pd.read_csv("IMDB.csv")
data = data.head(200)

# Define function to preprocess and combine relevant text fields dynamically
def preprocess_row(row):
    text_columns = [col for col in row.index if isinstance(row[col], str)]
    combined_text = ' '.join(row[text_columns].values)
    return combined_text

# Apply preprocessing to combine text fields into a single string for all rows
data['combined_text'] = data.apply(preprocess_row, axis=1)

# Encode combined text fields into vectors
data['vector'] = data['combined_text'].apply(lambda x: model.encode(x).tolist())

# Initialize Qdrant client
qdrant_client = QdrantClient(url=qdrant_url, api_key=api_key)

# Define Qdrant collection name
collection_name = "IMDB_movies_200"

# Create Qdrant collection if it doesn't exist
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
)

# Prepare data for uploading to Qdrant
points = []
for idx, row in data.iterrows():
    points.append(
        models.PointStruct(
            id=idx,
            vector=row['vector'],
            payload=row.drop(['combined_text', 'vector']).to_dict()
        )
    )

# Upload data to Qdrant
qdrant_client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Successfully ingested {len(points)} records into the Qdrant collection '{collection_name}'.")

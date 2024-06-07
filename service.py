from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
api_key = os.getenv('API_KEY')

# The file where NeuralSearcher is stored
from neural_searcher import NeuralSearcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
# Create a neural searcher instance
neural_searcher = NeuralSearcher(collection_name='IMDB_movies_200')


@app.get("/api/search")
def search_startup(q: str):
    return {"result": neural_searcher.search(text=q)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
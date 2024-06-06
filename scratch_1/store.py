import os
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

COLLECTION_NAME = os.getenv('COLLECTION_NAME')
COLLECTION_NAME_MULTI = os.getenv('COLLECTION_NAME_MULTI')
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('API_KEY')
EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL')
EMBEDDINGS_MODEL_MULTI = os.getenv('EMBEDDINGS_MODEL_MULTI')
CSV_FILE_PATH = "IMDB.csv"

def get_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.dropna(subset=['overview'])
    documents = df['overview'].tolist()
    metadata = df.to_dict('records')
    return documents, metadata


def upload_vectors(client: QdrantClient, encoder: SentenceTransformer, metadata):
    client.upload_records(
        collection_name=COLLECTION_NAME_MULTI,
        records=[
            models.Record(
                id=idx, vector=encoder.encode(doc['overview']).tolist(), payload=doc
            )
            for idx, doc in enumerate(tqdm(metadata))
        ],
    )


def add_docs(client: QdrantClient, documents, metadata):
    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadata,
        ids=tqdm(range(len(documents))),
        # usage of parallel leads to fork safety issue in OSX, therefore None
        parallel=None,
    )


def create_document_fastembed(client: QdrantClient):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )


def create_document_multi_lang(client: QdrantClient, encoder: SentenceTransformer):
    client.recreate_collection(
        collection_name=COLLECTION_NAME_MULTI,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
            on_disk=True
        ),
        # Quantize to 8-bit
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )


def init_multi_embed(client: QdrantClient, metadata):
    encoder = SentenceTransformer(EMBEDDINGS_MODEL_MULTI)
    create_document_multi_lang(client, encoder)
    upload_vectors(client, encoder, metadata)


def init_fastembed(client: QdrantClient, documents, metadata):
    client.set_model(EMBEDDINGS_MODEL)
    create_document_fastembed(client)
    add_docs(client, documents, metadata)


def populate_qdrant():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    documents, metadata = get_data(CSV_FILE_PATH)
    init_multi_embed(client, metadata)
    # init_fastembed(client, documents, metadata)


if __name__ == '__main__':
    populate_qdrant()
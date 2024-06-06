from sklearn.feature_extraction.text import TfidfVectorizer
import json

def vectorize_json_data(json_data):
    # Load the JSON data
    data = json.loads(json_data)

    # Extract the text data
    text_data = [item['overview'] for item in data]

    # Create a TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the text data and transform the text data into vectors
    vectors = vectorizer.fit_transform(text_data)

    return vectors.toarray()

# Example usage
# json_data = ingest_csv_data('IMDB.csv')
# vectors = vectorize_json_data(json_data)
# print(vectors)
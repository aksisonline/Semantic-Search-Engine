import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import csv
import csv
import json

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


def clean_data(text):
    # Remove HTML tags
    clean_text = re.sub('<.*?>', '', text)

    # Remove punctuation
    clean_text = clean_text.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    clean_text = clean_text.lower()

    # Tokenization
    tokens = word_tokenize(clean_text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return stemmed_tokens, lemmatized_tokens

# Example usage
# text = "<html><body><h1>Hello, World!</h1></body></html>"
# stemmed_tokens, lemmatized_tokens = clean_data(text)
# print("Stemmed Tokens:", stemmed_tokens)
# print("Lemmatized Tokens:", lemmatized_tokens)

def ingest_csv_data(file_path, num_rows=10):
    data = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        keys = next(reader)  # Get the first row as keys
        for i, row in enumerate(reader):
            if num_rows != 0 and i >= num_rows:
                break
            data.append(dict(zip(keys, row)))  # Create a dictionary with keys and row values
    return json.dumps(data)

# Example usage
csv_file_path = 'IMDB.csv'
json_data = ingest_csv_data(csv_file_path)
print(json_data)
from raw_text_ingest import *
from search import NeuralSearcher
from store import *
from vectorize import *
import streamlit as st

def main():
    # Create an instance of NeuralSearcher
    searcher = NeuralSearcher(collection_name="your_collection_name")

    # Streamlit search interface
    st.title("Semantic Search Engine")
    query = st.text_input("Enter your search query:")

    if st.button("Search"):
        # Perform search using your search_query function
        results = searcher.search_query(query=query, top_k=10)

        # Display search results
        for result in results:
            st.write(result)

if __name__ == "__main__":
    main()
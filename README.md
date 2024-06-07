# Neural Movie Searcher

This project is a movie search application that uses a neural network to provide search results. It consists of a Python backend that handles the neural search and a React frontend for the user interface.

## Project Structure

The project is divided into two main parts:

1. The Python backend located in the root directory and the [`scratch_1`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FSemantic-Search-Engine%2Fscratch_1%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Club Files\Projects\Semantic-Search-Engine\scratch_1") directory. The backend handles the neural search functionality. It uses the `NeuralSearcher` class from [`scratch_1/search.py`](scratch_1/search.py) and the [`create_document_fastembed`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FSemantic-Search-Engine%2Fscratch_1%2Fstore.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A45%2C%22character%22%3A4%7D%5D "scratch_1/store.py") and [`create_document_multi_lang`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FSemantic-Search-Engine%2Fscratch_1%2Fstore.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A59%2C%22character%22%3A4%7D%5D "scratch_1/store.py") functions from [`scratch_1/store.py`](scratch_1/store.py) to create and search through the document embeddings.
2. The React frontend located in the [`movie-search-ui`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FSemantic-Search-Engine%2Fmovie-search-ui%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Club Files\Projects\Semantic-Search-Engine\movie-search-ui") directory. The frontend provides a user interface for the movie search. It uses the `handleSearch` and `searchMovies` functions from [`movie-search-ui/src/App.js`](movie-search-ui/src/App.js) to handle user input and search for movies.

## Setup

### Backend

To set up the Python backend, you need to install the required Python packages. You can do this by running the following command in your terminal:

```sh
pip install -r requirements.txt
```

Then, you can start the backend by running the `service.py` script:

```sh
python service.py
```

### Frontend

To set up the React frontend, navigate to the [`movie-search-ui`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FSemantic-Search-Engine%2Fmovie-search-ui%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Club Files\Projects\Semantic-Search-Engine\movie-search-ui") directory and install the required Node.js packages:

```sh
cd movie-search-ui
npm install
```

You can then start the frontend by running the following command:

```sh
npm start
```

This will start the frontend in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Usage

To use the application, simply type your search query into the search bar in the frontend. The application will then use the neural network to search for relevant movies and display the results.

## Contributing

Contributions are welcome. Please submit a pull request if you have something to add or fix.

## License

This project is licensed under the MIT License.

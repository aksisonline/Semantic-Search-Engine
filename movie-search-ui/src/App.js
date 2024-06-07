import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchMovies = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/search?q=${query}`);
      setResponse(response.data.result);
      console.log(response.data.result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setLoading(false);
  };

  const handleSearch = () => {
    if (query.trim() !== '') {
      searchMovies();
    }
  };

  return (
    <div>
      <h1>Movie Search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for movies..."
      />
      <button onClick={handleSearch}>Search</button>
      <div>
        {loading ? (
          <p>Loading...</p>
        ) : response.length > 0 ? (
          <ul>
            {response.map((movie) => (
              <li key={movie.id}>
                <h2>{movie.title} ({movie.release_date})</h2>
                <p>{movie.overview}</p>
                <p>Genres: {movie.genres}</p>
                <p>Director: {movie.director}</p>
                <p>Cast: {movie.cast}</p>
                <p>Rating: {movie.vote_average}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No movies found.</p>
        )}
      </div>
    </div>
  );
};




export default App;

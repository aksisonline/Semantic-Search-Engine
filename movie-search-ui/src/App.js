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
    <div className="container mx-auto">
      <h1 className="text-4xl font-bold mb-4">Movie Search</h1>
      <div className="flex items-center mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for movies..."
          className="border border-gray-300 rounded py-2 px-4 mr-2"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Search
        </button>
      </div>
      <div>
        {loading ? (
          <p>Loading...</p>
        ) : response.length > 0 ? (
          <ul>
            {response.map((movie) => (
              <li key={movie.id} className="mb-4 rounded-xl bg-white shadow p-9">
                <h2 className="text-2xl font-bold pb-5">
                  {movie.title} ({movie.release_date})
                </h2>
                <p className='pb-3'>{movie.overview}</p>
                <p><b>Genres:</b> {movie.genres}</p>
                <p><b>Director:</b> {movie.director}</p>
                <p><b>Cast:</b> {movie.cast}</p>
                <p><b>Rating:</b> {movie.vote_average}</p>
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

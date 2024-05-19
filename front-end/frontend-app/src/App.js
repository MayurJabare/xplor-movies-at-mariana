import React, { useState, useEffect } from 'react';
import MoviesByDate from './MoviesByDate';  // Import the MoviesByDate component

function App() {
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchInput, setSearchInput] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [allGenres, setAllGenres] = useState([]);
  const [view, setView] = useState('main');  // State to manage the view
  const [selectedDate, setSelectedDate] = useState('');  // State to store the selected date

  useEffect(() => {
    fetchMovies();
    fetchAllGenres();
  }, []);

  const fetchMovies = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/home/');
      const data = await response.json();
      console.log('Response from API:', data);
      setMovies(data.movies);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  };

  const fetchAllGenres = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/home/');
      const data = await response.json();
      setAllGenres(data.all_genres);
    } catch (error) {
      console.error('Error fetching genres:', error);
    }
  };

  const filterMovies = () => {
    let filteredMovies = movies.filter(movie => movie.title.toLowerCase().includes(searchInput.toLowerCase()));

    if (selectedGenre) {
      filteredMovies = filteredMovies.filter(movie => movie.genres.includes(selectedGenre));
    }

    return filteredMovies;
  };

  const handleVoteClick = (date) => {
    setSelectedDate(date);
    setView('moviesByDate');
  };

  return (
    <div>
      <h1>Movie Search</h1>
      {view === 'main' ? (
        <div>
          <input
            type="text"
            placeholder="Search for movies..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            style={{
              marginBottom: '10px',
              padding: '8px',
              fontSize: '16px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              width: '100%',
              maxWidth: '300px',
              boxSizing: 'border-box',
            }}
          />
          <select
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
            style={{
              marginBottom: '10px',
              padding: '8px',
              fontSize: '16px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              width: '100%',
              maxWidth: '300px',
              boxSizing: 'border-box',
            }}
          >
            <option value="">All Genres</option>
            {allGenres.map(genre => (
              <option key={genre} value={genre}>{genre}</option>
            ))}
          </select>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <table style={{ borderCollapse: 'collapse', width: '100%' }}>
              <thead>
                <tr>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Date</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Title</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Poster</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Movie Genres</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>IMDB Rating</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Meta Score</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Released Year</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Movie Run Time</th>
                  <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Vote</th>
                </tr>
              </thead>
              <tbody>
                {filterMovies().map((movie, index) => (
                  <tr key={index}>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.date}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.title}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                      <img src={movie.poster} alt={`Poster of ${movie.title}`} style={{ maxWidth: '80px', maxHeight: '100px' }} />
                    </td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                      <ul>
                        {movie.genres.map((genre, index) => (
                          <li key={index}>{genre}</li>
                        ))}
                      </ul>
                    </td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.imdb_rating}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.meta_score}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.year}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.runtime}</td>
                    <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                      <button
                        className="edit-button"
                        data-id={movie.id}
                        data-date={movie.date}
                        onClick={() => handleVoteClick(movie.date)}
                      >
                        Vote For Movie
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ) : (
        <MoviesByDate date={selectedDate} />
      )}
    </div>
  );
}

export default App;

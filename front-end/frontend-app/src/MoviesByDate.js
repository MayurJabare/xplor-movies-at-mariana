import React, { useState, useEffect } from 'react';

function MoviesByDate({ date }) {
  const [movies, setMovies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchMoviesByDate(date);
  }, [date]);

  const fetchMoviesByDate = async (date) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/movies_by_date/${date}/`);
      const data = await response.json();
      setMovies(data.movies);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching movies by date:', error);
    }
  };

  const handleVote = async (movieId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/vote/?movie_id=${movieId}`);
      // Handle response as needed
      console.log('Vote success:', response);
      window.location.reload(); // Reload the page after voting
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  return (
    <div>
      <h1>Movies for {date}</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Title</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Metacritic Score</th>
              <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {movies.map((movie, index) => (
              <tr key={index}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.title}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{movie.meta_score}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                  <button className="vote-button" onClick={() => handleVote(movie.id)}>Vote</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default MoviesByDate;

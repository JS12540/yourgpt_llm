import React, { useState } from 'react';

function QueryForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send the user query to the ML model (server-side)
    try {
      const response = await fetch('/api/your-ml-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>ML Model Interaction</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={handleQueryChange}
        />
        <button type="submit">Submit</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default QueryForm;

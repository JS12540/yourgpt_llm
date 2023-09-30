import React, { useState } from 'react';

function QueryForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create a FormData object to send both text data and files
    const formData = new FormData();
    formData.append('query', query);
    formData.append('file', selectedFile);

    // Send the user query and file to the server-side endpoint
    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload_files', {
        method: 'POST',
        body: formData,
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
      <h1>ML Model Interaction with File Upload</h1>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={handleQueryChange}
        />
        <input
          type="file"
          accept=".pdf,.txt,.docx" // Specify the allowed file types
          onChange={handleFileChange}
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
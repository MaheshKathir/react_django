import React, { useState } from 'react';
// import axios from 'axios';
import connection from "../config/connection";

function TextForm() {
  const [inputText, setInputText] = useState('');
  const [processedData, setProcessedData] = useState('');

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    connection.post('/api/process_text/', { text: inputText })
      .then(response => {
        setProcessedData(response.data.processed_text);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Ask a Question?</label><br/>
        <input type="text" value={inputText} onChange={handleInputChange} />
        <button type="submit">Generate Response</button>
      </form><br/>
      <textarea value={processedData} rows="4" cols="40"></textarea>
      
    </div>
  );
}

export default TextForm;

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobType, setJobType] = useState('internship');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState([]);

  const handleJobTypeChange = (e) => {
    setJobType(e.target.value);
  };

  const handleKeywordsChange = (e) => {
    setKeywords(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      console.log('Sending request to backend...');
      const response = await axios.post('http://127.0.0.1:5000/scrape', {
        job_type: jobType,
        keywords: keywords,
      });
      console.log('Response received:', response.data);
      setResults(response.data);
    } catch (error) {
      console.error('Error fetching data', error);
    }
  };

  return (
    <div className="App">
      <h1>LinkedIn Job Scraper</h1>
      <div>
        <label>
          <input type="radio" value="internship" checked={jobType === 'internship'} onChange={handleJobTypeChange} />
          Internship
        </label>
        <label>
          <input type="radio" value="entry-level" checked={jobType === 'entry-level'} onChange={handleJobTypeChange} />
          Entry Level
        </label>
        <label>
          <input type="radio" value="associate" checked={jobType === 'associate'} onChange={handleJobTypeChange} />
          Associate
        </label>
      </div>
      <div>
        <input type="text" placeholder="Enter job keywords" value={keywords} onChange={handleKeywordsChange} />
      </div>
      <button onClick={handleSubmit}>Search</button>
      <div>
        {results.length > 0 && (
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                <a href={result[1]} target="_blank" rel="noopener noreferrer">
                  {result[0]}
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;

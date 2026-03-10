import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [entries, setEntries] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
    : `${window.location.protocol}//${window.location.hostname}:8000/api/leaderboard/`;

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const items = data.results || data;
        setEntries(items);
        console.log('Leaderboard endpoint:', endpoint);
        console.log('Fetched leaderboard:', items);
      });
  }, [endpoint]);

  return (
    <div>
      <h2>Leaderboard</h2>
      <ul>
        {entries.map((entry, idx) => (
          <li key={entry._id || idx}>{entry.user} - {entry.points} pts</li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;

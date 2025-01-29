import React, { useState } from "react";

function App() {
  const send_data = {
    interpolation_points: ["1"],
    first_derivatives_points: ["0", "1/2", "1"],
    second_derivatives_points: ["0", "1/2", "1"],
    analysis: true,
  };
  const [data, setData] = useState(send_data); // Initial data to send
  const [response, setResponse] = useState(null); // Response from the API
  const [error, setError] = useState(null);

  const sendDataToApi = async () => {
    console.log("clicked");
    try {
      const apiUrl = "https://grant-89eg.onrender.com/api/v1/generate"; // Replace with your API URL
      console.log("clicked 2");
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setResponse(result);
    } catch (err) {
      setError(err.message);
    }
    console.log("done");
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Send Data to API</h1>

      <div>
        <h3>Data to send:</h3>
        <pre>{JSON.stringify(data, null, 2)}</pre>
        <button
          onClick={() => {
            sendDataToApi();
          }}
          style={{ marginTop: "10px" }}
        >
          Send to API
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>API Response:</h3>
        {response ? (
          <pre>{JSON.stringify(response, null, 2)}</pre>
        ) : error ? (
          <p style={{ color: "red" }}>Error: {error}</p>
        ) : (
          <p>No response yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;

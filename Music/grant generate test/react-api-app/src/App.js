import React, { useState, useEffect } from "react";
import { MathJax, MathJaxContext } from "better-react-mathjax";

const FractionInputApp = () => {
  const [groupData, setGroupData] = useState([
    { name: "Interpolation", numFractions: 0, fractions: [] },
    { name: "First Derivative Collocation", numFractions: 0, fractions: [] },
    { name: "Second Derivative Collocation", numFractions: 0, fractions: [] },
  ]);

  const [responseMessage, setResponseMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingDots, setLoadingDots] = useState("");
  const [status, setStatus] = useState("idle"); // 'idle', 'loading', 'done', 'error'

  // Update loading dots (e.g., ".", "..", "...", then repeat)
  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setLoadingDots((prevDots) =>
          prevDots.length < 3 ? prevDots + "." : ""
        );
      }, 500); // Update every 500ms
      return () => clearInterval(interval); // Clear interval on component unmount or when loading stops
    }
  }, [loading]);

  const handleGroupChange = (groupIndex, field, value) => {
    const updatedGroups = [...groupData];
    if (field === "numFractions") {
      updatedGroups[groupIndex].numFractions = value;
      updatedGroups[groupIndex].fractions = Array.from(
        { length: value },
        () => ({ numerator: "", denominator: "" })
      );
    } else {
      const [fractionIndex, fractionField] = field;
      updatedGroups[groupIndex].fractions[fractionIndex][fractionField] = value;
    }
    setGroupData(updatedGroups);
  };

  const handleSubmit = async () => {
    const formattedGroups = groupData.map((group) => ({
      name: group.name,
      fractions: group.fractions.map(
        (fraction) => `${fraction.numerator}/${fraction.denominator}`
      ),
    }));

    const data = {
      interpolation_points: formattedGroups[0].fractions,
      first_derivatives_points: formattedGroups[1].fractions,
      second_derivatives_points: formattedGroups[2].fractions,
      analysis: true,
    };

    try {
      setLoading(true); // Start loading
      setStatus("loading"); // Set status to loading
      setResponseMessage(null); // Clear previous response

      const apiUrl = "https://grant-89eg.onrender.com/api/v1/generate/"; // Replace with your API URL
      // const apiUrl = "http://127.0.0.1:8000/api/v1/generate/"; // Replace with your API URL

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        const result = await response.json();
        if (result.status === "error") {
          setStatus("error"); // Set status to error
          alert(result.message);
        } else {
          setResponseMessage(result.results);
          setStatus("done"); // Set status to done
        }
      }
    } catch (err) {
      console.error(err);
      setStatus("error"); // Set status to error
    } finally {
      setLoading(false); // Stop loading
    }
  };

  // Determine the color based on the status
  const getStatusColor = () => {
    switch (status) {
      case "loading":
        return "red"; // Red for loading
      case "done":
        return "green"; // Green for done
      case "error":
        return "red"; // Red for error
      default:
        return "black"; // Default color
    }
  };

  return (
    <MathJaxContext>
      <div>
        <h1>Numerical Method Generator App</h1>
        {groupData.map((group, groupIndex) => (
          <div key={groupIndex}>
            <h2>{group.name}</h2>
            <div>
              <label>How many fractions?</label>
              <input
                type="number"
                min="0"
                value={group.numFractions}
                onChange={(e) =>
                  handleGroupChange(
                    groupIndex,
                    "numFractions",
                    Number(e.target.value)
                  )
                }
                placeholder="Enter number of fractions"
              />
            </div>
            {group.fractions.map((fraction, fractionIndex) => (
              <div key={fractionIndex}>
                <input
                  type="number"
                  placeholder={`Numerator ${fractionIndex + 1}`}
                  value={fraction.numerator}
                  onChange={(e) =>
                    handleGroupChange(
                      groupIndex,
                      [fractionIndex, "numerator"],
                      e.target.value
                    )
                  }
                />
                <span>/</span>
                <input
                  type="number"
                  placeholder={`Denominator ${fractionIndex + 1}`}
                  value={fraction.denominator}
                  onChange={(e) =>
                    handleGroupChange(
                      groupIndex,
                      [fractionIndex, "denominator"],
                      e.target.value
                    )
                  }
                />
              </div>
            ))}
          </div>
        ))}
        <button onClick={handleSubmit}>Submit All Fractions</button>

        {loading && (
          <div style={{ color: getStatusColor() }}>Loading{loadingDots}</div>
        )}

        {status === "done" && !loading && (
          <div style={{ color: getStatusColor() }}>Done!</div>
        )}

        {status === "error" && !loading && (
          <div style={{ color: getStatusColor() }}>Error occurred!</div>
        )}

        {responseMessage && (
          <div>
            <h3>Response:</h3>
            {responseMessage.map((equation, index) => (
              <MathJax key={index}>
                <div>{`\\(${equation}\\)`}</div>
              </MathJax>
            ))}
          </div>
        )}
      </div>
    </MathJaxContext>
  );
};

export default FractionInputApp;

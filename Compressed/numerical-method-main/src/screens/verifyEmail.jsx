import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import LoadingSpinner from "../components/spinner";

function VerifyEmail() {
  const [loading, setloading] = useState(false);
  const location = useLocation();

  // Extract token from URL query params
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get("token");

    if (token) {
      verifyEmail(token);
    } else {
      console.error("No token provided in URL");
    }
  }, [location.search]);

  const verifyEmail = async (token) => {
    try {
      setloading(true);

      const response = await axios.patch("/verify-email", null, {
        params: { token },
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      console.log(response);
    } catch (error) {
      if (error.response) {
        if (error.response.status === 422) {
          console.error("Validation error:", error.response.data);
        } else {
          console.error("Error verifying email:", error.response.data);
        }
      } else {
        console.error("Error verifying email:", error);
      }
    } finally {
      setloading(false);
    }
  };

  return <div>{loading && <LoadingSpinner />}</div>;
}

export default VerifyEmail;

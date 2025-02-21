import { Link, useNavigate } from "react-router-dom";
import React, { useState } from "react";
import LoadingSpinner from "../components/spinner";
import "react-toastify/dist/ReactToastify.css";
import { post } from "../utils/api";

function Login() {
  const [loading, setloading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState("");
  const navigate = useNavigate();

  const login = () => {
    setloading(true);
    const data = {
      password: password,
      email: email,
    };

    post(
      "/users/login",
      data,
      {},
      (response) => {
        console.log(response.access_token);
        setloading(false);
        sessionStorage.setItem("token", response.access_token);
        navigate("/GenerateMethod");
      },
      (error) => {
        console.log("Error", error);
        alert(error.detail);
        setloading(false);
      }
    );
  };

  return (
    <div className="flex flex-col items-center justify-center h-[100vh] textFont">
      <div className="relative flex flex-col items-center">
        <h1
          className={`${
            window.innerWidth < 1780
              ? "text-[6vw] md:text-[2vw]"
              : "text-[40px]"
          } font-semibold`}
        >
          Welcome
        </h1>
        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[4vw] md:text-[1.5vw]"
              : "text-[30px]"
          }`}
        >
          Please Log In To Continue
        </p>
        <input
          onChange={(e) => setEmail(e.target.value)}
          type="text"
          placeholder="Email"
          className={`${
            window.innerWidth < 1780
              ? "text-[3.5vw] md:text-[2vw] lg:text-[1.5vw] w-[85vw] md:w-[40vw]"
              : "w-[1000px] text-[40px]"
          } input bg-transparent rounded-[10px] text-black p-[8px] mt-[24px] mb-[8px] border border-[#00cc00]`}
        />
        <input
          onChange={(e) => setPassword(e.target.value)}
          // type="password"
          placeholder="Password"
          className={`${
            window.innerWidth < 1780
              ? "text-[3.5vw] md:text-[2vw] lg:text-[1.5vw] w-[85vw] md:w-[40vw]"
              : "w-[1000px] text-[40px]"
          } input bg-transparent rounded-[10px] text-black p-[8px] my-[8px] border border-[#00cc00]`}
        />

        <Link
          to="/ForgotPassword"
          className={`${
            window.innerWidth < 1780
              ? "text-[3vw] md:text-[1.5vw] lg:text-[1.2vw]"
              : "text-[30px]"
          }`}
        >
          Forgot Password?
        </Link>

        <button
          onClick={login}
          className={`${
            window.innerWidth < 1780 ? "w-[40vw] md:w-[13vw]" : "w-[200px]"
          } bg-[#013a19] text-white  mt-[32px] rounded-[20px] py-[4px] flex flex-col items-center justify-center`}
        >
          {loading ? <LoadingSpinner /> : "Log In"}
        </button>
        {errors && <p className="text-red-500">{errors}</p>}

        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[3vw] md:text-[1.5vw] lg:text-[1.2vw]"
              : "text-[30px]"
          } mt-[16px]`}
        >
          Don't have an account?{" "}
          <Link to="/SignUp" className="text-blue-500">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Login;

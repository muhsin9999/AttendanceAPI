import React, { useState } from "react";
import LoadingSpinner from "../components/spinner";
import "react-toastify/dist/ReactToastify.css";
import { post } from "../utils/api";


function ForgotPassword() {
  const [loading, setloading] = useState(false);
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState("");

  const forgotPassword = () => {
    setloading(true);
    const data = {
      email: email,
    };

    post(
      "/users/login/forget_password",
      data,
      {},
      (response) => {
        console.log(response);
        alert(response.message);
        setloading(false);
      },
      (error) => {
        console.log("Error", error);
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
          Forgot Password?
        </h1>
        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[4vw] md:text-[1.5vw]"
              : "text-[30px]"
          }`}
        >
          Please enter your email to reset password
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

        <button
          onClick={forgotPassword}
          className={`${
            window.innerWidth < 1780 ? "w-[33vw] md:w-[13vw]" : "w-[200px]"
          } bg-[#013a19] text-white  mt-[32px] rounded-[20px] py-[8px] flex flex-col items-center justify-center`}
        >
          {loading ? <LoadingSpinner /> : "Reset Password"}
        </button>
        {errors && <p className="text-red-500">{errors}</p>}
      </div>
    </div>
  );
}

export default ForgotPassword;

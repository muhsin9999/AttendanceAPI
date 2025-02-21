import { Link } from "react-router-dom";
import React, { useState } from "react";
import LoadingSpinner from "../components/spinner";
import Input from "../components/input";
// import { nigerianUniversities } from "../json/nigerianUniversities";
import { post } from "../utils/api";

function SignUp() {
  const [loading, setloading] = useState(false);
  const [universityError, setuniversityError] = useState("");
  const [email, setEmail] = useState("");
  const [emailError, setemailError] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setpasswordError] = useState("");
  const [firstName, setfirstName] = useState("");
  const [firstNameError, setfirstNameError] = useState("");
  const [selectedUniversity, setSelectedUniversity] = useState("");

  const handleUniversityChange = (e) => {
    setSelectedUniversity(e.target.value);
  };

  const signUp = () => {
    setloading(true);
    const data = {
      username: firstName,
      password: password,
      email: email,
      institution: selectedUniversity,
    };

    post(
      "/users/signup",
      data,
      {},
      (response) => {
        console.log(response);
        setloading(false);
        // navigation.navigate("Login");
      },
      (error) => {
        console.log("Error", error);
        setloading(false);
      }
    );
  };

  return (
    <div
      className={`${
        window.innerWidth < 1780 ? "w-[100vw]" : "w-[1780px]"
      } textFont flex flex-col items-center justify-center min-h-[100vh]`}
    >
      <div className="relative flex flex-col items-center mt-[32px]">
        <h1
          className={`${
            window.innerWidth < 1780
              ? "text-[6vw] md:text-[2vw]"
              : "text-[50px]"
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
          Lets get you started, input your details below.
        </p>

        <Input
          onChangeText={(e) => setfirstName(e.target.value)}
          type="text"
          error={firstNameError}
          placeholder="Username"
        />

        <Input
          onChangeText={(e) => setEmail(e.target.value)}
          type="text"
          error={emailError}
          placeholder="Email"
        />

        <Input
          onChangeText={(e) => setPassword(e.target.value)}
          type="text"
          error={passwordError}
          placeholder="Password"
        />

        <select
          value={selectedUniversity}
          onChange={handleUniversityChange}
          className={`${
            window.innerWidth < 1780
              ? "text-[3.5vw] md:text-[2vw] lg:text-[1.5vw] w-[85vw] md:w-[40vw]"
              : "w-[1000px] text-[40px]"
          } input bg-transparent rounded-[10px] text-black px-[8px] py-[12px] mt-[16px] border border-[#00cc00]`}
        >
          <option value="">Select Institution</option>
          {/* {nigerianUniversities.map((university) => (
            <option key={university} value={university}>
              {university}
            </option>
          ))} */}
        </select>

        {universityError && (
          <p
            className={`${
              window.innerWidth < 1780
                ? "text-[3vw] md:text-[2vw] lg:text-[1.5vw]"
                : "text-[30px]"
            } text-red-500  mb-[16px]`}
          >
            {universityError}
          </p>
        )}

        <button
          onClick={signUp}
          className={`${
            window.innerWidth < 1780 ? "w-[40vw] md:w-[13vw]" : "w-[200px]"
          } bg-[#013a19] items-center text-white mt-[16px] rounded-[20px] py-[4px] flex flex-col justify-center`}
        >
          {loading ? <LoadingSpinner /> : "Sign Up"}
        </button>

        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[3vw] md:text-[1.5vw] lg:text-[1.2vw]"
              : "text-[30px]"
          }  mt-[8px]`}
        >
          Already have an account?{" "}
          <Link to="/Login" className="text-blue-500">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}

export default SignUp;

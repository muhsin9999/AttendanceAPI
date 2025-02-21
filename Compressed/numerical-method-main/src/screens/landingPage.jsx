import { Link } from "react-router-dom";
import React from "react";
import "react-toastify/dist/ReactToastify.css";

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-between pt-[80px] h-[100vh] textFont">
      <div className="relative flex flex-col items-center">
        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[4vw] md:text-[1.5vw]"
              : "text-[30px]"
          } px-[16px] mt-[16px] lg:w-[1000px] text-center`}
        >
          Our web-based application is designed to automate the generation of
          Linear Multistep Methods (LMMs) for solving ordinary differential
          equations. By leveraging interpolation and collocation techniques, the
          tool simplifies the traditionally complex and time-consuming process
          of deriving LMMs. The tool supports fractional parameters and provides
          results in LaTeX format, which can be downloaded or rendered directly
          on the interface. Whether you’re a researcher, student, or
          practitioner, this platform enhances computational efficiency and
          accuracy. Experience the seamless integration of symbolic and
          numerical computation in a user-friendly environment. Start exploring
          now and transform the way you solve ODEs!
        </p>

        <Link
          to="/GenerateMethod"
          className={`${
            window.innerWidth < 1780 ? "w-[50vw] md:w-[13vw]" : "w-[200px]"
          } bg-[#013a19] mt-[16px] text-white rounded-[20px] py-[8px] flex flex-col items-center justify-center`}
        >
          Generate Method
        </Link>
      </div>
    </div>
  );
}

export default LandingPage;

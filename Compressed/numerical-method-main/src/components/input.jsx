import React from "react";

const Input = ({ onChangeText, placeholder, error, type, value }) => {
  return (
    <div>
      <div>
        <input
          placeholder={placeholder}
          onChange={onChangeText}
          value={value}
          type={type}
          className={`${
            window.innerWidth < 1780
              ? "text-[3.5vw] lg:text-[1.5vw] md:text-[2vw] w-[85vw] md:w-[40vw]"
              : "w-[1000px] text-[40px]"
          } input bg-transparent rounded-[10px] text-black px-[8px] py-[12px] mt-[16px] border border-[#00cc00] `}
        />
      </div>
      {error && (
        <p
          className={`${
            window.innerWidth < 1780
              ? "text-[3vw] md:text-[2vw] lg:text-[1.5vw]"
              : "text-[30px]"
          } text-red-500  mb-[16px] textFont`}
        >
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;

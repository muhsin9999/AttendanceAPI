import { Link } from "react-router-dom";

export default function Header() {
  return (
    <div
      className={`py-[0.5rem] px-[12px] shadow-md nav bg-[#013a19] rounded-b-[30px] text-center ${
        window.innerWidth > 1780 && "w-[1780px]"
      }`}
    >
      <h1
        className={`font-bold text-white ${
          window.innerWidth < 1780
            ? "text-[4.5vw] md:text-[2.5vw]"
            : "text-[40px]"
        }`}
      >
        LMM Generator: An Automated Tool for Deriving Linear Multistep Methods
      </h1>
    </div>
  );
}

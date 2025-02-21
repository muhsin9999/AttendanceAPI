import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <div
      className={`py-[2rem] px-[24px] shadow-md nav bg-[#013a19] rounded-t-[30px] text-center ${
        window.innerWidth > 1780 && "w-[1780px]"
      } `}
    >
      <Link
        onClick={() => {
          setnavigateTo("/");
        }}
        to="/"
        className={`font-bold text-white text-[14px] ${
          window.innerWidth < 1780
            ? "text-[3.5vw] md:text-[1.5vw]"
            : "text-[30px]"
        }`}
      >
        Powered by National Open University of Nigeria
      </Link>
    </div>
  );
}

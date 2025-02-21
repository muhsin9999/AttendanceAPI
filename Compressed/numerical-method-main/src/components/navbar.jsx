import { Link } from "react-router-dom";

export default function Navbar() {
  const token = sessionStorage.getItem("token");

  return (
    <div
      className={`flex flex-col md:items-center textFont ${
        window.innerWidth < 1780 ? "w-[100vw]" : "w-[1780px]"
      }`}
    >
      <div
        className={`flex justify-between p-[1rem] textFont shadow-md nav bg-white fixed items-center w-[100vw] pt-[3vh] ${
          window.innerWidth < 1780 ? "w-[100vw]" : "w-[1780px]"
        } `}
      >
        <Link
          onClick={() => {
            setnavigateTo("/");
          }}
          to="/"
          className="font-bold"
        >
          NMG
        </Link>

        <div className="lg:hidden relative">
          {!token && (
            <div className="flex flex-row">
              <Link
                to="/Login"
                className={`${
                  window.innerWidth < 1780
                    ? "w-[20vw] md:w-[13vw]"
                    : "w-[200px]"
                } bg-[#013a19] text-white rounded-[20px] py-[4px] flex flex-col items-center justify-center`}
              >
                Log In
              </Link>
            </div>
          )}
        </div>

        <div
          className={`hidden lg:flex flex-col items-end md:mr-[1rem] ${
            window.innerWidth < 1780 ? "w-[10vw]" : "w-[1000px]"
          }`}
        >
          {!token && (
            <div className="flex flex-row">
              <Link
                to="/Login"
                className={` bg-[#013a19] w-[100px] text-white rounded-[20px] py-[4px] flex flex-col items-center justify-center`}
              >
                Log In
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

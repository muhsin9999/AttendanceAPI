import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useState } from "react";
import "./App.css";
import { ScrollToTop } from "./components/scrollToTop";
import Login from "./screens/login";
import { ToastContainer } from "react-toastify";
import RequireAuth from "./components/requireAuth";
import ForgotPassword from "./screens/forgotPassword";
import ChangePassword from "./screens/changePassword";
import Navbar from "./components/navbar";
import LandingPage from "./screens/landingPage";
import SignUp from "./screens/signUpOne";
import GenerateMethod from "./screens/generateMethod";
import VerifyEmail from "./screens/verifyEmail";
import Footer from "./components/footer";

export const NavigateTo = React.createContext();

function App() {
  const [navigateTo, setnavigateTo] = useState("/");

  return (
    <div className="textFont max-w-[1780px] backgroundImage">
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        closeOnClick
        pauseOnHover
        draggable
        progress={undefined}
        theme="light"
      />
      <NavigateTo.Provider value={{ navigateTo, setnavigateTo }}>
        <Router>
            {/* <Navbar /> */}
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/Login" element={<Login />} />
              <Route path="/ForgotPassword" element={<ForgotPassword />} />
              <Route path="/ChangePassword" element={<ChangePassword />} />
              <Route path="/GenerateMethod" element={<GenerateMethod />} />
              <Route path="/SignUp" element={<SignUp />} />
              <Route path="/verify-email" element={<VerifyEmail />} />
              <Route element={<RequireAuth />}>
                <Route path="/GenerateMethod" element={<GenerateMethod />} />
                <Route path="*" element={<Navigate to="/Login" />} />
              </Route>
            </Routes>
        </Router>
      </NavigateTo.Provider>
    </div>
  );
}

export default App;

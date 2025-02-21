import { Navigate, Outlet } from "react-router-dom";

function RequireAuth() {
  const user = sessionStorage.getItem("token");
  console.log("Auth", user);
  return user ? <Outlet /> : <Navigate to="/Login" />;
}

export default RequireAuth;

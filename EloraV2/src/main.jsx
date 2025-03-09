import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import SignUp from "./components/SignUp";
import SignIn from "./components/SignIn";
import DoctorDashboard from "./pages/DoctorDashboard";
import './index.css'

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/signin" element={<SignIn />} />
      <Route path="/dashboard" element={<DoctorDashboard />} />
    </Routes>
  </BrowserRouter>
);

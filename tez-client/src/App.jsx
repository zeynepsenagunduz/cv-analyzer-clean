import { useState } from 'react'
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import DashboardUser from "./pages/DashboardUser";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<DashboardUser />} />
    </Routes>
  );
}
/*
function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='text-3xl font-bold underline text-center'>
        appp
    </div>
  )
}
  */

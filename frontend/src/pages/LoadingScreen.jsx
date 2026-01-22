// src/pages/LoadingScreen.jsx
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Lottie from "lottie-react";
import botAnimation from "../assets/AI CPU circuit board loading animation.json"; // tu JSON

const LoadingScreen = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/app"); // ⬅️ ahora redirige a /app
    }, 6500);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-100">
      <div className="flex flex-col items-center gap-4">
        <div className="w-56 h-56">
          <Lottie animationData={botAnimation} loop={true} />
        </div>
        <p className="text-sm md:text-base tracking-wide text-slate-300">
          Cargando...
        </p>
      </div>
    </div>
  );
};

export default LoadingScreen;

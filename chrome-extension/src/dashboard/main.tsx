import React from "react";
import ReactDOM from "react-dom/client";
import { Dashboard } from "../components/Dashboard";
import "../styles/globals.css";

const root = document.getElementById("root");
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <div className="min-h-screen bg-gray-50 flex items-start justify-center pt-8">
        <div className="w-[480px] bg-white rounded-2xl shadow-lg overflow-hidden">
          <Dashboard />
        </div>
      </div>
    </React.StrictMode>
  );
}

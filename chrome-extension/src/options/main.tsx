import React from "react";
import ReactDOM from "react-dom/client";
import { Settings } from "../components/Settings";
import "../styles/globals.css";

const root = document.getElementById("root");
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <div className="min-h-screen bg-gray-50 flex items-start justify-center pt-8">
        <div className="w-96 bg-white rounded-2xl shadow-lg overflow-hidden">
          <Settings />
        </div>
      </div>
    </React.StrictMode>
  );
}

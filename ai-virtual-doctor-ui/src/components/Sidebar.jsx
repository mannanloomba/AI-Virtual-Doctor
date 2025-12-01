import React from "react";
import "./Sidebar.css";

export default function Sidebar({ active, setActive }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="avatar">👩‍⚕️</div>
        <h2>MedGPT</h2>
        <small>AI Virtual Doctor</small>
      </div>

      <nav className="nav">
        <button className={active === "dashboard" ? "active" : ""} onClick={() => setActive("dashboard")}>Dashboard</button>
        <button className={active === "consult" ? "active" : ""} onClick={() => setActive("consult")}>Consult</button>
        <button className={active === "image" ? "active" : ""} onClick={() => setActive("image")}>Image Analysis</button>
        <button className={active === "history" ? "active" : ""} onClick={() => setActive("history")}>History</button>
      </nav>

      <div className="sidebar-foot">Built with Gemini • FastAPI</div>
    </aside>
  );
}

import React from "react";
import "./DoctorAssistant.css";

export default function DoctorAssistant({ text }) {
    return (
        <div className="doctor-card">
            <div className="doctor-anim">👨‍⚕️</div>
            <div className="doctor-text">
                <strong>AI Assistant</strong>
                <p>{text || "Hello — describe your symptoms or start a chat."}</p>
            </div>
        </div>
    );
}

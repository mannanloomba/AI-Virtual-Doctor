import React, { useEffect, useState } from "react";
import "./HistoryTimeline.css";

export default function HistoryTimeline({ userId }) {
    const [history, setHistory] = useState([]);
    useEffect(() => {
        const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
        fetch(`${apiUrl}/user/history?user_id=${userId}`)
            .then(r => r.json()).then(d => setHistory(d.history || []))
            .catch(() => setHistory([]));
    }, [userId]);

    return (
        <div className="glass-card">
            <h3>Patient Timeline</h3>
            <ul className="timeline">
                {history.length === 0 && <li>No history found.</li>}
                {history.map((h, idx) => {
                    // Handle various formats of history records
                    const timeStr = h.time ? new Date(h.time * 1000).toLocaleString() : new Date().toLocaleString();
                    const content = typeof h.record === 'string' ? h.record : JSON.stringify(h.record || h);
                    return (
                        <li key={idx}>
                            <div className="time">{timeStr}</div>
                            <div className="entry">{content}</div>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}

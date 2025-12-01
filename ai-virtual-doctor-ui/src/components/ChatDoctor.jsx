import React, { useState } from "react";
import "./ChatDoctor.css";

export default function ChatDoctor({ userId, onComplete }) {
    const [messages, setMessages] = useState([{ from: "bot", text: "Hello — I am your AI Medical Agent. How can I assist you today?" }]);
    const [val, setVal] = useState("");

    const send = async () => {
        if (!val.trim()) return;
        const userMsg = { from: "user", text: val };
        setMessages(m => [...m, userMsg]);

        // Call backend chat
        const form = new FormData();
        form.append("user_id", userId);
        form.append("message", val);
        // Convert current messages to Gemini history format
        const history = messages.map(m => ({ role: m.from === "bot" ? "model" : "user", parts: [m.text] }));
        form.append("history", JSON.stringify(history));

        try {
            const res = await fetch("http://127.0.0.1:8000/chat", { method: "POST", body: form });
            const data = await res.json();
            setMessages(m => [...m, { from: "bot", text: data.response }]);
        } catch (err) {
            setMessages(m => [...m, { from: "bot", text: "Failed to reach doctor." }]);
        }

        // if user signals done or long message -> run full assessment
        const done = /done|finish|assess|please assess|submit/i.test(val) || val.length > 200;
        if (done) {
            const formAssess = new FormData();
            formAssess.append("user_id", userId);
            formAssess.append("text", val);
            try {
                const res = await fetch("http://127.0.0.1:8000/full-assess", { method: "POST", body: formAssess });
                const data = await res.json();
                setMessages(m => [...m, { from: "bot", text: "Assessment finished. See results below." }]);
                onComplete && onComplete(data);
            } catch (err) {
                setMessages(m => [...m, { from: "bot", text: "Failed to reach backend." }]);
            }
        }
        setVal("");
    };

    return (
        <div className="chat-doctor glass-card">
            <div className="chat-window">
                {messages.map((m, i) => (
                    <div key={i} className={m.from === "bot" ? "bot-msg" : "user-msg"}>
                        <b>{m.from === "bot" ? "Doctor" : "You"}:</b> {m.text}
                    </div>
                ))}
            </div>

            <div className="chat-input">
                <input value={val} onChange={e => setVal(e.target.value)} placeholder="Type symptoms, or 'done' when finished." />
                <button onClick={send} className="action-btn">Send</button>
            </div>
        </div>
    );
}

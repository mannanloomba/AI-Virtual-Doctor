import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import DoctorAssistant from "./components/DoctorAssistant";
import ChatDoctor from "./components/ChatDoctor";
import HistoryTimeline from "./components/HistoryTimeline";
import ChatAssistantResponse from "./ChatAssistantResponse";
import "./index.css";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(BarElement, CategoryScale, LinearScale);

function App() {
    const [activeTab, setActiveTab] = useState("dashboard"); // dashboard, consult, image, history
    const [text, setText] = useState("");
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Image Analysis State
    const [selectedImage, setSelectedImage] = useState(null);
    const [imageAnalysis, setImageAnalysis] = useState(null);

    // History State
    const [history, setHistory] = useState([]);

    const userId = "mannan"; // Hardcoded for demo

    const handleSymptomSubmit = async () => {
        if (!text.trim()) return;
        setLoading(true);
        setResponse(null);
        setError(null);

        const formData = new FormData();
        formData.append("user_id", userId);
        formData.append("text", text);

        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
            const res = await fetch(`${apiUrl}/full-assess`, {
                method: "POST",
                body: formData,
            });
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            setResponse(data);
        } catch (err) {
            console.error(err);
            setError("Failed to connect to the Virtual Doctor.");
        } finally {
            setLoading(false);
        }
    };

    const handleImageUpload = async () => {
        if (!selectedImage) return;
        setLoading(true);
        setImageAnalysis(null);
        setError(null);

        const formData = new FormData();
        formData.append("user_id", userId);
        formData.append("file", selectedImage);

        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
            const res = await fetch(`${apiUrl}/upload-image`, {
                method: "POST",
                body: formData,
            });
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            setImageAnalysis(data);
        } catch (err) {
            console.error(err);
            setError("Failed to upload image.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (activeTab === "history") {
            fetchHistory();
        }
    }, [activeTab]);

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
            const res = await fetch(`${apiUrl}/user/history?user_id=${userId}`);
            if (!res.ok) throw new Error(`Server error: ${res.status}`);
            const data = await res.json();
            setHistory(data.history || []);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch history.");
        } finally {
            setLoading(false);
        }
    };

    const exportReport = async () => {
        // Export the result panel (.chat-bubble) as PDF
        const el = document.querySelector('.chat-bubble') || document.body;
        const canvas = await html2canvas(el);
        const img = canvas.toDataURL('image/png');
        const doc = new jsPDF({ unit: 'px', format: 'a4' });
        const width = doc.internal.pageSize.getWidth();
        const height = (canvas.height * width) / canvas.width;
        doc.addImage(img, 'PNG', 0, 0, width, height);
        doc.save(`medical_report_${Date.now()}.pdf`);
    };

    // small helpers for chart data
    const chartLabels = response?.diagnosis?.probable_diagnoses?.map(d => d.name) || [];
    const chartData = (response?.diagnosis?.probable_diagnoses || []).map(d => Math.round((d.score || 0) * 100));

    return (
        <div className="app-shell">
            <Sidebar active={activeTab} setActive={(t) => setActiveTab(t)} />

            <main className="main">
                <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div>
                        <h1 style={{ margin: 0, color: "#004d40" }}>AI Virtual Doctor</h1>
                        <small>Advanced Medical Assistance System • Multi-Agent • Gemini-enabled</small>
                    </div>
                    <div>
                        <button className="action-btn" onClick={() => { setText("Fever and headache for 2 days"); setActiveTab("consult"); }}>Demo: Flu</button>
                        <button className="action-btn" onClick={() => { setText("Red itchy rash on my forearm for 4 days"); setActiveTab("consult"); }}>Demo: Rash</button>
                    </div>
                </header>

                <DoctorAssistant text={response ? "I found probable diagnoses — scroll for details." : "Ready to assist. Try demo buttons or type symptoms."} />

                {/* Main panels */}
                {activeTab === "dashboard" && (
                    <>
                        <section className="top-cards" style={{ display: "flex", gap: 18 }}>
                            <div className="glass-card" style={{ flex: 1 }}>
                                <h3>Quick Assess</h3>
                                <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Describe your symptoms..." style={{ width: "100%", minHeight: 110 }} />
                                <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
                                    <button className="action-btn" onClick={handleSymptomSubmit} disabled={loading || !text.trim()}>{loading ? "Analyzing..." : "Get Assessment"}</button>
                                    <button className="action-btn" onClick={exportReport}>Export PDF</button>
                                </div>
                            </div>

                            <div className="glass-card chart-card" style={{ width: 520 }}>
                                <h4>Diagnosis Confidence</h4>
                                <Bar data={{
                                    labels: chartLabels.length ? chartLabels : ["No data"],
                                    datasets: [{
                                        label: 'Confidence %',
                                        data: chartData.length ? chartData : [0],
                                    }]
                                }} />
                            </div>
                        </section>
                        {response && <ChatAssistantResponse data={response} />}
                    </>
                )}

                {activeTab === "consult" && (
                    <div>
                        <ChatDoctor userId={userId} onComplete={(data) => setResponse(data)} />
                        {response && <ChatAssistantResponse data={response} />}
                        <div style={{ marginTop: 12 }}>
                            <h4>AI Mode</h4>
                            <small>Use the AI endpoints to compare rule-based vs LLM-based outputs (server must have AI endpoints enabled).</small>
                            <div style={{ marginTop: 8 }}>
                                <button className="action-btn" onClick={async () => {
                                    // call compare endpoint
                                    const form = new FormData(); form.append("user_id", userId); form.append("text", text || "");
                                    try {
                                        const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
                                        const res = await fetch(`${apiUrl}/compare`, { method: "POST", body: form });
                                        const d = await res.json(); console.log("Compare:", d); alert("Compare results logged to console.");
                                    } catch (e) { alert("Compare failed"); }
                                }}>Compare Rule vs AI</button>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === "image" && (
                    <div className="glass-card">
                        <h3>Upload Medical Image</h3>
                        <input type="file" accept="image/*" onChange={(e) => setSelectedImage(e.target.files[0])} />
                        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 10 }}>
                            <button className="action-btn" onClick={handleImageUpload} disabled={loading || !selectedImage}>{loading ? "Analyzing..." : "Analyze Image"}</button>
                        </div>

                        {imageAnalysis && (
                            <div style={{ marginTop: 12 }}>
                                <h4>Analysis Result</h4>
                                <p><strong>Finding:</strong> {imageAnalysis.analysis.possible_finding || "No specific findings detected."}</p>
                                <p><strong>Redness Score:</strong> {imageAnalysis.analysis.redness_score}</p>
                                <p><strong>Trend:</strong> {imageAnalysis.analysis.trend}</p>
                                <p><strong>Recommendation:</strong> {imageAnalysis.recommendation}</p>
                            </div>
                        )}
                    </div>
                )}

                {activeTab === "history" && (
                    <>
                        <HistoryTimeline userId={userId} />
                        <div style={{ marginTop: 12 }}>
                            <h4>Export Health Card</h4>
                            <button className="action-btn" onClick={async () => {
                                // quick shareable card export
                                const el = document.querySelector('.glass-card') || document.body;
                                const canvas = await html2canvas(el);
                                const img = canvas.toDataURL('image/png');
                                const doc = new jsPDF({ unit: 'px', format: 'a4' });
                                const width = doc.internal.pageSize.getWidth();
                                const height = (canvas.height * width) / canvas.width;
                                doc.addImage(img, 'PNG', 0, 0, width, height);
                                doc.save(`health_card_${Date.now()}.pdf`);
                            }}>Export Health Card</button>
                        </div>
                    </>
                )}

                {/* Global Error */}
                {error && <div className="error-banner">{error}</div>}
            </main>
        </div>
    );
}

export default App;

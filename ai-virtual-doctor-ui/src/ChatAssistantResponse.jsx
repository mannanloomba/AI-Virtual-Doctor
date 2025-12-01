import React, { useRef } from 'react';
import './ChatAssistantResponse.css';

const ChatAssistantResponse = ({ data }) => {
  const contentRef = useRef(null);

  if (!data) return null;

  // Extract data with correct mapping based on backend agents
  const symptoms = data.structured?.main_symptoms || []; // List of strings
  const severity = data.structured?.severity || 'Unknown';
  const duration = data.structured?.duration_days;

  const diagnoses = data.diagnosis?.probable_diagnoses || [];
  const treatmentPlan = data.treatment?.treatment_plan || [];

  // Prescription agent returns 'medications' (list of strings), not 'prescriptions'
  const prescriptions = data.prescription?.medications || [];

  // Triage agent returns dict { level, reasons, confidence }
  const triageData = data.triage || {};
  const triageLevel = triageData.level || 'Standard';

  const disclaimer = data.disclaimer || '';

  const handleCopy = () => {
    if (contentRef.current) {
      const text = contentRef.current.innerText;
      navigator.clipboard.writeText(text).then(() => {
        alert('Report copied to clipboard!');
      }).catch(err => {
        console.error('Failed to copy:', err);
      });
    }
  };

  // Helper to determine triage badge class
  const getTriageClass = (level) => {
    if (!level) return 'badge selfcare';
    const l = level.toString().toLowerCase();
    if (l.includes('emergency') || l.includes('urgent') || l.includes('critical')) return 'badge urgent';
    if (l.includes('moderate') || l.includes('consult')) return 'badge moderate';
    return 'badge selfcare';
  };

  return (
    <div className="chat-container">
      <div className="chat-bubble" ref={contentRef}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '2px solid #e0f2f1', paddingBottom: '10px' }}>
          <h2 style={{ margin: 0, color: '#00796b' }}>Medical Assessment</h2>
          <span className={getTriageClass(triageLevel)}>{triageLevel.toUpperCase()}</span>
        </div>

        {/* AI Reasoning Summary */}
        {data?.diagnosis && (
          <div className="section">
            <div className="section-title">🧠 AI Reasoning Summary</div>
            <p style={{ background: "#f8f9fa", padding: "12px", borderRadius: "8px", borderLeft: "4px solid #00796b" }}>
              This assessment combines rule-based matching with LLM reasoning. Key signals: duration = {data.structured?.duration_days || 'N/A'} days; severity = {data.structured?.severity || 'N/A'}.
            </p>
          </div>
        )}

        {/* Symptoms */}
        {symptoms.length > 0 && (
          <div className="section">
            <div className="section-title">📋 Symptoms Analyzed</div>
            <div style={{ marginBottom: '10px', fontStyle: 'italic', color: '#555' }}>
              Severity: <strong>{severity}</strong>
              {duration ? ` • Duration: ${duration} days` : ''}
            </div>
            <ul className="info-list">
              {symptoms.map((s, idx) => (
                <li key={idx}>
                  {/* s is a string in the backend response */}
                  <strong>{s}</strong>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Diagnosis */}
        {diagnoses.length > 0 && (
          <div className="section">
            <div className="section-title">🩺 Probable Diagnoses</div>
            <ul className="info-list">
              {diagnoses.map((d, idx) => (
                <li key={idx} style={{ borderLeftColor: '#00796b' }}>
                  <strong>{d.name || d.diagnosis}</strong>
                  {d.score && <span style={{ float: 'right', fontSize: '0.9em', color: '#666' }}>Match Score: {(d.score * 100).toFixed(0)}%</span>}
                  {d.score_reason && <div style={{ fontSize: '0.9em', marginTop: '4px', color: '#555' }}>{d.score_reason}</div>}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Treatment */}
        {treatmentPlan.length > 0 && (
          <div className="section">
            <div className="section-title">💊 Treatment Plan</div>
            {treatmentPlan.map((tp, idx) => (
              <div key={idx} style={{ marginBottom: '15px' }}>
                <h4 style={{ margin: '0 0 8px 0', color: '#004d40' }}>For: {tp.disease}</h4>
                <ul className="info-list">
                  {tp.plan?.first_line_medications?.length > 0 && (
                    <li><strong>Medications:</strong> {tp.plan.first_line_medications.join(', ')}</li>
                  )}
                  {tp.plan?.non_pharmacologic?.length > 0 && (
                    <li><strong>Advice:</strong> {tp.plan.non_pharmacologic.join(', ')}</li>
                  )}
                  {tp.plan?.follow_up_days && (
                    <li><strong>Follow-up:</strong> In {tp.plan.follow_up_days} days</li>
                  )}
                </ul>
              </div>
            ))}
          </div>
        )}

        {/* Prescriptions */}
        {prescriptions.length > 0 && (
          <div className="section">
            <div className="section-title">📝 Prescriptions</div>
            <ul className="info-list">
              {prescriptions.map((p, idx) => (
                <li key={idx}>
                  {/* p is a string in the backend response */}
                  <strong>{p}</strong>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Disclaimer */}
        {disclaimer && (
          <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#fff3e0', borderRadius: '8px', fontSize: '0.85em', color: '#e65100', border: '1px solid #ffe0b2' }}>
            <strong>DISCLAIMER:</strong> {disclaimer}
          </div>
        )}

        {data && (
          <div style={{ marginTop: 20, padding: 12, borderRadius: 8, background: '#fff8e1', border: '1px solid #ffe0b2' }}>
            <strong>📝 Doctor Summary:</strong> Patient reports {data.structured?.symptoms?.join(", ") || "symptoms"}. Triage: {data.triage?.level || 'standard'}. Please verify medication allergies and seek urgent care if symptoms worsen.
          </div>
        )}
      </div>

      <button className="copy-button" onClick={handleCopy}>
        Copy Report
      </button>
    </div>
  );
};

export default ChatAssistantResponse;


import React, { useState, useEffect } from 'react';

export default function App() {
  const [backendHealth, setBackendHealth] = useState({
    status: 'checking',
    project: 'Creator Content Intelligence',
    environment: 'development',
    version: '0.1.0',
  });

  useEffect(() => {
    fetch('/health')
      .then((res) => {
        if (!res.ok) throw new Error('Health check failed');
        return res.json();
      })
      .then((data) => setBackendHealth(data))
      .catch(() =>
        setBackendHealth((prev) => ({
          ...prev,
          status: 'offline',
        }))
      );
  }, []);

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="logo-area">
          <div className="logo-icon">C</div>
          <div className="logo-text">
            <h1>Creator Content Intelligence</h1>
            <p>AI-Powered YouTube Content Intelligence</p>
          </div>
        </div>
        <div className="status-badge">
          <span
            className={`status-dot ${
              backendHealth.status === 'healthy'
                ? 'healthy'
                : backendHealth.status === 'offline'
                ? 'offline'
                : 'connecting'
            }`}
          />
          <span>
            API Status:{' '}
            {backendHealth.status === 'healthy'
              ? `Online (${backendHealth.environment})`
              : backendHealth.status === 'offline'
              ? 'Disconnected'
              : 'Connecting...'}
          </span>
        </div>
      </header>

      {/* Hero Banner */}
      <section className="hero-banner">
        <div className="hero-badge">Phase 0 — Foundation Ready</div>
        <h2 className="hero-title">Evidence-Based YouTube Strategy</h2>
        <p className="hero-subtitle">
          Evaluate video ideas, benchmark title reach against historical evidence,
          and discover statistically verified content patterns using semantic retrieval and RAG.
        </p>
      </section>

      {/* Feature Navigation Shell */}
      <div className="cards-grid">
        <div className="feature-card">
          <div>
            <div className="card-header">
              <div className="card-icon">💡</div>
              <span className="card-phase">Phase 6 &amp; 9</span>
            </div>
            <h3 className="card-title">Idea Analyzer</h3>
            <p className="card-description">
              Explore natural-language video concepts, retrieve closely related historical
              videos, examine observed metrics, and discover evidence-backed content angles.
            </p>
          </div>
          <div className="card-footer">Awaiting semantic retrieval &amp; analytics layer</div>
        </div>

        <div className="feature-card">
          <div>
            <div className="card-header">
              <div className="card-icon">🎯</div>
              <span className="card-phase">Phase 7 &amp; 9</span>
            </div>
            <h3 className="card-title">Title Analyzer</h3>
            <p className="card-description">
              Benchmark proposed titles against similar content, compute historical reach
              distributions, identify title strengths/weaknesses, and generate evidence-based alternatives.
            </p>
          </div>
          <div className="card-footer">Awaiting reach estimation &amp; LLM reasoning</div>
        </div>

        <div className="feature-card">
          <div>
            <div className="card-header">
              <div className="card-icon">📊</div>
              <span className="card-phase">Phase 8 &amp; 9</span>
            </div>
            <h3 className="card-title">Dataset Insights</h3>
            <p className="card-description">
              Transparent, statistically validated findings derived from historical video data—covering
              title length patterns, numerical phrasing, and engagement distributions.
            </p>
          </div>
          <div className="card-footer">Awaiting database &amp; analytics pipeline</div>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Creator Content Intelligence &bull; Architecture Foundation (Phase 0)</p>
      </footer>
    </div>
  );
}

# CCI - Creator Content Intelligence

An evidence-driven AI platform for YouTube creators that helps evaluate video ideas, benchmark title reach against historical performance, discover observed dataset patterns, and generate evidence-based content recommendations.

---

## Product Vision

Creator Content Intelligence is designed to answer fundamental creator questions:
- *"I want to make a video about Python automation. What content opportunities exist?"*
- *"Is this title strong compared with similar videos in this niche?"*
- *"What kind of reach have similar videos historically achieved?"*
- *"Why does this title appear promising or weak?"*
- *"What alternative titles or content angles should I consider?"*
- *"What patterns can we observe from the historical videos in our dataset?"*

This is **not** a generic AI title generator, nor is it a black-box view predictor. Its core value comes from combining:
1. **Semantic Understanding**: Representing ideas and titles via vector embeddings.
2. **Historical Content Retrieval**: Finding closely related videos from actual YouTube data.
3. **Actual Performance Evidence**: Grounding all analysis in observed views, likes, and engagement metrics.
4. **Statistical Analysis**: Deterministic, transparent calculations (medians, percentiles, reach ranges).
5. **Retrieval-Augmented Generation (RAG)**: Factual context from official platform guidance and dataset insights.
6. **LLM Reasoning**: Clear synthesis, explanation, and actionable recommendations.

---

## Architectural Decision: Supervised ML is Intentionally Excluded from V1

The legacy iteration of this project attempted to train supervised regression models (`.pkl`) predicting view, like, and comment counts from limited metadata.

**Supervised ML has been intentionally discarded for V1:**
- Small and noisy historical datasets do not provide reliable generalizations for exact view predictions.
- Creators do not need false precision (e.g., *"Predicted views: 73,421"*); they need **evidence-based benchmarks** (e.g., *"Historical Reach Estimate: ~60K–85K views based on 8 closely related videos; Confidence: Moderate"*).
- The product architecture is built on **semantic retrieval + actual observed metrics + transparent statistics + RAG + LLM reasoning**.
- If a sufficiently large, validated dataset is accumulated in the future, supervised ML can be re-evaluated as an additional signal, but it is not part of V1.

---

## Core Architecture & Technology Stack

| Component | Technology | Responsibility |
|---|---|---|
| **Backend** | Python 3.10+, FastAPI, Pydantic | API endpoints, application services, validation |
| **Frontend** | React 18, Vite | Interactive UI, modern dark theme, evidence visualization |
| **Database** | PostgreSQL + pgvector | Relational data store and vector similarity search |
| **ORM & Migrations** | SQLAlchemy, Alembic | Data modeling and schema migration management |
| **Semantic Retrieval** | Embeddings | Vector representation of titles, descriptions, and concepts |
| **Quantitative Layer** | Deterministic Statistics | Median, percentiles, distribution, reach estimation, confidence |
| **Contextual Knowledge** | RAG | Official YouTube guidance and internal dataset insights |
| **Reasoning & Synthesis**| LLM Service | Structured analysis, strengths/weaknesses, title alternatives |
| **External Data** | YouTube Data API v3 | Historical video metadata and metric collection |

---

## Repository Structure

```text
creator-content-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (health, ideas, titles, insights)
│   │   ├── core/         # Settings, configuration, and logging
│   │   ├── database/     # SQLAlchemy models, session, repositories
│   │   ├── rag/          # Knowledge base and contextual retrievers
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # Application business logic (retrieval, analytics, LLM)
│   │   └── main.py       # FastAPI application entry point
│   ├── tests/            # Automated test suite (pytest)
│   └── requirements.txt  # Python backend dependencies
│
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── App.jsx       # Application shell
│   │   ├── main.jsx      # React root entry point
│   │   └── index.css     # Design system & styling
│   ├── index.html        # HTML entry point
│   ├── package.json      # Node dependencies and scripts
│   └── vite.config.js    # Vite configuration & backend proxy
│
├── data/
│   └── seed/             # Seed datasets (e.g. historical YouTube videos CSV)
├── docs/                 # Architecture specifications and documentation
├── scripts/              # Data collection and utility scripts
├── project_context.md    # Primary product and architecture specification
├── current_status.md     # Living project phase and implementation tracker
├── .env.example          # Sample environment variables
└── .gitignore            # Git exclusion rules
```

---

## 🗺️ Project Roadmap & Implementation Phases

- [x] **Phase 0 — Repository Reset & Architecture Foundation**: Clean slate, modular FastAPI foundation, React/Vite frontend shell, configuration, tests, and documentation.
- [ ] **Phase 1 — Database & Data Foundation**: PostgreSQL + pgvector setup, SQLAlchemy schema (`channels`, `videos`, `video_metrics`), Alembic migrations, seed ingestion.
- [ ] **Phase 2 — Embeddings & Semantic Retrieval**: Embedding provider abstraction, vector indexing, similarity search service.
- [ ] **Phase 3 — Analytics & Historical Reach Estimation**: Deterministic metrics, reach estimation range, confidence scoring.
- [ ] **Phase 4 — RAG Knowledge Layer**: Dual-source knowledge store (official guidance & dataset insights) and RAG retriever.
- [ ] **Phase 5 — LLM Reasoning Layer**: Structured prompt templates, LLM client abstraction, output schema parsing.
- [ ] **Phase 6 — Idea Analyzer API**: `POST /api/analyze/idea` end-to-end integration.
- [ ] **Phase 7 — Title Analyzer API**: `POST /api/analyze/title` end-to-end integration.
- [ ] **Phase 8 — Insights API**: `GET /api/insights` dataset pattern exploration.
- [ ] **Phase 9 — React Frontend**: Interactive Idea Analyzer, Title Analyzer, Insights dashboard, and evidence visualization.
- [ ] **Phase 10 — Evaluation & Polish**: End-to-end testing, error handling, performance optimization.

---

## Local Development Quickstart

### Prerequisites
- **Python 3.10+** (Python 3.14 supported)
- **Node.js 18+** & **npm**

### 1. Environment Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

### 2. Backend Setup & Execution

Navigate to the `backend/` directory:
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run automated tests
pytest tests/test_health.py -v

# Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```
FastAPI documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

### 3. Frontend Setup & Execution

In a separate terminal, navigate to `frontend/`:
```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
The React development UI will be available at:
- Web App: `http://localhost:5173`

---



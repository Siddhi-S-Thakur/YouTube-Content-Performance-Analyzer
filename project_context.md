# Project Context

## Project Name

# Creator Content Intelligence

**Working title:** `Creator Content Intelligence`

**Purpose:** Build an AI-powered YouTube content intelligence platform that helps creators evaluate video ideas, analyze titles, discover relevant historical content, understand observed performance patterns, and generate evidence-based content recommendations.

---

## 1. Product Vision

The product should help a creator answer questions such as:

- "I want to make a video about Python automation. What opportunities exist?"
- "Is this title strong compared with similar videos?"
- "What kind of reach have similar videos historically achieved?"
- "Why does this title appear promising or weak?"
- "What alternative titles or content angles should I consider?"
- "What patterns can we observe from the videos in our dataset?"

This is **not** intended to be a generic AI title generator.

Its core value comes from combining:

1. Semantic understanding
2. Historical YouTube content retrieval
3. Actual observed performance data
4. Statistical analysis
5. Retrieval-Augmented Generation (RAG)
6. LLM reasoning, explanation, and generation

The system should be evidence-first: the LLM should reason over retrieved evidence and structured analytics rather than inventing quantitative claims.

---

# 2. Major Architecture Decision: No Supervised ML

The previous version of the project used:

- Flask
- scikit-learn
- Jupyter notebooks
- serialized `.pkl` regression models
- a simple HTML/Bootstrap frontend

That architecture is being discarded.

The old supervised ML models for views, likes, and comments are **not part of the new system**.

The new project should be treated as a **fresh rebuild**, not a refactor of the old application.

Do not carry forward:

- Flask backend code
- old frontend
- Jupyter model-training workflow
- `.pkl` models
- ML inference endpoints
- old feature-engineering pipeline
- old application structure

The old historical dataset may be reused as seed/evidence data if useful, but it must not be treated as training data for a supervised prediction model.

### Why supervised ML is intentionally skipped

The earlier approach attempted to predict video performance from limited features such as title and publishing information. The available dataset was small, and the resulting supervised models were not reliable enough to justify making them the quantitative foundation of the product.

Rather than forcing ML into the architecture simply because this is an AI/ML-oriented project, the new system will use:

- semantic retrieval
- actual historical performance
- transparent statistics
- evidence-based estimation
- RAG
- LLM reasoning

This is an intentional product and engineering decision.

If the system later accumulates a sufficiently large, diverse, and reliable dataset, supervised ML can be reconsidered as an additional layer. It is not a V1 requirement.

---

# 3. Core Product Modes

The product should have two primary analysis modes.

## 3.1 Idea Analyzer

The user enters a natural-language idea.

Example:

> I want to make a video about Python automation.

The user should **not** need to know how to formulate a perfect YouTube title.

### Intended flow

```text
Natural-language idea
        ↓
Semantic understanding
        ↓
Embedding / semantic representation
        ↓
Related topics and concepts
        ↓
Historical video retrieval
        ↓
Actual performance data
        ↓
Statistical analysis
        ↓
Relevant RAG knowledge
        ↓
LLM reasoning
        ↓
Creator recommendations
```

### The result should help the creator understand

- What closely related videos already exist
- Which related topics/titles have demonstrated reach
- Historical performance distribution
- High-performing patterns observed in the dataset
- Potential content opportunities
- Possible title directions
- Potential content angles
- Why the recommendations are being made
- What evidence supports each recommendation

The system must clearly distinguish observed facts from generated suggestions.

---

## 3.2 Title Analyzer

The user directly enters a proposed YouTube title.

Example:

> 10 Python Automation Scripts That Will Save You Hours

The system should:

1. Understand the title
2. Identify its topic, intent, and important concepts
3. Retrieve semantically similar historical videos
4. Inspect their actual performance
5. Calculate a historical reach estimate
6. Analyze title characteristics
7. Explain strengths and weaknesses
8. Generate improved title alternatives

The output should clearly separate:

- Historical evidence
- Statistical estimates
- Factual/contextual knowledge
- LLM-generated recommendations

---

# 4. Historical Reach Estimation

The product can provide an estimated performance range, but this must **not** be presented as a precise ML prediction.

Preferred terminology:

- Historical Reach Estimate
- Evidence-Based Reach Estimate
- Estimated Performance Range
- Historical Performance Benchmark

Avoid false precision such as:

> Predicted views: 73,421

Prefer:

> Historical Reach Estimate: ~60K–85K views  
> Based on 8 closely related videos  
> Confidence: Moderate

## 4.1 Baseline methodology

The initial approach should be:

```text
1. Retrieve top-k semantically similar videos.
2. Filter for relevance and data quality.
3. Collect actual views/likes/comments.
4. Calculate median and percentile ranges.
5. Measure dispersion/uncertainty.
6. Optionally calculate a similarity-weighted estimate.
7. Generate a confidence level.
```

A similarity-weighted estimate can conceptually be:

```text
estimate =
Σ(similarity_i × views_i)
--------------------------
Σ(similarity_i)
```

The exact methodology should be implemented transparently and documented.

## 4.2 Confidence

Confidence should depend on factors such as:

- Number of relevant videos
- Semantic similarity of retrieved videos
- Variance in their observed performance
- Data completeness
- Recency where appropriate

A small number of weakly similar videos must result in lower confidence.

The system should never manufacture confidence simply because an estimate is required by the UI.

---

# 5. Responsibilities of Each Technology

The architecture should keep responsibilities explicit.

## 5.1 Embeddings

**Purpose:** Understand semantic meaning and retrieve conceptually similar content.

Embeddings should be the primary mechanism for semantic retrieval rather than relying only on exact keyword matching.

Potential embedded content:

- Video title
- Description
- Later: transcript
- Normalized topic/metadata representation

The embedding provider should be abstracted behind a service interface so it can be changed without rewriting the application.

---

## 5.2 PostgreSQL

**Purpose:** Primary application database and source of truth.

PostgreSQL should store:

- Channels
- Videos
- Video metadata
- Video metrics
- Embeddings
- Knowledge documents
- Dataset-derived insights
- Analysis history if required

---

## 5.3 pgvector

**Purpose:** Vector similarity search inside PostgreSQL.

Use PostgreSQL + pgvector initially instead of introducing a separate vector database.

There is no current need for Pinecone, Weaviate, Milvus, etc.

Keeping vectors and relational data together will simplify:

- deployment
- querying
- metadata filtering
- development
- maintenance

A separate vector database can be reconsidered only if scale or requirements justify it.

---

## 5.4 Analytics / Statistics

**Purpose:** Quantitatively interpret observed historical data.

Potential analytics include:

- Median views
- Mean views where appropriate
- Percentile ranges
- View distribution
- Like rate
- Comment rate
- Engagement rate
- Title length patterns
- Number usage
- Topic-level performance
- Publishing-time patterns
- Historical performance by category/topic
- Similarity-weighted estimates
- Confidence/uncertainty

Analytics should be deterministic, transparent, and reproducible.

The LLM should not be responsible for calculating these values.

---

## 5.5 RAG

**Purpose:** Retrieve factual/contextual knowledge that the LLM should use when reasoning.

The RAG knowledge base should have at least two clearly distinguished source types.

### Source A — Official YouTube / Creator Knowledge

Examples:

- Official YouTube documentation
- Official creator guidance
- Authoritative platform documentation

### Source B — Internal Dataset Insights

Examples:

- Statistics calculated from collected historical videos
- Observed title patterns
- Observed topic patterns
- Observed engagement patterns

These two sources must never be silently mixed.

The UI and/or API should make it possible to tell whether a statement comes from:

- official external knowledge
- internal dataset evidence
- model-generated reasoning

---

## 5.6 LLM

**Purpose:** Reasoning, explanation, synthesis, and generation.

The LLM may:

- Explain analytical results
- Compare retrieved examples
- Identify strengths and weaknesses
- Generate title alternatives
- Suggest content angles
- Summarize retrieved knowledge
- Turn structured analytics into creator-friendly recommendations
- Explain why an estimate has a particular confidence level

The LLM must **not invent quantitative evidence**.

Where a number is presented, it should originate from the analytics/retrieval layer or a clearly identified source.

The LLM should preferably receive structured evidence and return structured output.

---

# 6. Dataset Insights / Knowledge Page

The product should include a page where users can explore guidelines and patterns learned from the collected dataset.

Potential insights:

- Title length patterns
- Use of numbers in titles
- Common title structures
- Topic clusters
- Engagement patterns
- Publishing-time patterns
- High-performing vs lower-performing title characteristics
- Recurring words or phrases
- Other statistically observable patterns

Every dataset-derived insight should include context such as:

- Sample size
- Metric used
- Time range where relevant
- Methodology
- Important limitations

### Example of appropriate wording

> In our analyzed dataset, titles containing numbers had a higher median view count than titles without numbers.

### Avoid universal claims

Do not write:

> YouTube's algorithm prefers titles with numbers.

The product should distinguish:

- observation
- correlation
- causation

Unless causal evidence exists, the system should not imply causation.

---

# 7. Search and Retrieval Strategy

Semantic vector search is the primary retrieval mechanism.

A future hybrid search layer may combine:

- Vector similarity
- PostgreSQL full-text/keyword search
- Metadata filters

Potential filters:

- Channel
- Topic/category
- Date range
- Language
- Video type
- Data quality
- Minimum available metrics

Retrieval results should contain enough metadata to understand:

- What was matched
- How relevant it was
- What performance it had
- Why it was included in the analysis

The retrieval layer should be deterministic and testable independently of the LLM.

---

# 8. Initial Data Model

The exact database schema should be finalized during implementation, but the domain should be based around the following concepts.

## `channels`

Stores YouTube channel information.

Possible fields:

- `id`
- `youtube_channel_id`
- `name`
- `description`
- `subscriber_count` when available
- `created_at`
- `updated_at`

---

## `videos`

Stores relatively stable video metadata.

Possible fields:

- `id`
- `youtube_video_id`
- `channel_id`
- `title`
- `description`
- `published_at`
- `duration`
- `url`
- `language`
- `category`
- `created_at`
- `updated_at`

---

## `video_metrics`

Stores observed performance measurements.

Possible fields:

- `id`
- `video_id`
- `view_count`
- `like_count`
- `comment_count`
- `captured_at`

Keeping metrics separate allows future periodic snapshots and performance-over-time analysis.

---

## `video_embeddings`

Stores searchable vector representations.

Possible fields:

- `id`
- `video_id`
- `content_type`
- `embedding`
- `model_name`
- `created_at`

`content_type` can distinguish title, description, combined text, transcript, etc.

---

## `knowledge_documents`

Stores RAG knowledge.

Possible fields:

- `id`
- `source_type`
- `title`
- `content`
- `source_url`
- `metadata`
- `embedding`
- `created_at`
- `updated_at`

`source_type` should distinguish official knowledge from internal dataset insights.

---

## `insights`

Stores structured dataset-derived findings.

Possible fields:

- `id`
- `title`
- `description`
- `metric`
- `methodology`
- `sample_size`
- `time_range`
- `confidence/limitations`
- `source_data_reference`
- `embedding`
- `created_at`
- `updated_at`

The exact schema can evolve after the first retrieval and analytics implementation.

---

# 9. Backend Architecture

Use **FastAPI** as the backend framework.

The backend should be API-first and organized by responsibility.

Suggested structure:

```text
backend/
├── main.py
├── api/
│   ├── ideas.py
│   ├── titles.py
│   ├── search.py
│   ├── insights.py
│   └── ingestion.py
│
├── services/
│   ├── llm_service.py
│   ├── embedding_service.py
│   ├── retrieval_service.py
│   ├── analytics_service.py
│   └── youtube_service.py
│
├── rag/
│   ├── retriever.py
│   └── knowledge_base.py
│
├── database/
│   ├── connection.py
│   ├── models.py
│   └── repositories/
│
├── schemas/
│   ├── idea.py
│   ├── title.py
│   ├── search.py
│   └── insights.py
│
└── core/
    ├── config.py
    └── logging.py
```

This is a starting structure, not a rigid requirement.

Business logic should not be embedded directly inside route handlers.

---

# 10. Frontend Architecture

Use:

- React
- Vite

The frontend should be a modern application rather than a server-rendered Flask template.

Potential pages:

```text
/
├── Idea Analyzer
├── Title Analyzer
├── Insights / Knowledge
└── History (optional)
```

The frontend should consume structured FastAPI APIs.

Avoid putting analytical logic in React. The frontend should primarily:

- collect input
- request analysis
- display evidence
- display statistics
- display recommendations
- visualize relevant comparisons

---

# 11. Initial API Direction

Exact request/response schemas should be designed before implementation.

Suggested endpoints:

### Idea analysis

```http
POST /api/analyze/idea
```

Input:

```json
{
  "idea": "I want to make a video about Python automation."
}
```

Output should contain structured analysis such as:

- interpreted topic
- related concepts
- similar videos
- historical metrics
- reach estimate
- confidence
- dataset insights
- relevant RAG evidence
- content opportunities
- title suggestions
- explanation

---

### Title analysis

```http
POST /api/analyze/title
```

Input:

```json
{
  "title": "10 Python Automation Scripts That Will Save You Hours"
}
```

Output should contain:

- title analysis
- topic/intent
- similar videos
- historical performance
- reach estimate
- confidence
- strengths
- weaknesses
- relevant insights
- title alternatives
- supporting evidence

---

### Similar content search

```http
POST /api/search/similar
```

Used independently for semantic retrieval and debugging.

---

### Dataset insights

```http
GET /api/insights
```

Returns available structured insights.

---

### Data ingestion

Potentially:

```http
POST /api/ingestion/...
```

Exact ingestion endpoints should be designed after the data model and YouTube integration are finalized.

---

### Health

```http
GET /health
```

---

# 12. LLM Output Contract

LLM responses should preferably be structured rather than arbitrary prose.

For example:

```json
{
  "summary": "...",
  "topic": "...",
  "intent": "...",
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "title_alternatives": [],
  "evidence": [],
  "confidence": "moderate"
}
```

The exact schema will be defined during implementation.

Important principle:

**Analytics produces facts and numbers.  
Retrieval produces evidence.  
RAG produces contextual knowledge.  
LLM produces interpretation and recommendations.**

---

# 13. Evidence and Source Attribution

The system should be designed so that important recommendations can be traced to evidence.

For example:

```text
Recommendation
    ↓
Supporting insight
    ↓
Underlying dataset statistics
    ↓
Relevant historical videos
```

For external knowledge:

```text
Recommendation
    ↓
Retrieved RAG passage
    ↓
Official source
```

The product should avoid opaque recommendations where the user cannot understand why the system reached a conclusion.

---

# 14. YouTube Data Ingestion

YouTube Data API v3 can be used to collect historical content and metadata.

The ingestion system should be designed to:

1. Discover relevant videos/channels
2. Store stable metadata
3. Store observed metrics
4. Normalize fields
5. Generate embeddings
6. Make the content searchable

Ingestion should be separated from analysis.

Do not make live YouTube API calls for every user analysis if the required historical evidence can be served from the local database.

Use the database as the primary analysis corpus.

Live API access can be added where necessary for fresh information.

---

# 15. Development Principles

## Evidence first

Never let the LLM manufacture data.

## Explainability

Users should understand where major claims came from.

## Separation of concerns

Keep these layers independent:

```text
API
 ↓
Application Services
 ↓
Retrieval / Analytics / RAG / LLM
 ↓
Database / External APIs
```

## Provider abstraction

LLM and embedding providers should be accessed through service interfaces rather than scattered provider-specific calls throughout the codebase.

## Testability

Core retrieval and analytics functions should be testable without invoking an LLM.

## Reproducibility

Statistical calculations should be deterministic and documented.

## Honest uncertainty

The product must not present weak evidence as strong evidence.

## Progressive complexity

Start with the smallest architecture that supports the product.

Do not introduce:

- a separate vector database
- microservices
- distributed queues
- complex ML pipelines
- unnecessary infrastructure

until actual requirements justify them.

---

# 16. Proposed Technology Stack

## Frontend

- React
- Vite

## Backend

- Python
- FastAPI

## Database

- PostgreSQL
- pgvector

## Data/analytics

- Python
- pandas and/or SQL-based analytics where appropriate

## External data

- YouTube Data API v3

## AI

- LLM provider through an abstraction layer
- Embedding provider through an abstraction layer

## ORM / migrations

Recommended direction:

- SQLAlchemy
- Alembic

Exact choices can be finalized during implementation.

---

# 17. Project Structure

A clean starting repository could look like:

```text
creator-content-intelligence/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.*
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── rag/
│   │   ├── database/
│   │   ├── schemas/
│   │   └── core/
│   ├── tests/
│   └── requirements.txt / pyproject.toml
│
├── data/
│   └── seed/
│
├── docs/
│
├── scripts/
│
├── project_context.md
├── README.md
└── .env.example
```

The exact structure can change if the implementation benefits from a simpler organization.

---

# 18. V1 Scope

The first implementation should focus on proving the core loop.

### V1 should include

- PostgreSQL + pgvector
- YouTube historical dataset ingestion
- Embedding generation
- Semantic similar-video retrieval
- Actual performance statistics
- Historical reach estimate
- Confidence calculation
- Idea Analyzer
- Title Analyzer
- Basic RAG knowledge base
- LLM explanation/recommendations
- Dataset Insights page
- React/Vite frontend
- FastAPI backend

### V1 should not include

- Supervised ML
- Model training
- `.pkl` models
- Microservices
- Separate vector database
- Complex real-time streaming infrastructure
- Over-engineered agent orchestration

---

# 19. Suggested Implementation Order

Do not begin by building the entire UI.

Build the system from the evidence layer upward.

Recommended order:

```text
1. Finalize architecture and database schema
2. Set up PostgreSQL + pgvector
3. Import/normalize seed YouTube data
4. Implement embedding generation
5. Implement semantic retrieval
6. Implement analytics/statistical layer
7. Implement historical reach estimation
8. Build RAG knowledge ingestion/retrieval
9. Add LLM reasoning service
10. Define and implement FastAPI contracts
11. Build Idea Analyzer API
12. Build Title Analyzer API
13. Build Insights API
14. Build React/Vite frontend
15. Add evaluation/tests
16. Improve UX and recommendation quality
```

The most important milestone is:

> Given an idea or title, retrieve genuinely relevant historical videos, calculate trustworthy statistics from their actual performance, and use an LLM to explain the evidence and generate useful recommendations.

If this loop works well, the rest of the product can be built around it.

---

# 20. Product Language

Use careful language throughout the UI.

Prefer:

- "Based on similar videos in our dataset..."
- "Historical performance..."
- "Observed pattern..."
- "Estimated range..."
- "Evidence suggests..."
- "Moderate confidence..."
- "Our dataset shows..."

Avoid:

- "The algorithm will..."
- "YouTube prefers..."
- "This video will get..."
- "Guaranteed views..."
- "Predicted views: exact number..."

The product is an intelligence and decision-support system, not a guarantee engine.

---

# 21. Success Criteria

The project is successful when a creator can enter a rough idea or title and quickly receive:

1. Relevant historical examples
2. Actual observed performance
3. A transparent historical benchmark/range
4. An explanation of the evidence
5. Relevant dataset insights
6. Relevant factual knowledge
7. Actionable title/content recommendations
8. Clear confidence and limitations

The system should feel like:

> **"An intelligent research and decision-support assistant for YouTube content."**

It should not feel like:

> **"A chatbot guessing how many views your video will get."**

---

# 22. Agent Instructions

When an implementation agent works on this repository:

- Treat this file as the product/architecture context.
- Do not reintroduce supervised ML unless explicitly requested.
- Do not resurrect the old Flask/Bootstrap architecture.
- Do not assume the old `.pkl` models are required.
- Prefer simple, modular architecture.
- Keep retrieval, analytics, RAG, and LLM responsibilities separate.
- Do not fabricate data during development.
- Clearly mark mock/demo data if it is ever necessary.
- Build APIs around structured contracts.
- Keep important calculations outside the LLM.
- Add tests for retrieval and analytics logic.
- Prefer PostgreSQL + pgvector over introducing a second vector database.
- Keep provider-specific AI code behind service abstractions.
- Preserve source attribution and evidence throughout the analysis pipeline.
- Optimize for a working end-to-end vertical slice before adding secondary features.

---

# 23. Current Decision Summary

| Decision | Choice |
|---|---|
| Project type | AI-powered YouTube content intelligence |
| Supervised ML | **Skipped for V1** |
| Old Flask app | Discard |
| Old ML models | Discard |
| Frontend | React + Vite |
| Backend | FastAPI |
| Database | PostgreSQL |
| Vector search | pgvector |
| Semantic search | Embeddings |
| Quantitative layer | Statistics + historical evidence |
| RAG | Yes |
| LLM | Yes |
| YouTube data | YouTube Data API v3 |
| Primary user modes | Idea Analyzer + Title Analyzer |
| Historical estimate | Evidence-based range, not precise ML prediction |
| Insights page | Yes |
| Separate vector DB | Not initially |
| Microservices | Not initially |

---

## Final Product Definition

**Creator Content Intelligence** is an evidence-driven AI platform for YouTube creators.

It combines:

```text
Creator Idea / Title
        ↓
Semantic Understanding
        ↓
Historical Content Retrieval
        ↓
Actual Performance Evidence
        ↓
Statistical Analysis
        ↓
RAG Knowledge
        ↓
LLM Reasoning
        ↓
Actionable Creator Intelligence
```

The fundamental principle is:

> **Use data and retrieval to establish what is known; use statistics to quantify it; use RAG to provide factual context; and use the LLM to reason about it and communicate it clearly.**

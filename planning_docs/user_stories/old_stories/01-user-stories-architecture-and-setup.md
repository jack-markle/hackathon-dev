### User Stories – Architecture and Project Setup (Milestone 1)

These stories capture the needs around initial architecture decisions, repository scaffolding, and environment setup. They support the outcomes described in `01-architecture-and-project-setup.md`.

---

### Story A1 – Shared Architectural Understanding

**As a** team member (developer, analyst, or AI lead)  
**I want** a clear, documented architecture for the AI Pricing Monitor & Advisor  
**So that** we can build and discuss the system using the same mental model.

**Acceptance Criteria**

- **Architecture document exists** that explains:
  - Pricing Analyst Console (Next.js)
  - Pricing Orchestrator (FastAPI + LangChain)
  - Conceptual agents:
    - Environmental
    - Supply & Demand
    - Loyalty
    - Historical
  - n8n workflow for logging/alerts.
- **High-level diagram** shows:
  - Console → Orchestrator → Agents → n8n.
- The architecture document references the core API contract for `/api/v1/recommendation`.

---

### Story A2 – Backend and Frontend Skeletons

**As a** backend or frontend developer  
**I want** a consistent repository structure with skeleton files  
**So that** I can start implementing features without bikeshedding folder layout.

**Acceptance Criteria**

- Repository contains at least:
  - `backend/app/main.py` – FastAPI entrypoint skeleton.
  - `backend/app/api/v1/recommendation.py` – route placeholder.
  - `backend/app/models/recommendation.py` – request/response models.
  - `frontend/app/page.tsx` – root console page skeleton.
  - `orchestration/agents/*.py` and `orchestration/chains/pricing_explanation_chain.py` – all with TODO docstrings.
- `requirements.txt` and `package.json` exist with minimal dependencies to run skeleton apps.
- Running the following commands starts minimal servers (even if returning placeholders only):

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

---

### Story A3 – Agreed Recommendation API Contract

**As a** frontend developer and pricing analyst  
**I want** a stable request/response shape for the recommendation endpoint  
**So that** the UI and demos can be built in parallel with backend logic.

**Acceptance Criteria**

- A shared contract is defined (e.g., in `backend/app/models/recommendation.py` and documentation) with:

```json
{
  "zone": "string",
  "scenario": "string",
  "time": "ISO-8601 string",
  "loyalty_segment": "string | null",
  "notes": "string | null"
}
```

and response shape:

```json
{
  "recommended_adjustment": 0.0,
  "goodness": 0.0,
  "factors": {
    "environment": "string",
    "supply_demand": "string",
    "loyalty": "string",
    "historical": "string"
  },
  "reasoning": "string"
}
```

- Any changes to the contract must be explicitly discussed and reflected in models and docs.

---

### Story A4 – Local Development Environments

**As a** developer  
**I want** a quick way to set up Python and Node environments  
**So that** onboarding and collaboration are frictionless during the hackathon.

**Acceptance Criteria**

- Backend setup instructions documented (e.g., in `README` or planning docs), including:
  - Python version.
  - Virtual environment creation.
  - `pip install -r requirements.txt`.
- Frontend setup instructions documented, including:
  - Node version (or `.nvmrc`).
  - `npm install` or `yarn install`.
- A new developer can:
  - Clone the repo.
  - Follow the instructions.
  - Run backend and frontend locally without needing undocumented steps.



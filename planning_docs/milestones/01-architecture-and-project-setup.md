### Milestone 1 – Architecture, Repo Setup, and Environments

**Goal:** Establish a clean, convention-based project structure and shared understanding of the architecture so the team can build in parallel with minimal friction.

---

### 1.1 Outcomes

- **Shared architecture**: Everyone understands the orchestrator + conceptual agents + corporate pressure tool + UI + n8n flow.
- **Repo structure ready**: Backend (FastAPI), frontend (Next.js), orchestration, and infra folders exist.
- **Environments**: Basic Python and Node environments set up and reproducible (e.g., via `requirements.txt` and `package.json`).
- **Run scripts**: Simple commands exist to run backend and frontend locally (even if they only serve “Hello, world” or placeholder responses).

---

### 1.2 Proposed Repository Layout

This is a **reference structure** to keep things organized. Names can be adjusted, but keep clear separation of concerns.

```bash
ai-pricing-advisor/
  backend/
    app/
      main.py                  # FastAPI app entrypoint (skeleton only)
      api/
        __init__.py
        v1/
          __init__.py
          recommendation.py    # /recommendation route definition (skeleton)
      core/
        config.py              # Settings / environment configuration
      models/
        recommendation.py      # Pydantic request/response schemas

    requirements.txt           # Backend dependencies (FastAPI, pydantic, etc.)

  frontend/
    app/
      page.tsx                 # Next.js root page (Pricing Analyst Console shell)
    package.json               # Frontend dependencies (Next.js, React, etc.)

  orchestration/
    chains/
      pricing_explanation_chain.py  # LangChain explanation chain factory (skeleton)
    agents/
      environment_agent.py
      loyalty_agent.py
      supply_demand_agent.py
      historical_agent.py
      corporate_pressure_agent.py   # Interprets corporate revenue goals/strategy

  infra/
    n8n/
      pricing_goodness_alert.json   # Example workflow export (reference only)

  planning_docs/
    milestones/
    user_stories/
```

> Note: At this milestone, the code files above should exist as **empty or near-empty skeletons** with docstrings/TODOs only—no real business logic yet.

---

### 1.3 Backend Skeleton (FastAPI) – No Business Logic

Create ultra-thin skeletons that future milestones will fill in.

```python
# backend/app/main.py
from fastapi import FastAPI

from app.api.v1 import recommendation


def create_app() -> FastAPI:
    """
    Application factory.
    Business logic is implemented in later milestones.
    """
    app = FastAPI(title="AI Pricing Monitor & Advisor")
    app.include_router(recommendation.router, prefix="/api/v1")
    return app


app = create_app()
```

```python
# backend/app/api/v1/recommendation.py
from fastapi import APIRouter
from app.models.recommendation import RecommendationRequest, RecommendationResponse

router = APIRouter(tags=["recommendation"])


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    """
    Placeholder endpoint to be implemented in later milestones.
    For now, this may return a hard-coded or minimal stub response.
    """
    raise NotImplementedError("Business logic is implemented in Milestone 2.")
```

```python
# backend/app/models/recommendation.py
from pydantic import BaseModel
from typing import Dict


class RecommendationRequest(BaseModel):
    zone: str
    scenario: str
    time: str
    loyalty_segment: str | None = None
    notes: str | None = None
    # Corporate pressure / strategy inputs:
    corporate_revenue_goal: float | None = None  # e.g., target uplift percentage or index
    corporate_strategy_notes: str | None = None  # free-text description of current strategy


class RecommendationResponse(BaseModel):
    recommended_adjustment: float
    goodness: float
    factors: Dict[str, str]
    reasoning: str
```

> These models are defined early to give both backend and frontend teams a shared contract, even if actual logic is not yet in place.

---

### 1.4 Frontend Skeleton (Next.js – App Router)

Create a minimal page that will later become the Pricing Analyst Console.

```tsx
// frontend/app/page.tsx
export default function PricingAnalystConsolePage() {
  // Milestone 4 will introduce the full form and wiring to the backend.
  return (
    <main className="min-h-screen flex flex-col items-center justify-center">
      <section className="max-w-2xl w-full px-4">
        <h1 className="text-2xl font-semibold mb-4">
          AI Pricing Monitor & Advisor
        </h1>
        <p className="text-gray-600">
          Placeholder console. The scenario form and results panel will be
          implemented in later milestones.
        </p>
      </section>
    </main>
  );
}
```

---

### 1.5 Orchestration & Agents Skeleton (LangChain)

Create empty factories with clear names; no chain wiring yet.

```python
# orchestration/agents/environment_agent.py
"""
Environment Agent

Responsibility: Evaluate environmental factors such as storms, road closures,
and emergencies and express them as a pricing adjustment factor.

Implementation is added in Milestone 3.
"""

from typing import Any, Dict


def evaluate_environment(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns an interim environmental factor object.
    Implementation TBD. Should NOT call external APIs in the hackathon demo
    unless explicitly decided later.
    """
    raise NotImplementedError
```

Similar skeletons should exist for:

- `loyalty_agent.py`
- `supply_demand_agent.py`
- `historical_agent.py`

And a placeholder chain factory:

```python
# orchestration/chains/pricing_explanation_chain.py
"""
LangChain-based explanation chain.

Takes in computed factors and produces a BA-friendly reasoning string.
Actual LLM prompt and wiring is implemented in Milestone 3.
"""

from typing import Any, Dict


def build_pricing_explanation_chain() -> Any:
    """
    Returns a chain object that can be invoked with pricing context.
    Implementation added in a later milestone.
    """
    raise NotImplementedError
```

---

### 1.6 Definition of Done

- **Architecture agreed** and documented (mirrors the hackathon proposal: console → orchestrator → conceptual agents → n8n).
- **Repo structure created** with backend, frontend, orchestration, and infra folders.
- **Key skeleton files exist**: FastAPI `main.py`, `recommendation.py`, Pydantic models (including corporate pressure fields), basic Next.js page, agent and chain skeletons.
- **Teams can run**:

```bash
# Backend (example)
cd backend
uvicorn app.main:app --reload

# Frontend (example)
cd frontend
npm run dev
```

- No production logic is implemented yet; all meaningful computation is deferred to later milestones.

---

### 1.7 Developer Lanes (4-Day Hackathon, 5 Developers)

To maximize parallel work from Day 1, we split responsibility into five lanes that map to later milestones and dedicated user-story files (`dev_1_stories.md`–`dev_5_stories.md`):

- **Dev 1 – Backend Core Pricing Logic**
  - Owns `backend/app/services/recommendation_service.py` and core factor math.
  - Focuses on environment, supply/demand, loyalty, historical, and corporate pressure numeric factors and guardrails.
- **Dev 2 – Orchestrator, Agents, and LangChain**
  - Owns `orchestration/orchestrator.py`, `orchestration/agents/*`, and `orchestration/chains/pricing_explanation_chain.py`.
  - Integrates the Corporate Pressure Determinator while respecting market physics and ethical guardrails.
- **Dev 3 – Next.js Pricing Analyst Console**
  - Owns `frontend/app/page.tsx` and related UI components/styles.
  - Implements all form inputs (including corporate revenue goal/strategy) and result display.
- **Dev 4 – n8n & Integrations**
  - Owns `infra/n8n/*` and `backend/app/integrations/n8n_notifier.py`.
  - Ensures alerts fire correctly without blocking user requests.
- **Dev 5 – Data, Scenarios, Testing & Demo**
  - Curates mock data, scripted scenarios (including corporate pressure examples), and light tests.
  - Helps refine prompts, UX polish, and presentation artifacts.

Each developer’s detailed user stories and any shared technical contracts they rely on are captured in the `planning_docs/user_stories/dev_<x>_stories.md` files to reduce cross-branch conflicts.




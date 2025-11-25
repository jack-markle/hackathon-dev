### Milestone 2 – Backend Recommendation Logic (FastAPI)

**Goal:** Implement a coherent, testable backend recommendation pipeline that computes adjustment factors and returns the contract defined in Milestone 1.

---

### 2.1 Outcomes

- **`POST /api/v1/recommendation`** returns a **non-hardcoded**, but still hackathon-simple recommendation.
- All four conceptual factors are represented in code:
  - `environment_factor`
  - `supply_demand_factor`
  - `loyalty_factor`
  - `historical_factor`
- Factors are combinable into:
  - `recommended_adjustment` (e.g., `0.10` for +10%)
  - `goodness` score between `0.0` and `1.0`
- Guardrails exist in code (e.g., special handling for emergencies).

---

### 2.2 Recommendation Service Structure

Keep controller logic thin and core logic in a dedicated service module.

```python
# backend/app/services/recommendation_service.py
from typing import Dict
from app.models.recommendation import RecommendationRequest, RecommendationResponse


def compute_environment_factor(req: RecommendationRequest) -> float:
    """Derive a simple percentage adjustment from environment conditions."""
    # Implementation: small lookup / heuristic (added in this milestone)
    raise NotImplementedError


def compute_supply_demand_factor(req: RecommendationRequest) -> float:
    """Derive adjustment from time of day / pseudo demand-supply ratio."""
    raise NotImplementedError


def compute_loyalty_factor(req: RecommendationRequest) -> float:
    """Discount or soften surge based on loyalty tier."""
    raise NotImplementedError


def compute_historical_factor(req: RecommendationRequest) -> float:
    """Approximate adjustment based on mock historical scenarios."""
    raise NotImplementedError


def combine_factors(
    env: float,
    supply_demand: float,
    loyalty: float,
    historical: float,
) -> Dict[str, float]:
    """
    Combine individual factors into a single recommended adjustment and
    a 'goodness' score.
    """
    raise NotImplementedError


def build_recommendation(req: RecommendationRequest) -> RecommendationResponse:
    """
    Orchestrates factor computation and produces the final response
    (without natural-language reasoning – that is Milestone 3).
    """
    raise NotImplementedError
```

The `api/v1/recommendation.py` route will call `build_recommendation` and later also invoke the LangChain explanation chain.

---

### 2.3 Guardrails: Emergencies and Fairness

Codify the strategic guardrails noted in `notes.txt` and the proposal:

- **In case of emergency (e.g., disaster scenario)**:
  - Do **not** apply aggressive markup, even if demand is high.
  - Optionally cap the adjustment at a small positive number or even `0.0`.
- **Loyal customers**:
  - Apply **softer surge** for loyal segments.

Example pseudo-logic (to be implemented with real condition checks):

```python
def apply_guardrails(
    base_adjustment: float,
    scenario: str,
    loyalty_segment: str | None,
) -> float:
    """
    Enforce guardrails such as limiting surge during emergencies and
    softening surge for loyal customers.
    """
    # Pseudocode, implementation done in this milestone:
    #
    # if scenario in {"natural_disaster", "emergency"}:
    #     return min(base_adjustment, 0.0)
    #
    # if loyalty_segment in {"gold", "platinum"}:
    #     return base_adjustment * 0.7
    #
    raise NotImplementedError
```

---

### 2.4 Example Request/Response Contract

Use this example to validate the backend behavior.

**Request** (from frontend or API client):

```json
{
  "zone": "airport_corridor",
  "scenario": "road_closure",
  "time": "2025-11-27T18:00:00Z",
  "loyalty_segment": "gold",
  "notes": "evening commute, partial freeway closure"
}
```

**Response** (example shape – values are illustrative):

```json
{
  "recommended_adjustment": 0.1,
  "goodness": 0.78,
  "factors": {
    "environment": "Road closure near airport adds moderate travel time (+5%).",
    "supply_demand": "Driver supply tight vs ride requests at 6pm (+10%).",
    "loyalty": "Gold segment gets softened surge (-5%).",
    "historical": "Similar airport evening trips succeed around 1.05x."
  },
  "reasoning": "Explanation to be filled by LangChain in Milestone 3."
}
```

> During this milestone, `reasoning` can be a simple placeholder string. Milestone 3 replaces it with a real LLM-generated explanation.

---

### 2.5 Testing Strategy

- **Unit tests** (lightweight, if time allows):
  - `compute_environment_factor` for different scenarios (normal, storm, road closure, emergency).
  - `compute_loyalty_factor` for different loyalty segments.
  - `apply_guardrails` for emergency and loyalty combinations.
- **Contract tests**:
  - For 2–3 scripted scenarios (e.g., “storm downtown”, “concert at stadium”, “holiday morning”), ensure:
    - `recommended_adjustment` and `goodness` are within expected ranges.
    - `factors` keys are all present.

---

### 2.6 Definition of Done

- `POST /api/v1/recommendation` returns a structured response with non-zero logic-based adjustments.
- All four factor functions implemented with simple, explainable heuristics.
- Guardrails implemented and demonstrably working in at least one scenario.
- Example scenarios are documented (for frontend and demo) and can be replayed consistently.



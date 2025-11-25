### Milestone 3 – Orchestrator, Agents, and LangChain Reasoning

**Goal:** Connect backend factor computation with conceptual agents and a LangChain explanation chain that produces BA-friendly reasoning.

---

### 3.1 Outcomes

- Orchestrator module that:
  - Invokes environmental, loyalty, supply/demand, and historical logic (conceptual “agents”).
  - Combines results into final adjustment and goodness.
  - Calls a LangChain chain to generate natural-language reasoning.
- `reasoning` field in `RecommendationResponse` now contains LLM-generated text based on factors.
- Agents and chain implementation remain **simple and deterministic** for the demo.

---

### 3.2 Orchestrator Structure

Introduce an orchestrator layer so the FastAPI route calls **one clear function**.

```python
# orchestration/orchestrator.py
from typing import Dict, Any

from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services import recommendation_service
from orchestration.chains.pricing_explanation_chain import build_pricing_explanation_chain


def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    """
    High-level orchestration:
      1. Compute numeric factors (service).
      2. Call explanation chain with factors and proposed adjustment.
      3. Return RecommendationResponse with populated reasoning.
    """
    # Pseudocode; real wiring implemented in this milestone.
    #
    # factors = recommendation_service.compute_all_factors(req)
    # adjustment_info = recommendation_service.combine_factors(**factors)
    #
    # chain = build_pricing_explanation_chain()
    # reasoning = chain.invoke({
    #   "request": req.dict(),
    #   "factors": factors,
    #   "adjustment": adjustment_info,
    # })
    #
    # return RecommendationResponse(
    #   recommended_adjustment=adjustment_info["recommended_adjustment"],
    #   goodness=adjustment_info["goodness"],
    #   factors=factors["summaries"],
    #   reasoning=reasoning,
    # )
    raise NotImplementedError
```

Update the FastAPI route to use the orchestrator:

```python
# backend/app/api/v1/recommendation.py (conceptual change)
from orchestration.orchestrator import orchestrate_pricing_recommendation


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    return orchestrate_pricing_recommendation(payload)
```

---

### 3.3 Conceptual Agents Implementation

Agents can be lightweight functions with clear single responsibilities, backed by lookup tables or simple rules.

- `environment_agent.py`
- `loyalty_agent.py`
- `supply_demand_agent.py`
- `historical_agent.py`

Example pattern:

```python
# orchestration/agents/loyalty_agent.py
from typing import Dict, Any


def evaluate_loyalty(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map a loyalty segment into:
      - numeric factor adjustment
      - a short human-readable summary string
    """
    # Pseudocode:
    # segment = context.get("loyalty_segment") or "standard"
    # if segment == "gold":
    #   return {"factor": -0.05, "summary": "Gold customers receive softer surge (-5%)."}
    # ...
    raise NotImplementedError
```

The recommendation service can then compose these agent outputs into a unified structure:

```python
def compute_all_factors(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Call each conceptual agent and normalize outputs into a single dict:
    {
      "environment": {"factor": 0.05, "summary": "..."},
      "supply_demand": {"factor": 0.10, "summary": "..."},
      "loyalty": {"factor": -0.05, "summary": "..."},
      "historical": {"factor": 0.0, "summary": "..."},
      "summaries": {
        "environment": "...",
        "supply_demand": "...",
        "loyalty": "...",
        "historical": "..."
      }
    }
    """
    raise NotImplementedError
```

---

### 3.4 LangChain Explanation Chain

Use a single chain that accepts request + factors and returns **explanation text only**.

```python
# orchestration/chains/pricing_explanation_chain.py
from typing import Any
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable


def build_pricing_explanation_chain(llm: BaseLanguageModel) -> Runnable:
    """
    Construct a simple chain that:
      - Takes 'request', 'factors', 'adjustment' as input.
      - Returns a BA-friendly explanation string.
    """
    # Pseudocode only; actual prompt & wiring implemented here in this milestone.
    #
    # template = ChatPromptTemplate.from_messages([
    #   ("system", "You are a pricing advisor for ride-hailing..."),
    #   ("human", "{request}\n{factors}\n{adjustment}\nExplain your recommendation..."),
    # ])
    # return template | llm | StrOutputParser()
    raise NotImplementedError
```

Guidelines:

- **Deterministic-ish**: Use concise, structured prompts to keep explanations stable across runs.
- **BA-friendly tone**: Avoid overly technical phrasing; emphasize trade-offs and fairness.
- **Traceability**: Ensure the prompt references each factor by name (environment, supply/demand, loyalty, historical).

---

### 3.5 Goodness Score and Explanation Alignment

Ensure the explanation references the **same trade-offs** the `goodness` metric encodes:

- If goodness is low because adjustment is aggressive:
  - Explanation should mention risk or fairness concerns.
- If goodness is high:
  - Explanation should mention balance between revenue and customer impact.

Example input to the chain (for reference only):

```json
{
  "request": {
    "zone": "airport_corridor",
    "scenario": "road_closure",
    "time": "2025-11-27T18:00:00Z",
    "loyalty_segment": "gold"
  },
  "factors": {
    "environment": "Road closure adds moderate travel time (+5%).",
    "supply_demand": "High demand vs limited drivers (+10%).",
    "loyalty": "Gold segment softens surge (-5%).",
    "historical": "Similar trips succeed around 1.05x."
  },
  "adjustment": {
    "recommended_adjustment": 0.1,
    "goodness": 0.78
  }
}
```

---

### 3.6 Definition of Done

- Orchestrator function exists and is used by FastAPI route.
- All four conceptual agents are implemented with simple, explainable heuristics.
- LangChain chain is wired to produce explanation text based on request + factors.
- `reasoning` field is non-empty and consistently references all four factors and the goodness score.
- The team has at least 2–3 **scripted scenarios** whose explanations are demo-ready.



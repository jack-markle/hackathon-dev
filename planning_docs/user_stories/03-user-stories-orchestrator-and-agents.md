### User Stories – Orchestrator, Agents, and LangChain (Milestone 3)

These stories focus on tying factor computation into conceptual agents and generating natural-language reasoning with LangChain, aligned with `03-orchestrator-and-agents-langchain.md`.

---

### Story C1 – Orchestrated Pricing Recommendation Flow

**As a** backend developer or AI lead  
**I want** a single orchestrator function to coordinate agents and explanation generation  
**So that** the FastAPI route has a clean, testable integration point.

**Acceptance Criteria**

- A function similar to the following exists and is used by the FastAPI route:

```python
from app.models.recommendation import RecommendationRequest, RecommendationResponse

def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    ...
```

- Orchestrator responsibilities:
  - Calls a “compute all factors” function (which delegates to conceptual agents).
  - Combines factors into a recommended adjustment and goodness.
  - Invokes a LangChain-based explanation chain.
  - Returns `RecommendationResponse` with `reasoning` populated.
- The API handler (`/api/v1/recommendation`) delegates to this orchestrator instead of embedding logic directly.

---

### Story C2 – Conceptual Agents with Clear Responsibilities

**As a** system designer  
**I want** the four conceptual agents (environment, supply/demand, loyalty, historical) represented as code units  
**So that** the architecture diagram maps cleanly to implementation.

**Acceptance Criteria**

- There are separate modules or functions for each conceptual agent, for example:
  - `environment_agent.evaluate_environment(context)`
  - `loyalty_agent.evaluate_loyalty(context)`
  - `supply_demand_agent.evaluate_supply_demand(context)`
  - `historical_agent.evaluate_historical(context)`
- Each agent:
  - Accepts a simple context dict (or strongly typed object) derived from `RecommendationRequest`.
  - Returns:
    - A numeric factor (or structure containing a factor).
    - A short human-readable summary string.
- A `compute_all_factors` helper aggregates agents’ outputs into a single normalized structure used by the orchestrator.

---

### Story C3 – LangChain Explanation Generation

**As a** pricing analyst  
**I want** a plain-language explanation of each recommendation  
**So that** I understand why the AI suggested that price and can defend it to stakeholders.

**Acceptance Criteria**

- A LangChain chain builder is implemented, e.g.:

```python
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable

def build_pricing_explanation_chain(llm: BaseLanguageModel) -> Runnable:
    ...
```

- The chain:
  - Accepts input including:
    - Request details (zone, scenario, time, loyalty_segment).
    - Factor summaries.
    - Recommended adjustment and goodness.
  - Returns a string explanation.
- The prompt design:
  - Refers explicitly to environment, supply/demand, loyalty, and historical factors.
  - Mentions trade-offs between revenue and fairness.
- The `reasoning` field in API responses is populated from the chain’s output.

---

### Story C4 – Alignment Between Goodness Metric and Explanation

**As a** stakeholder evaluating the prototype  
**I want** the explanation text and goodness score to tell a consistent story  
**So that** I can trust the system’s behavior and messaging.

**Acceptance Criteria**

- When goodness is low (e.g., < 0.6):
  - Explanations highlight risks, uncertainties, or fairness concerns.
- When goodness is high (e.g., ≥ 0.8):
  - Explanations emphasize balanced trade-offs and confidence in the recommendation.
- At least two scripted scenarios demonstrate:
  - A relatively low-goodness case with cautionary language.
  - A high-goodness case with reassuring language.
- The logic used to derive the goodness value is described in comments and informally mirrored in the explanation prompt.



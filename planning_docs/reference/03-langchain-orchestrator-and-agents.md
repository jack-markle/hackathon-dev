### LangChain, Orchestrator, and Agents – Reference

This document covers how we intend to use **LangChain** alongside our orchestrator and conceptual agents to produce explainable recommendations.

---

### 1. Role in Our Architecture

- LangChain is used to:
  - Turn numeric factors and summaries into **natural-language reasoning**.
  - Enforce a consistent **voice and structure** in explanations.
- The **orchestrator**:
  - Calls the factor-computing service / agents.
  - Invokes a LangChain **Runnable** (chain).
  - Returns a `RecommendationResponse` including `reasoning`.

---

### 2. Components Overview

Recommended layout:

```bash
orchestration/
  orchestrator.py                     # High-level flow
  agents/
    environment_agent.py
    loyalty_agent.py
    supply_demand_agent.py
    historical_agent.py
    corporate_pressure_agent.py
  chains/
    pricing_explanation_chain.py      # LangChain prompt + wiring
```

- **Agents**:
  - Simple Python functions that return numeric factor + short summary.
- **Chain**:
  - A LangChain pipeline from structured context → string explanation.

---

### 3. Agents: Implementation Notes

- Each agent takes a **simple context dictionary** (or typed object) and returns structured output:

```python
from typing import Dict, Any


def evaluate_environment(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns something like:
    {
      "factor": 0.05,
      "summary": "Road closure adds moderate travel time (+5%)."
    }
    """
    ...
```

- A helper like `compute_all_factors` aggregates:
  - All agent outputs.
  - A `summaries` dict to feed the explanation chain.

---

### 4. LangChain Explanation Chain

- Build a single-purpose chain for this project:

```python
from typing import Any
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import Runnable


def build_pricing_explanation_chain(llm: BaseLanguageModel) -> Runnable:
    """
    Returns a chain that:
      - Accepts {request, factors, adjustment}.
      - Produces a short, BA-friendly explanation string.
    """
    ...
```

- Prompt guidelines:
  - **System**: set role (“pricing advisor for ride-hailing”) and objectives (balance profit, fairness, loyalty, corporate goals).
  - **Human**: include:
    - Zone, scenario, time, loyalty segment.
    - Factor summaries by name (Environment, Supply/Demand, Loyalty, Historical, Corporate Pressure).
    - Recommended adjustment and goodness.
    - Instructions: “Explain in 3–6 sentences, in business language, referencing each factor.”

---

### 5. Orchestrator Flow

- High-level pseudocode:

```python
from app.models.recommendation import RecommendationRequest, RecommendationResponse


def orchestrate_pricing_recommendation(
    req: RecommendationRequest,
) -> RecommendationResponse:
    # 1. Compute numeric factors via agents/service.
    # 2. Combine into recommended_adjustment + goodness.
    # 3. Invoke LangChain explanation chain with structured context.
    # 4. Return a full RecommendationResponse.
    ...
```

- Keep orchestrator **stateless** and **deterministic** for the same input, aside from LLM variability in wording.

---

### 6. Best Practices for This Project

- Keep agents **simple and explainable**:
  - Use small lookup tables or rule-of-thumb heuristics.
- Make prompts **explicitly reference** the five conceptual agents (including corporate pressure) and the goodness score.
- Avoid over-engineering:
  - One orchestrator, one explanation chain is sufficient for the hackathon.
- Document any non-obvious heuristics in comments to keep reasoning auditable.

---

### 7. Example Cursor Rule Snippet (LangChain & Agents)

Example `.cursor/rules/langchain.mdc` content:

```text
When editing orchestration or LangChain code:
- Keep one primary orchestrator function that coordinates agents and the explanation chain.
- Implement agents as simple, deterministic functions that return {factor, summary}.
- Design the LangChain prompt to reference environment, supply/demand, loyalty, historical, corporate pressure factors, and the goodness score explicitly.
- Avoid adding new chains or agents unless they clearly support the five conceptual dimensions already defined.
```

Use this rule when prompting in `orchestration/` or related backend files.



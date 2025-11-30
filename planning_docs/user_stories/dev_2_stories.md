### Dev 2 Stories – Orchestrator, Agents, and LangChain

**Primary focus:** Implement the orchestrator, conceptual agents (including Corporate Pressure Determinator), and the LangChain explanation chain.

Related milestones: **01, 03, 06**.

---

### D2.1 – Orchestrator Entry Point

**As a** backend/API consumer  
**I want** a single orchestrator function that coordinates factor computation and explanation  
**So that** the FastAPI route can remain thin and testable.

**Scope for Dev 2**

- Implement `orchestrate_pricing_recommendation(req: RecommendationRequest) -> RecommendationResponse` in `orchestration/orchestrator.py`.
- Responsibilities:
  - Call Dev 1’s `build_recommendation` or `compute_all_factors`/`combine_factors` (depending on final split).
  - Invoke the LangChain explanation chain with:
    - Request details.
    - Factor summaries (including corporate pressure).
    - Adjustment and goodness.
  - Populate `reasoning` field in `RecommendationResponse`.

**Shared technical details**

- The FastAPI route should use:

```python
from orchestration.orchestrator import orchestrate_pricing_recommendation
```

to produce the final response.

---

### D2.2 – Conceptual Agents (Environment, Supply/Demand, Loyalty, Historical, Corporate Pressure)

**As a** system designer  
**I want** separate, named agents for each conceptual factor  
**So that** architecture diagrams match the code structure.

**Scope for Dev 2**

- Implement agent modules in `orchestration/agents/`:
  - `environment_agent.py`
  - `loyalty_agent.py`
  - `supply_demand_agent.py`
  - `historical_agent.py`
  - `corporate_pressure_agent.py`
- Each agent:
  - Accepts a context dict (derived from `RecommendationRequest`).
  - Returns `{ "factor": float, "summary": str }`.
- Implement `compute_all_factors(req: RecommendationRequest) -> Dict[str, Any]` that normalizes agents’ outputs into the shared structure described in Milestone 3.

**Shared technical details**

- Factor outputs from agents should be compatible with Dev 1’s combination logic; align on:
  - What `factor` means (e.g., +0.05 is +5%).
  - How summaries will be displayed in the UI and fed into LangChain.

---

### D2.3 – Corporate Pressure Determinator Tool

**As a** corporate stakeholder  
**I want** my revenue goals/strategy to influence pricing recommendations  
**So that** the system can suggest prices aligned with high-level business objectives.

**Scope for Dev 2**

- In `corporate_pressure_agent.py`, interpret:
  - `corporate_revenue_goal` (float or `None`).
  - `corporate_strategy_notes` (string or `None`).
- Behavior:
  - If no corporate inputs provided → factor defaults to 0 with a neutral summary.
  - If provided → factor nudges pricing upward/downward **within** limits defined by Dev 1’s guardrails.
  - Provide a clear summary, e.g., “Corporate target of +15% revenue nudges price upward within allowed guardrails.”

**Shared technical details**

- Corporate pressure is modeled as a **soft factor**:
  - Must not override emergency/ethical guardrails.
  - Any tension (e.g., corporate asking for +30% but capped at +20%) should:
    - Be visible via a `flag` or factor summary.
    - Be referenced by the explanation chain and, optionally, n8n alerts.

---

### D2.4 – LangChain Explanation Chain

**As a** pricing analyst  
**I want** a concise, BA-friendly explanation for each recommendation  
**So that** I can understand and communicate why that price was suggested.

**Scope for Dev 2**

- Implement `build_pricing_explanation_chain(llm: BaseLanguageModel) -> Runnable` in `orchestration/chains/pricing_explanation_chain.py`.
- Prompt design:
  - System message:
    - Role: pricing advisor.
    - Objective: balance profit, fairness, loyalty, and corporate revenue goals under constraints.
  - Human message:
    - Injects: request, factor summaries, recommended adjustment, goodness.
    - Explicitly mentions: environment, supply/demand, loyalty, historical, corporate pressure.
    - Requests 3–6 sentences of business-language reasoning.

**Shared technical details**

- Chain input keys (agreed with Dev 1/3):

```json
{
  "request": { ... },
  "factors": { ... },
  "adjustment": {
    "recommended_adjustment": 0.1,
    "goodness": 0.78
  }
}
```

- Chain output is a `string` assigned to `reasoning`.

---

### D2.5 – Explanations vs. Goodness & Corporate Pressure

**As a** sponsor  
**I want** explanations and goodness scores to tell the same story, including corporate pressures  
**So that** I can see how the AI is balancing competing goals.

**Scope for Dev 2**

- Ensure the explanation template:
  - Acknowledges when corporate pressure is pushing against guardrails.
  - Uses lower-confidence language when goodness is low.
  - Uses more confident, balanced language when goodness is high.
- Work with Dev 5 to:
  - Validate a couple of scenarios where:
    - Corporate goal is high but constrained by emergencies.
    - Corporate goal is modest and well-aligned with market conditions.



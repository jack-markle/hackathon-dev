### Dev 1 Stories – Backend Core Pricing Logic

**Primary focus:** Implement core factor computations and guardrails in the FastAPI backend so that `/api/v1/recommendation` returns coherent numeric outputs, including the new Corporate Pressure Determinator input.

Related milestones: **01, 02** (with coordination to 03).

---

### D1.1 – Implement Factor Functions (Environment, Supply/Demand, Loyalty, Historical, Corporate Pressure)

**As a** pricing analyst using the system  
**I want** the backend to compute numeric factors for each dimension of pricing  
**So that** the orchestrator and explanation layer can combine them into a clear recommendation.

**Scope for Dev 1**

- Implement in `backend/app/services/recommendation_service.py`:
  - `compute_environment_factor`
  - `compute_supply_demand_factor`
  - `compute_loyalty_factor`
  - `compute_historical_factor`
  - `compute_corporate_pressure_factor` (using `corporate_revenue_goal` and `corporate_strategy_notes`)
- Use simple, documented heuristics (lookups/rules), not complex models.

**Shared technical details**

- Input model (from `Milestone 1`):

```python
class RecommendationRequest(BaseModel):
    zone: str
    scenario: str
    time: str
    loyalty_segment: str | None = None
    notes: str | None = None
    corporate_revenue_goal: float | None = None
    corporate_strategy_notes: str | None = None
```

- Each `compute_*_factor` function returns a `float` representing its contribution as a percentage delta (e.g., `0.05` for +5%).

---

### D1.2 – Combine Factors and Compute Goodness

**As a** sponsor/AI lead  
**I want** a single numeric adjustment and a “goodness” score  
**So that** recommendations are easy to consume and compare.

**Scope for Dev 1**

- Implement `combine_factors(env, supply_demand, loyalty, historical, corporate_pressure)` to:
  - Produce `recommended_adjustment` (float).
  - Produce `goodness` (float in `[0.0, 1.0]`).
- Ensure:
  - Corporate pressure behaves as a **soft** influence.
  - Environment + supply/demand + ethical guardrails are **hard constraints**.

**Shared technical details**

- The combination output should at least include:

```python
{
  "recommended_adjustment": float,
  "goodness": float,
}
```

- Downstream orchestrator (Dev 2) will wrap this into `RecommendationResponse`.

---

### D1.3 – Guardrails Implementation (Emergencies, Loyalty, Corporate Pressure)

**As a** risk-conscious pricing owner  
**I want** guardrails that prevent unethical prices even when corporate pressure is high  
**So that** the system remains defensible.

**Scope for Dev 1**

- Implement `apply_guardrails(base_adjustment, scenario, loyalty_segment)` and, if helpful, a small helper for interpreting corporate pressure relative to guardrails.
- Behavior:
  - Emergency scenarios cap or zero out surge regardless of corporate pressure.
  - Loyal segments have softened surge.
  - If corporate pressure “wants” a higher price than guardrails allow:
    - Guardrails win; adjustment is capped.
    - Dev 2/3 will surface this tension via `flags` and explanation.

**Shared technical details**

- Guardrails should be applied **after** raw factors are combined but **before** returning `recommended_adjustment`.
- For at least one scenario, document:
  - Raw vs. guardrailed adjustment.

---

### D1.4 – Build Recommendation (Numeric Only)

**As a** consumer of the API from UI/orchestrator  
**I want** a simple function to get a full numeric recommendation from a request  
**So that** higher layers don’t need to know factor internals.

**Scope for Dev 1**

- Implement `build_recommendation(req: RecommendationRequest) -> RecommendationResponse` (temporarily with placeholder `reasoning` until Dev 2 wires LangChain).
- Populate:
  - `recommended_adjustment`
  - `goodness`
  - `factors` summaries for:
    - `environment`
    - `supply_demand`
    - `loyalty`
    - `historical`
    - `corporate_pressure`

**Shared technical details**

- Response shape (align with milestones):

```json
{
  "recommended_adjustment": 0.1,
  "goodness": 0.78,
  "factors": {
    "environment": "...",
    "supply_demand": "...",
    "loyalty": "...",
    "historical": "...",
    "corporate_pressure": "..."
  },
  "reasoning": "placeholder until LangChain integration"
}
```

---

### D1.5 – Lightweight Tests / Scenario Checks

**As a** team  
**I want** core numeric logic to be predictable  
**So that** demo scenarios behave consistently throughout the hackathon.

**Scope for Dev 1**

- Add a few small tests or scripts (even if just simple functions) to:
  - Verify factor outputs for distinct scenarios.
  - Verify guardrails behavior (especially for emergencies and high corporate pressure).
  - Verify `recommended_adjustment` and `goodness` ranges for 2–3 agreed scenarios.



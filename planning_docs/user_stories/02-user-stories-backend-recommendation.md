### User Stories – Backend Recommendation Logic (Milestone 2)

These stories describe how the backend should compute and expose pricing recommendations via FastAPI, aligned with `02-backend-recommendation-logic.md`.

---

### Story B1 – Compute a Combined Price Adjustment

**As a** pricing analyst  
**I want** the backend to compute a single recommended price adjustment from multiple factors  
**So that** I can quickly understand how prices should change in a given scenario.

**Acceptance Criteria**

- `POST /api/v1/recommendation` accepts the agreed request payload and returns:
  - `recommended_adjustment` as a numeric multiplier offset (e.g., `0.1` for +10%).
  - `goodness` between `0.0` and `1.0`.
  - A `factors` object with keys for `environment`, `supply_demand`, `loyalty`, and `historical`.
- The endpoint uses a dedicated service function such as:

```python
# Conceptual reference only – logic implemented elsewhere
from app.models.recommendation import RecommendationRequest, RecommendationResponse

def build_recommendation(req: RecommendationRequest) -> RecommendationResponse:
    ...
```

- Unit or smoke tests exist to verify that:
  - Outputs are structurally valid for several test scenarios.
  - `recommended_adjustment` and `goodness` are always present.

---

### Story B2 – Environment Factor Calculation

**As a** pricing analyst  
**I want** environmental conditions (storms, road closures, emergencies) to influence the recommended price  
**So that** adjustments reflect real-world constraints and fairness.

**Acceptance Criteria**

- A dedicated function (or agent) exists for environment, e.g.:

```python
def compute_environment_factor(req: RecommendationRequest) -> float:
    ...
```

- For at least the following scenario values:
  - `normal_day`
  - `storm`
  - `road_closure`
  - an “emergency” value (e.g., `natural_disaster`)
- The function returns **non-zero, explainable numeric factors** used in the combination logic.
- `factors["environment"]` in the response contains a short human-readable summary that matches the numeric behavior.

---

### Story B3 – Supply & Demand, Loyalty, and Historical Factors

**As a** data-minded stakeholder  
**I want** supply/demand, loyalty, and historical patterns to each contribute distinct factors  
**So that** the overall recommendation can be broken down and explained.

**Acceptance Criteria**

- There are functions (or equivalent) for:
  - `compute_supply_demand_factor`
  - `compute_loyalty_factor`
  - `compute_historical_factor`
- Each function:
  - Returns a numeric factor.
  - Has a documented heuristic (in comments) explaining the intent (e.g., loyalty softens surge, historical data nudges toward known-successful levels).
- The combined recommendation:
  - Incorporates all three factors.
  - Exposes summaries in `factors["supply_demand"]`, `factors["loyalty"]`, and `factors["historical"]`.

---

### Story B4 – Guardrails for Emergencies and Loyal Customers

**As a** risk-conscious pricing owner  
**I want** guardrails that limit surge in emergencies and treat loyal customers more favorably  
**So that** dynamic pricing remains fair and defensible.

**Acceptance Criteria**

- A guardrail function exists, e.g.:

```python
def apply_guardrails(
    base_adjustment: float,
    scenario: str,
    loyalty_segment: str | None,
) -> float:
    ...
```

- In emergency-like scenarios:
  - The final adjustment is capped or flattened according to documented rules.
- For high-loyalty segments (e.g., gold/platinum):
  - The effective adjustment is softened relative to standard segments.
- At least one example scenario is documented where:
  - Raw combined adjustment is more aggressive than the final return value after guardrails.

---

### Story B5 – Basic Goodness Metric

**As a** sponsor or AI lead  
**I want** a simple “goodness” score attached to each recommendation  
**So that** I can see how well the proposed price balances revenue and fairness.

**Acceptance Criteria**

- A goodness metric is computed alongside the recommended adjustment, exposed as:

```json
{
  "goodness": 0.78
}
```

- The computation is:
  - Documented in comments at a high level (e.g., weighted components).
  - Deterministic for the same inputs.
- Goodness stays within the range `[0.0, 1.0]`.
- Documentation describes (in plain language) what low, medium, and high goodness roughly indicate in terms of trade-offs.



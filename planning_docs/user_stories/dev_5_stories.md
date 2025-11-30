### Dev 5 Stories – Data, Scenarios, Testing, and Demo Prep

**Primary focus:** Curate mock data, define scripted scenarios (including corporate pressure), support light testing, and help shape the final demo narrative.

Related milestones: **02, 03, 04, 05, 06**.

---

### D5.1 – Mock Data and Historical/Hypothetical Scenarios

**As a** team  
**I want** simple, consistent mock data behind historical and scenario logic  
**So that** factor outputs and explanations are predictable for the demo.

**Scope for Dev 5**

- Create small, documented data structures (JSON/fixtures or Python constants) that represent:
  - Typical historical pricing outcomes for key zones/scenarios.
  - A few loyalty distributions (e.g., proportion of gold vs standard).
  - Example corporate revenue goals/strategies.
- Coordinate with Dev 1/2 on how these mocks plug into:
  - `compute_historical_factor`
  - Any historical/Chroma-like lookups.

**Shared technical details**

- Keep data:
  - Small, readable, and checked into the repo.
  - Clearly commented as “mock/demo” only.

---

### D5.2 – Scripted Demo Scenarios (Including Corporate Pressure)

**As a** presenter  
**I want** a few well-defined demo scenarios with expected behavior  
**So that** the team can rehearse and deliver a smooth story.

**Scope for Dev 5**

- Define 2–4 canonical scenarios such as:
  - Airport corridor + road closure + corporate push for extra revenue.
  - Downtown storm + driver shortage with no corporate pressure.
  - Holiday event with moderate corporate goal aligned with demand.
- For each:
  - Specify input payload (matching Dev 3’s form/Dev 1’s model).
  - Capture expected ranges for:
    - `recommended_adjustment`.
    - `goodness`.
  - Sketch an example explanation snippet (aligned with Dev 2’s prompt).

**Shared technical details**

- Store scenarios in a small JSON or markdown file under `planning_docs` so all devs can refer to the same source of truth.

---

### D5.3 – Cross-Cutting Testing & Sanity Checks

**As a** technical lead support  
**I want** light, cross-cutting tests to validate end-to-end behavior  
**So that** regressions are less likely during the hackathon crunch.

**Scope for Dev 5**

- Work with:
  - Dev 1/2 on a couple of backend smoke tests hitting `/api/v1/recommendation` with scripted scenarios.
  - Dev 3 on manual UI test cases:
    - Required fields.
    - Loading/error/empty states.
    - Corporate pressure fields affecting outputs sensibly.
  - Dev 4 on verifying that at least one scenario triggers an n8n alert.

**Shared technical details**

- Testing can be lightweight (even simple scripts or manual checklists) but should be:
  - Documented.
  - Repeatable by another teammate.

---

### D5.4 – Explanation and Goodness Review

**As a** narrative owner  
**I want** explanations that match numeric behavior and corporate constraints  
**So that** the story we tell to the sponsor is coherent.

**Scope for Dev 5**

- Review:
  - Example responses from the backend/console for scripted scenarios.
  - Ensure that:
    - Goodness values feel reasonable.
    - Explanations acknowledge corporate goals vs. guardrails when relevant.
    - Wording is business-friendly and concise.
- Propose prompt tweaks or factor tuning to Dev 1/2 as needed.

---

### D5.5 – Presentation and Demo Script

**As a** hackathon team  
**I want** a clear, time-bounded presentation script  
**So that** we can showcase the system effectively in 10–15 minutes.

**Scope for Dev 5**

- Draft:
  - Slide outline (problem, concept, architecture, demo scenarios, extension ideas).
  - Demo flow:
    - Which scenario to show first.
    - When to highlight corporate pressure vs. constraints.
    - When to show n8n alerts.
- Run at least one practice session with the team and adjust the script based on timing and clarity.



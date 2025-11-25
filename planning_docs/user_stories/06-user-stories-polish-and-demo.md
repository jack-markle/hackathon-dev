### User Stories – Polish, Testing, and Demo Preparation (Milestone 6)

These stories describe the final refinements, testing expectations, and demo preparation, aligned with `06-polish-testing-and-demo-prep.md`.

---

### Story P1 – Analyst-Friendly UX and Visual Polish

**As a** pricing analyst  
**I want** a clean, readable console UI  
**So that** I can focus on the scenario and recommendations without being distracted by rough edges.

**Acceptance Criteria**

- The console uses:
  - Clear section headings (e.g., “Scenario”, “Recommendation”, “Goodness Score”, “AI Reasoning”).
  - Consistent typography and spacing.
- Goodness scores are visually distinguished using color (e.g., green/amber/red) while maintaining accessibility (e.g., also using labels).
- The layout is tested on a typical laptop resolution and remains usable without horizontal scrolling.

---

### Story P2 – Coherent, Business-Friendly Explanations

**As a** business stakeholder  
**I want** explanations that sound like a pricing analyst, not a generic chatbot  
**So that** I can use them to discuss decisions with non-technical colleagues.

**Acceptance Criteria**

- The LangChain prompt is tuned so that explanations:
  - Use concise business language (3–6 sentences or an equivalent compact format).
  - Reference environment, supply/demand, loyalty, and historical factors explicitly.
  - Mention trade-offs between revenue, fairness, and loyalty where relevant.
- At least a couple of example explanations are captured in planning docs to illustrate the desired tone and structure.

---

### Story P3 – Scripted Demo Scenarios

**As a** presenter  
**I want** a small set of scripted scenarios with expected outcomes  
**So that** the live demo or recording runs smoothly and predictably.

**Acceptance Criteria**

- A short list (e.g., 2–3) of demo scenarios is defined, each with:
  - Input values:

```json
{
  "zone": "string",
  "scenario": "string",
  "time": "ISO-8601 string",
  "loyalty_segment": "string",
  "notes": "string"
}
```

  - Expected range for:
    - `recommended_adjustment` (e.g., around +10%).
    - `goodness` (e.g., between 0.6 and 0.8).
  - Example explanation snippet capturing the key narrative.
- These scenarios are easy to reproduce from the console UI with minimal typing.

---

### Story P4 – Basic Stability and Testing

**As a** technical lead  
**I want** light testing and manual verification in place  
**So that** the prototype behaves consistently during the hackathon.

**Acceptance Criteria**

- Backend:
  - Smoke tests (manual or automated) verify `/api/v1/recommendation` for all scripted demo scenarios.
  - Responses always contain all required fields.
- Frontend:
  - Manual tests confirm:
    - Form validation works for required fields.
    - Loading and error states behave correctly.
    - Results update when inputs change.
- n8n:
  - At least one scenario is confirmed to:
    - Trigger an alert.
    - Produce a visible log or message in n8n or its downstream sink.

---

### Story P5 – Presentation Narrative and Artifacts

**As a** hackathon team  
**I want** a concise narrative, slides, and a demo script  
**So that** we can clearly explain the problem, our solution, and how it maps to the sponsor’s brief.

**Acceptance Criteria**

- A lightweight slide deck covers:
  - Problem framing (why dynamic, explainable pricing is needed).
  - Concept and target user (internal pricing analyst).
  - Architecture: console → orchestrator → agents → n8n.
  - One or two demo scenarios.
- A demo script outlines:
  - Who speaks when.
  - Which scenarios will be shown.
  - Which UI sections or logs to highlight for each step.
- The team runs at least one practice session using the script, verifying timing and flow.



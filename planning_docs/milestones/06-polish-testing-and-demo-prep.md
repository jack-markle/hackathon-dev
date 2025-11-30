### Milestone 6 – Polish, Testing, and Demo Preparation

**Goal:** Refine UX, stabilize behavior, and prepare a compelling, repeatable demo and slide narrative for the hackathon presentation.

---

### 6.1 Outcomes

- UI polished enough for a non-technical pricing analyst to use comfortably.
- Explanations feel **intentional and coherent**, not random chatbot output.
- 2–3 **scripted demo scenarios** with:
  - Inputs.
  - Expected numeric adjustments and goodness ranges.
  - Example explanations.
- Basic testing and error handling in place.
- Slide content and demo script drafted.

---

### 6.2 UX and Visual Polish

Focus on:

- **Readability**:
  - Clear headings: “Scenario”, “Recommendation”, “Goodness Score”, “AI Reasoning”.
  - Sufficient spacing and consistent typography.
- **Color usage**:
  - Reserve strong colors (red/green) for goodness and alerts.
- **Responsiveness**:
  - Ensure layout works on typical laptop resolutions.

Example goodness display logic (conceptual):

```tsx
function goodnessColor(goodness: number): string {
  if (goodness >= 0.8) return "text-emerald-600";
  if (goodness >= 0.6) return "text-amber-600";
  return "text-rose-600";
}
```

> Implement this pattern (or similar) so the score visually communicates risk level.

---

### 6.3 Explanation Prompt Refinement

Iterate on the LangChain prompt so that explanations:

- Reference each factor by name.
- Explicitly mention:
  - Revenue considerations.
  - Fairness and loyalty impact.
  - Any guardrails applied (e.g., “Because this is an emergency, we capped the price.”).
  - How corporate revenue goals/strategy were considered but constrained by market physics and ethics where necessary.

Prompt guidelines:

- System message should define:
  - Role: “You are a pricing advisor for a ride-hailing company.”
  - Objectives: “Balance profit, fairness, loyalty, and corporate revenue goals without violating market or ethical constraints.”
- Human message should inject:
  - Scenario description (zone, time, scenario).
  - Summarized factors.
  - Adjustment and goodness.
  - A clear instruction: “Explain in 3–6 sentences, in business language.”

---

### 6.4 Scripted Demo Scenarios

Define 2–3 scenarios in a markdown table or JSON file for repeatability, e.g.:

```json
[
  {
    "name": "Airport corridor – road closure at rush hour",
    "request": {
      "zone": "airport_corridor",
      "scenario": "road_closure",
      "time": "2025-11-27T18:00:00Z",
      "loyalty_segment": "gold",
      "notes": "Partial freeway closure, evening commute."
    }
  },
  {
    "name": "Downtown – storm with driver shortage",
    "request": {
      "zone": "downtown",
      "scenario": "storm",
      "time": "2025-11-27T21:00:00Z",
      "loyalty_segment": "standard",
      "notes": "Heavy rain; short trips likely."
    }
  }
]
```

For each scenario, record:

- Approximate expected `recommended_adjustment`.
- Expected `goodness` range (e.g., 0.6–0.7).
- Example explanation snippet.

---

### 6.5 Light Testing and Stability

Where time allows:

- **Backend**:
  - Smoke tests for `/api/v1/recommendation` using the scripted scenarios.
  - Basic checks that factors and reasoning strings are always present.
- **Frontend**:
  - Manual verification that:
    - Required fields are validated.
    - Loading and error states appear correctly.
    - Results update when inputs change.
- **n8n**:
  - Run at least one scenario that triggers an alert and verify it appears in the workflow log.

---

### 6.6 Presentation and Storytelling

Prepare a simple narrative that mirrors the sponsor’s brief:

- **Problem framing**:
  - “Pricing is slow to react; competitors use the same raw data.”
- **Our solution**:
  - “An AI Pricing Monitor & Advisor for analysts – not riders.”
- **Architecture story**:
  - Console → Orchestrator → Agents → n8n alerts.
- **Live demo script**:
  - Walk through 1–2 scripted scenarios.
  - Point out:
    - Adjustment.
    - Goodness.
    - Explanation references to environment, supply/demand, loyalty, historical data.

---

### 6.7 Definition of Done

- Console looks and feels polished enough for a stakeholder demo.
- Explanations are consistently understandable and aligned with the numeric outputs.
- Scripted scenarios are documented and reproducible.
- Team has a basic slide deck and a 10–15 minute presentation flow defined.



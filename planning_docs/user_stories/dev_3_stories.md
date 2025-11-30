### Dev 3 Stories – Next.js Pricing Analyst Console

**Primary focus:** Implement the Pricing Analyst Console UI in Next.js, including corporate pressure inputs and rendering of all backend outputs.

Related milestones: **01, 04, 06**.

---

### D3.1 – Console Layout and Navigation

**As a** pricing analyst  
**I want** a clear console page with separate areas for input and results  
**So that** I can quickly understand and operate the tool.

**Scope for Dev 3**

- Implement the root page (`/`) as the Pricing Analyst Console:
  - Left (or top): scenario input form.
  - Right (or bottom): recommendation, goodness score, and AI reasoning.
- Use semantic HTML (e.g., `main`, `section`, `header`) and responsive layout that works on a typical laptop.

**Shared technical details**

- Page skeleton aligns with the example in Milestone 4:
  - `frontend/app/page.tsx` as a client component using React hooks.

---

### D3.2 – Scenario Form Including Corporate Pressure

**As a** pricing analyst  
**I want** to specify zone, scenario, notes, and corporate strategy inputs  
**So that** the AI can consider both market context and business goals.

**Scope for Dev 3**

- Implement controlled inputs for:
  - Zone (dropdown).
  - Scenario (dropdown).
  - Notes (textarea).
  - Corporate revenue goal (numeric input; may be optional).
  - Corporate strategy notes (textarea; optional).
- Group corporate fields under a “Corporate Strategy” subheading with helper text explaining their role.

**Shared technical details**

- Payload sent to backend should follow:

```json
{
  "zone": "airport_corridor",
  "scenario": "road_closure",
  "time": "<frontend-generated ISO 8601>",
  "loyalty_segment": "gold",
  "notes": "evening commute, partial freeway closure",
  "corporate_revenue_goal": 0.15,
  "corporate_strategy_notes": "End-of-quarter revenue push."
}
```

- Coordinate with Dev 1/2 to keep field names and types aligned with `RecommendationRequest`.

---

### D3.3 – Wiring to Backend API and Handling States

**As a** user of the console  
**I want** responsive feedback when I submit a scenario  
**So that** I know when the system is working, succeeded, or failed.

**Scope for Dev 3**

- Implement `handleSubmit` with `fetch("/api/recommendation", ...)` or a proxied API route.
- Manage state:
  - `loading`: disables button and shows “Analyzing...” cue.
  - `error`: banner or inline message.
  - `result`: typed as the response shape.
- Ensure the console:
  - Preserves form inputs on error.
  - Shows a helpful empty state before first submission.

**Shared technical details**

- Expected response shape:

```ts
type RecommendationResponse = {
  recommended_adjustment: number;
  goodness: number;
  factors: Record<string, string>;
  reasoning: string;
};
```

---

### D3.4 – Displaying Recommendation, Goodness, and Reasoning

**As a** pricing analyst  
**I want** a clear view of the proposed adjustment, its goodness, and the reasoning  
**So that** I can assess and explain the recommendation.

**Scope for Dev 3**

- Implement result cards:
  - **Recommendation**:
    - Show percentage adjustment and selected zone.
  - **Goodness Score**:
    - Show numeric score.
    - Color-code based on thresholds (green/amber/red).
  - **AI Reasoning**:
    - Show `result.reasoning` in a readable layout, preserving line breaks.
- Optionally surface factor summaries (e.g., list of environment, supply/demand, loyalty, historical, corporate pressure lines).

**Shared technical details**

- Coordinate with Dev 2 to ensure explanation text matches UI expectations (length, tone).
- Goodness thresholds should match those described in Milestone 4/6.

---

### D3.5 – Demo Readiness and Scripted Scenarios

**As a** presenter  
**I want** the console to make scripted scenarios easy to run  
**So that** the live demo or recording goes smoothly.

**Scope for Dev 3**

- Ensure:
  - Default values can be used or quickly adjusted to match documented scenarios (from Dev 5).
  - It’s easy to switch between a “normal” scenario and a “corporate pressure vs guardrails” scenario.
- Provide small UI hints that map to the story, e.g.:
  - “Try changing the corporate revenue goal to see how the recommendation changes (within guardrails).”



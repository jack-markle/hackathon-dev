### User Stories – Frontend Pricing Analyst Console (Milestone 4)

These stories define how the Pricing Analyst Console (Next.js) should behave from the analyst’s perspective, aligned with `04-frontend-pricing-analyst-console.md`.

---

### Story F1 – Submit a Pricing Scenario

**As a** pricing analyst  
**I want** to enter a zone, scenario, and optional notes into a simple console  
**So that** I can quickly explore “what-if” pricing situations.

**Acceptance Criteria**

- The root page (`/`) displays a clearly labeled form section (e.g., “Scenario”).
- Inputs include at least:
  - Zone / region dropdown (e.g., Downtown, Airport Corridor, Suburbs, Stadium District).
  - Scenario dropdown (e.g., Normal day, Concert, Storm, Road closure, Holiday).
  - Optional notes textarea.
- Default values are provided so that:
  - The analyst can submit a first request without changing any fields.
- The form has:
  - A submit button labeled something like “Analyze and Recommend”.
  - Basic validation (zone and scenario are required).

---

### Story F2 – View Recommended Adjustment and Goodness

**As a** pricing analyst  
**I want** to see the recommended adjustment and goodness score clearly presented  
**So that** I can quickly judge the AI’s proposal and its confidence.

**Acceptance Criteria**

- After submitting a valid scenario and receiving a response, the console shows:
  - A summary card with:
    - The percentage adjustment derived from `recommended_adjustment`.
    - Text tying the adjustment back to the selected zone.
  - A separate card or section for the `goodness` score.
- Goodness is:
  - Displayed as a numeric value.
  - Color-coded according to thresholds (e.g., green, amber, red).
- If the API returns an error (non-2xx status):
  - An error message is shown.
  - The user’s inputs remain intact for easy retry.

---

### Story F3 – See Factor Breakdown and AI Reasoning

**As a** pricing analyst  
**I want** a breakdown of how environment, supply/demand, loyalty, and historical data influenced the recommendation  
**So that** I can understand the explanation and share it with stakeholders.

**Acceptance Criteria**

- The console includes:
  - A clearly labeled panel such as “AI Reasoning”.
  - A structured area or section for the factor summaries (environment, supply/demand, loyalty, historical).
- The `reasoning` field from the backend is displayed as:
  - Readable paragraphs or bullet points.
  - With preserved line breaks (if any) for clarity (`whitespace-pre-line` or similar).
- The UI distinguishes between:
  - Brief factor summaries.
  - Full natural-language explanation.

---

### Story F4 – Loading, Error, and Empty States

**As a** user of the console  
**I want** clear loading and error feedback  
**So that** I am not confused when the system is working or when something goes wrong.

**Acceptance Criteria**

- While a request is in-flight:
  - The submit button is disabled and visually indicates loading (e.g., “Analyzing...”).
- On error:
  - An error banner or message is shown near the form or results area.
  - The message is concise and non-technical (e.g., “We couldn’t fetch a recommendation. Please try again.”).
- Before the first successful submission:
  - A subtle empty state message is shown (e.g., “Submit a scenario to see pricing recommendations here.”).

---

### Story F5 – Demo-Friendly Layout

**As a** hackathon presenter  
**I want** the console layout to clearly separate inputs and outputs  
**So that** it is easy to walk an audience through a scenario live or in a recording.

**Acceptance Criteria**

- The page layout uses a two-column or stacked design where:
  - Left (or top) column: scenario input form.
  - Right (or bottom) column: recommendation, goodness, and reasoning.
- Headings and labels are:
  - Descriptive and business-oriented (e.g., “Scenario”, “Recommendation”, “Goodness Score”, “AI Reasoning”).
- The console is usable on a typical laptop resolution without horizontal scrolling.



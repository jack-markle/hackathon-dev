### Milestone 4 – Frontend Pricing Analyst Console (Next.js)

**Goal:** Build a single-page internal console that lets a pricing analyst submit scenarios and view recommendations, goodness scores, and reasoning.

---

### 4.1 Outcomes

- A **single Next.js page** serving as the “Pricing Analyst Console”.
- Form elements:
  - Zone/region dropdown.
  - Scenario dropdown.
  - Optional notes field.
- Result display:
  - Recommended adjustment (formatted, e.g., “+10% in Airport Corridor – next 2 hours”).
  - Goodness score (with basic color-coding).
  - Reasoning box (separate, clearly labeled panel).
- Robust but simple error and loading states.

---

### 4.2 Page Layout (App Router)

Use a layout that cleanly separates **input** and **output**.

```tsx
// frontend/app/page.tsx
import { useState } from "react";

type RecommendationResponse = {
  recommended_adjustment: number;
  goodness: number;
  factors: Record<string, string>;
  reasoning: string;
};

export default function PricingAnalystConsolePage() {
  const [zone, setZone] = useState("airport_corridor");
  const [scenario, setScenario] = useState("normal_day");
  const [notes, setNotes] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RecommendationResponse | null>(null);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    // Implementation wired in this milestone (API call to backend).
    // Keep logic minimal and focused on calling the FastAPI endpoint.
  }

  return (
    <main className="min-h-screen flex flex-col items-center bg-slate-50">
      <section className="w-full max-w-4xl px-4 py-8 space-y-6">
        <header>
          <h1 className="text-3xl font-semibold">
            AI Pricing Monitor & Advisor
          </h1>
          <p className="text-gray-600 mt-2">
            Internal console for pricing analysts to explore “what-if”
            scenarios and review AI recommendations.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]">
          {/* Left: Scenario form */}
          <form
            onSubmit={handleSubmit}
            className="space-y-4 bg-white p-4 rounded-lg shadow-sm border"
          >
            {/* Inputs added in this milestone */}
          </form>

          {/* Right: Results */}
          <section className="space-y-4">
            {/* Result and reasoning panels implemented in this milestone */}
          </section>
        </div>
      </section>
    </main>
  );
}
```

> Implementation details (API calls, full JSX, styling) are completed in this milestone following this skeleton.

---

### 4.3 Form Fields and UX

Best practices:

- Use **controlled components** with `useState`.
- Provide **sensible defaults** (e.g., “Downtown” and “Normal day”) so a demo can start with a single click.
- Add small helper text under each field to remind the user of intent.

Example snippet for the zone and scenario selectors:

```tsx
<div className="space-y-1">
  <label className="text-sm font-medium">Zone / Region</label>
  <select
    className="w-full border rounded px-2 py-1 text-sm"
    value={zone}
    onChange={(e) => setZone(e.target.value)}
  >
    <option value="downtown">Downtown</option>
    <option value="airport_corridor">Airport Corridor</option>
    <option value="suburbs">Suburbs</option>
    <option value="stadium_district">Stadium District</option>
  </select>
  <p className="text-xs text-gray-500">
    Choose the primary zone you are evaluating.
  </p>
</div>
```

---

### 4.4 Calling the Backend API

Use the `fetch` API from the client side; keep it thin and resilient.

```tsx
async function handleSubmit(event: React.FormEvent) {
  event.preventDefault();
  setLoading(true);
  setError(null);

  try {
    const response = await fetch("/api/recommendation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        zone,
        scenario,
        time: new Date().toISOString(),
        loyalty_segment: "gold", // could later be another field
        notes,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch recommendation");
    }

    const data: RecommendationResponse = await response.json();
    setResult(data);
  } catch (err: any) {
    setError(err.message ?? "Unknown error");
    setResult(null);
  } finally {
    setLoading(false);
  }
}
```

> The `/api/recommendation` path can be a frontend proxy to the FastAPI backend (via Next.js API route or reverse proxy configuration).

---

### 4.5 Displaying Results and Reasoning

Present results in a way that is intuitive to a business analyst:

- Show adjustment as a **percentage** with a clear label.
- Color-code goodness:
  - >= 0.8: green.
  - 0.6–0.79: amber.
  - < 0.6: red.
- Reasoning box:
  - Title: “AI Reasoning”.
  - Show a brief paragraph or bullet summary from the LLM.

Example JSX snippet:

```tsx
{result && (
  <section className="space-y-3">
    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h2 className="text-lg font-semibold mb-2">Recommendation</h2>
      <p className="text-sm">
        <span className="font-medium">
          {Math.round(result.recommended_adjustment * 100)}%{" "}
        </span>
        price adjustment recommended for the selected zone.
      </p>
    </div>

    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h3 className="text-sm font-semibold mb-1">Goodness Score</h3>
      {/* Simple color-coded display based on result.goodness */}
    </div>

    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h3 className="text-sm font-semibold mb-2">AI Reasoning</h3>
      <p className="text-sm text-gray-700 whitespace-pre-line">
        {result.reasoning}
      </p>
    </div>
  </section>
)}
```

---

### 4.6 Error, Loading, and Empty States

- **Loading**:
  - Disable submit button.
  - Show a small spinner or “Analyzing...” label.
- **Error**:
  - Show a dismissible error banner.
  - Keep the user’s form input intact so they can retry.
- **Empty state**:
  - When no result yet, display a subtle prompt: “Submit a scenario to see recommendations.”

---

### 4.7 Definition of Done

- Pricing Analyst Console page exists and is reachable as the root page.
- Form collects zone, scenario, and notes and calls the backend endpoint.
- The page shows recommended adjustment, goodness score, and AI reasoning on success.
- Basic loading, error, and empty states implemented.
- At least 2–3 scripted demo scenarios documented and easy to reproduce from the UI.



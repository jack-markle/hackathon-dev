### Next.js Frontend – Reference

This document describes how we’ll use **Next.js (App Router)** to implement the Pricing Analyst Console, plus best practices and a Cursor rule example.

---

### 1. Role in Our Architecture

- Provides the **single-page internal console** for pricing analysts.
- Collects **scenario inputs** and calls the FastAPI backend.
- Displays:
  - Recommended adjustment.
  - Goodness score (with visual cues).
  - AI reasoning text and factor summaries.

---

### 2. Recommended Project Structure

Lightweight, app-router-based structure:

```bash
frontend/
  app/
    layout.tsx        # Global layout (styles, metadata)
    page.tsx          # Pricing Analyst Console
    api/
      recommendation/route.ts  # (Optional) proxy to FastAPI backend
  lib/
    api.ts            # fetch helpers (optional)
  styles/
    globals.css
```

We can either:

- Call FastAPI directly from the browser (backend URL configured), or
- Use a **Next.js API route** (`app/api/recommendation/route.ts`) as a proxy.

---

### 3. Implementation Notes & Patterns

- Use **functional components** with React hooks (`useState`, `useEffect`).
- Keep the console page as a **client component**:

```tsx
// frontend/app/page.tsx
"use client";

export default function PricingAnalystConsolePage() {
  // local state, handlers, and JSX
}
```

- Encapsulate API calls in a small helper if they grow:

```tsx
async function fetchRecommendation(payload: any) {
  const res = await fetch("/api/recommendation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to fetch recommendation");
  return res.json();
}
```

- Keep **loading, error, and empty states** explicit and obvious to the user.

---

### 4. UI / UX Best Practices for This Project

- Clear sections:
  - **Scenario** – form inputs.
  - **Recommendation** – adjustment summary.
  - **Goodness Score** – numeric + color-coded status.
  - **AI Reasoning** – explanation panel.
- Prefer **semantic HTML** (e.g., `main`, `section`, `header`, `h1`–`h3`).
- Use **controlled components** for inputs:
  - Makes it easier to wire to `fetchRecommendation`.
- Keep styling simple and consistent (Tailwind or utility classes are fine).
- Enforce minimal **validation** (required fields) without overcomplicating UX.

---

### 5. Example Cursor Rule Snippet (Next.js)

Example `.cursor/rules/nextjs.mdc` content:

```text
When editing Next.js frontend code:
- Use the App Router (files under frontend/app) and functional components.
- Treat the root page as the Pricing Analyst Console with clear sections: Scenario, Recommendation, Goodness Score, AI Reasoning.
- Keep API interaction in thin helpers using fetch and preserve the /recommendation payload/response contract.
- Handle loading, error, and empty states explicitly, without adding complex state management libraries.
```

Apply this rule when prompting in `frontend/` files to keep the console implementation aligned with our plan.



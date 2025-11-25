### n8n Workflows & Alerting – Reference

This document describes how we use **n8n** as a workflow engine for logging and alerting based on pricing recommendations.

---

### 1. Role in Our Architecture

- Receives **webhook events** from FastAPI when:
  - Goodness is below a threshold.
  - A scenario is flagged as high-risk (e.g., emergency, high surge).
- Evaluates simple conditions and:
  - Logs the event.
  - Sends an alert (e.g., email, Slack-like message, or another webhook).

---

### 2. Basic Workflow Shape

In n8n, we expect a workflow roughly like:

1. **Webhook Node**:
   - Method: `POST`.
   - Path: (e.g.) `/pricing-goodness-alert`.
   - Expects JSON body like:

```json
{
  "zone": "airport_corridor",
  "recommended_adjustment": 0.2,
  "goodness": 0.62,
  "flags": ["high_surge"],
  "scenario": "storm",
  "notes": "Storm tonight, limited drivers near airport."
}
```

2. **IF Node**:
   - Condition: `goodness < 0.7` **OR** `flags` contains `"emergency"` or `"high_surge"`.

3. **Action Node**:
   - Email, Slack, or other notification:
     - Subject/title: “Review AI pricing recommendation in {zone}”.
     - Body includes recommended adjustment, goodness, flags, and notes.

We store an exported JSON of this workflow under `infra/n8n/pricing_goodness_alert.json` as reference.

---

### 3. Backend Integration Pattern

- A small helper handles outbound calls to n8n:

```python
from typing import Any, Dict

import httpx


async def send_pricing_alert(payload: Dict[str, Any], webhook_url: str) -> None:
    """
    Fire-and-forget style POST to n8n's webhook endpoint.
    Errors are logged but do not break the main user flow.
    """
    ...
```

- Higher-level logic decides when to call it (e.g., `maybe_trigger_alert`).
- The **n8n URL** is configurable via environment (`N8N_WEBHOOK_URL`) and read in `config.py`.

---

### 4. Best Practices for This Project

- Keep n8n calls **non-blocking** for the user:
  - Use timeouts.
  - Catch and log errors without failing the API request.
- Use **structured payloads**:
  - Avoid sending free-form strings where structured fields are more useful (zone, scenario, flags, etc.).
- Don’t encode business rules only in n8n:
  - Critical guardrails (e.g., “no surge in emergencies”) should live in backend logic.
  - n8n focuses on **notification and logging**, not price computation.
- Document the workflow JSON and path so others can import it into n8n quickly.

---

### 5. Example Cursor Rule Snippet (n8n & Alerting)

Example `.cursor/rules/n8n.mdc` content:

```text
When editing n8n integration or alerting code:
- Keep the main pricing API path user-focused and non-blocking; n8n failures must not break recommendations.
- Send structured JSON payloads to the n8n webhook including zone, recommended_adjustment, goodness, flags, scenario, and notes.
- Reserve business-critical pricing rules for the backend; use n8n primarily for logging and notifications.
- Read the n8n webhook URL from configuration (e.g., N8N_WEBHOOK_URL) rather than hard-coding it.
```

Use this rule when prompting in `integrations/` or alert-related modules.



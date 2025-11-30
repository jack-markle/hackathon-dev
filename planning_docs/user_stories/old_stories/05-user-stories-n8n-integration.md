### User Stories – n8n Integration and Alerting (Milestone 5)

These stories cover how pricing recommendations should trigger n8n workflows for logging and alerts, aligned with `05-n8n-integration-and-alerting.md`.

---

### Story N1 – Alert on Low Goodness or High-Risk Conditions

**As a** pricing or risk manager  
**I want** to receive alerts when recommendations look risky or low-confidence  
**So that** I can review and override them before they impact customers.

**Acceptance Criteria**

- The backend evaluates alert conditions such as:
  - `goodness` below a configured threshold (e.g., `< 0.7`).
  - Presence of risk-related flags (e.g., `"emergency"`, `"high_surge"`).
- When an alert condition is met, the backend:
  - Constructs a payload including:

```json
{
  "zone": "string",
  "recommended_adjustment": 0.0,
  "goodness": 0.0,
  "flags": ["string"],
  "scenario": "string",
  "notes": "string | null"
}
```

  - Sends it to an n8n webhook endpoint.
- At least one n8n workflow exists that:
  - Receives the webhook.
  - Routes low-goodness or high-risk cases to an alert node (e.g., email or Slack-style message).

---

### Story N2 – Non-Blocking Alert Integration

**As a** system reliability owner  
**I want** n8n integration to be non-blocking for the main API call  
**So that** failures in alerting do not break the pricing console experience.

**Acceptance Criteria**

- Alert-sending is implemented via:
  - A dedicated helper (e.g., `send_pricing_alert`) that:
    - Uses reasonable timeouts.
    - Catches and logs errors without raising them back to the caller.
- From the Pricing Analyst Console’s perspective:
  - The recommendation response continues to work even if:
    - n8n is down.
    - The webhook times out.
- Basic logging exists (even if simple) to observe:
  - When alerts were attempted.
  - When they failed.

---

### Story N3 – Configurable n8n Webhook URL

**As a** DevOps or environment owner  
**I want** the n8n webhook URL to be configurable via environment variables  
**So that** the system can be pointed at different n8n instances without code changes.

**Acceptance Criteria**

- Backend settings include something like:

```python
class Settings:
    N8N_WEBHOOK_URL: str
```

- The value is sourced from:
  - Environment variables or `.env` file.
- If `N8N_WEBHOOK_URL` is empty or not configured:
  - The backend either:
    - Skips sending alerts and logs a warning, or
    - Uses a documented safe default behavior.
- Configuration expectations (how to set the URL) are documented in the planning or setup docs.

---

### Story N4 – Demonstrable Alert Scenario

**As a** hackathon judge or sponsor  
**I want** to see a concrete example where a risky recommendation triggers an automated alert  
**So that** I can understand how this pattern would work in production.

**Acceptance Criteria**

- At least one **scripted demo scenario** is documented where:
  - The combination of factors leads to:
    - A relatively aggressive adjustment, or
    - A lower goodness score.
  - The alert logic triggers and sends an event to n8n.
- During the demo:
  - The team can show:
    - The analyst console receiving the recommendation.
    - The corresponding alert entry or message within n8n (or downstream sink).



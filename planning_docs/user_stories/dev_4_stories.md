### Dev 4 Stories – n8n Integration and Backend Integrations

**Primary focus:** Implement n8n workflows and backend integration so that risky or low-goodness recommendations trigger appropriate alerts without blocking the user.

Related milestones: **01, 05, 06**.

---

### D4.1 – n8n Webhook Workflow

**As a** pricing/risk manager  
**I want** an automated alert when risky recommendations occur  
**So that** I can review them before they affect customers at scale.

**Scope for Dev 4**

- Build an n8n workflow that:
  - Starts with a Webhook node (method `POST`).
  - Evaluates `goodness` and `flags`.
  - Routes to an alert node (e.g., email or Slack-like notification) when conditions are met.
- Export the workflow as `infra/n8n/pricing_goodness_alert.json`.

**Shared technical details**

- Expected payload (from backend):

```json
{
  "zone": "airport_corridor",
  "recommended_adjustment": 0.2,
  "goodness": 0.62,
  "flags": ["high_surge", "corporate_overruled_by_guardrails"],
  "scenario": "storm",
  "notes": "Storm tonight, limited drivers near airport. Corporate requested +30% but guardrails capped at +20%."
}
```

- Conditions for alert:
  - `goodness < 0.7` OR
  - `flags` contains `"emergency"`, `"high_surge"`, or `"corporate_overruled_by_guardrails"`.

---

### D4.2 – Backend n8n Notifier Utility

**As a** backend maintainer  
**I want** a single utility for sending alerts to n8n  
**So that** pricing logic stays clean and the notification mechanism can evolve independently.

**Scope for Dev 4**

- Implement in `backend/app/integrations/n8n_notifier.py`:
  - `send_pricing_alert(payload: Dict[str, Any], webhook_url: str) -> None`
    - Uses `httpx` or similar.
    - Applies a reasonable timeout.
    - Catches and logs errors without raising.

**Shared technical details**

- Read `N8N_WEBHOOK_URL` from centralized settings, e.g.:

```python
class Settings:
    N8N_WEBHOOK_URL: str
```

- If `N8N_WEBHOOK_URL` is missing/empty, log and skip sending.

---

### D4.3 – Maybe-Trigger-Alert Hook in Orchestrator/Service

**As a** system designer  
**I want** alerts triggered only when necessary  
**So that** we avoid noisy notifications and keep the main flow fast.

**Scope for Dev 4**

- Implement a helper such as `maybe_trigger_alert(...)` that:
  - Accepts zone, adjustment, goodness, flags, scenario, notes.
  - Decides whether to call `send_pricing_alert`.
- Wire this helper into an appropriate place (e.g., orchestrator or recommendation service) after the final adjustment and flags are known.

**Shared technical details**

- Coordinate with Dev 1/2 to:
  - Agree on flag names (e.g., `"corporate_overruled_by_guardrails"`).
  - Ensure flags are included in the payload whenever relevant.

---

### D4.4 – Non-Blocking Integration and Observability

**As a** reliability-focused engineer  
**I want** n8n integration to be observable but not fragile  
**So that** we can see when alerts fail without impacting users.

**Scope for Dev 4**

- Ensure:
  - n8n timeouts do not surface as API errors.
  - Basic logs (console/file) record:
    - When alerts were attempted.
    - Success/failure and key fields (zone, flags).
- Optionally tag logs with environment (dev/hackathon) and scenario name if available.

---

### D4.5 – Demo Scenario for Alerts

**As a** presenter  
**I want** a clear demo where an alert is triggered  
**So that** the sponsor can see how the pattern works end to end.

**Scope for Dev 4**

- Work with Dev 3 and Dev 5 to:
  - Pick a scenario that:
    - Has high surge or low goodness.
    - And/or shows corporate pressure being constrained by guardrails.
  - Verify that:
    - The console shows the recommendation and reasoning.
    - The n8n workflow receives the webhook and produces a visible alert/log.



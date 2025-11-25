### Milestone 5 – n8n Integration and Alerting

**Goal:** Integrate the backend with an n8n workflow to log key events and send alerts when goodness drops below a threshold or risk flags are present.

---

### 5.1 Outcomes

- An **n8n workflow** (JSON export in `infra/n8n`) that:
  - Exposes a webhook endpoint.
  - Evaluates `goodness` and risk flags.
  - Sends a simple alert (e.g., email, Slack-style message, or log).
- FastAPI backend posts to the n8n webhook whenever:
  - `goodness < threshold` (e.g., `< 0.7`), or
  - Certain flags are set (e.g., emergency scenario, high surge).

---

### 5.2 n8n Workflow Shape

At a high level, the workflow should look like:

- **Webhook node** – receives:
  - `zone`
  - `recommended_adjustment`
  - `goodness`
  - optional `flags` (e.g., `["emergency", "high_surge"]`)
- **IF node** – checks conditions:
  - `goodness < 0.7`
  - OR `"emergency" in flags`
  - OR `"high_surge" in flags`
- **Action node** – for alerting:
  - Email node, Slack node, or simply a log/HTTP call for the demo.

Example payload expected by the webhook:

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

Store the exported workflow JSON as:

- `infra/n8n/pricing_goodness_alert.json`

---

### 5.3 Backend → n8n Integration

Create a small notifier utility that is called from the orchestrator or service layer when an alert condition is met.

```python
# backend/app/integrations/n8n_notifier.py
from typing import Any, Dict

import httpx


async def send_pricing_alert(payload: Dict[str, Any], webhook_url: str) -> None:
  """
  Non-blocking call to n8n webhook for logging/alerting.
  Errors should be logged but must not break the main flow.
  """
  # Implementation in this milestone: simple POST with timeout & error logging.
  raise NotImplementedError
```

Example usage (inside orchestrator or recommendation service):

```python
async def maybe_trigger_alert(
    zone: str,
    adjustment: float,
    goodness: float,
    flags: list[str],
    scenario: str,
    notes: str | None,
) -> None:
    """
    Check alert conditions and POST to n8n webhook if needed.
    """
    # Pseudocode:
    # if goodness < 0.7 or "emergency" in flags or "high_surge" in flags:
    #     await send_pricing_alert(
    #         {
    #             "zone": zone,
    #             "recommended_adjustment": adjustment,
    #             "goodness": goodness,
    #             "flags": flags,
    #             "scenario": scenario,
    #             "notes": notes,
    #         },
    #         webhook_url=settings.N8N_WEBHOOK_URL,
    #     )
    raise NotImplementedError
```

Make sure any `await` calls to n8n are:

- **Low impact**: Use timeouts and swallow/log failures.
- **Non-blocking** for the user’s experience.

---

### 5.4 Configuration and Secrets

Add n8n configuration to backend settings:

- `N8N_WEBHOOK_URL` (environment variable).

Example (in `config.py`):

```python
import os


class Settings:
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "")


settings = Settings()
```

> For the hackathon, it is acceptable to load this from `.env` or direct environment variables and document expected values.

---

### 5.5 Demo Flow

Script a scenario that intentionally generates a **low goodness** score or **high surge**, so:

- The analyst runs the scenario in the console.
- The backend returns a visible recommendation and explanation.
- n8n receives the webhook and:
  - Sends an email/Slack-like message, **or**
  - Logs an event that can be shown in the n8n UI.

This gives a clear narrative:

> “When our AI proposes a risky price, we don’t just apply it blindly – we raise an alert for human review.”

---

### 5.6 Definition of Done

- n8n workflow exists and is imported and runnable in an n8n instance.
- Backend can post alerts to n8n webhook without impacting the main request/response path.
- At least one scripted scenario demonstrably triggers an alert.
- The alert is viewable in the n8n UI or in a downstream sink (email, Slack, log).



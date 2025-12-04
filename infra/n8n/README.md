# n8n Pricing Goodness Alert Workflow

## Overview

This workflow automatically sends email alerts when pricing recommendations meet risk criteria, helping pricing and risk managers review potentially problematic recommendations before they affect customers at scale.

## Workflow File

- **Location:** `infra/n8n/pricing_goodness_alert.json`
- **Workflow Name:** `pricing_goodness_alert`

## Workflow Structure

```
Webhook (POST) → Check Alert Conditions (IF) → Send Alert Email (Gmail)
                                             → No Alert Needed (NoOp)
```

## Nodes

### 1. Webhook Node
- **Type:** `n8n-nodes-base.webhook`
- **Method:** POST
- **Purpose:** Receives pricing recommendation payloads from the FastAPI backend

### 2. Check Alert Conditions (IF Node)
- **Type:** `n8n-nodes-base.if`
- **Logic:** OR combinator
- **Conditions:**
  - `goodness < 0.7` (below 70% threshold)
  - `flags` contains `"emergency"`
  - `flags` contains `"high_surge"`
  - `flags` contains `"corporate_overruled_by_guardrails"`

### 3. Send Alert Email (Gmail Node)
- **Type:** `n8n-nodes-base.gmail`
- **Triggered when:** Any alert condition is met (true branch)
- **Recipient:** tmluongx@gmail.com
- **Subject:** `🚨 Pricing Alert: Review recommendation for {origin_zone} → {destination_zone}`

### 4. No Alert Needed (NoOp Node)
- **Type:** `n8n-nodes-base.noOp`
- **Triggered when:** No alert conditions are met (false branch)

## Expected Payload Format

The webhook expects a JSON payload with the following structure:

```json
{
  "origin_zone": "downtown",
  "destination_zone": "airport_corridor",
  "recommended_adjustment": 0.2,
  "goodness": 0.62,
  "flags": ["high_surge", "corporate_overruled_by_guardrails"],
  "scenarios": ["storm", "road_closure"],
  "scenario": "storm",
  "time": "2024-01-15T14:30:00.000Z",
  "loyalty_segment": "gold",
  "notes": "Storm expected to reduce driver availability by 40%.",
  "corporate_revenue_goal": 0.03,
  "corporate_strategy_notes": "Q4 revenue push"
}
```

### Field Descriptions

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `origin_zone` | string | Starting zone | "downtown", "airport_corridor", "suburbs", "stadium_district" |
| `destination_zone` | string | Ending zone | Same options as origin_zone |
| `scenarios` | array | Multiple selected scenarios | ["storm", "road_closure", "concert", "holiday"] |
| `scenario` | string | Primary scenario (backward compatibility) | "storm", "normal_day", etc. |
| `time` | string | ISO 8601 timestamp | "2024-01-15T14:30:00.000Z" |
| `loyalty_segment` | string | Customer tier | "gold", "silver", "bronze" |
| `notes` | string | Additional analyst context | Free text |
| `corporate_revenue_goal` | number | Revenue target as decimal | 0.03 (3%), 0.15 (15%) |
| `corporate_strategy_notes` | string | Corporate strategy context | "Q4 revenue push" |
| `recommended_adjustment` | number | Price adjustment as decimal | 0.2 (20%), -0.1 (-10%) |
| `goodness` | number | Quality score [0.0-1.0] | 0.62 (62%) |
| `flags` | array | Risk flags | ["emergency", "high_surge", "corporate_overruled_by_guardrails"] |

## Email Alert Content

The email includes:

1. **Route Information:** Origin → Destination zones
2. **Scenario Details:** Primary scenario and all selected scenarios
3. **Timing:** ISO timestamp of the recommendation
4. **Customer Context:** Loyalty segment
5. **Pricing Metrics:** Recommended adjustment % and goodness score %
6. **Corporate Pressure:** Revenue goal % and strategy notes
7. **Risk Flags:** List of all risk flags
8. **Analyst Notes:** Additional context provided by the analyst
9. **Alert Triggers:** Specific reasons why the alert was triggered

### Sample Email

```
🚨 Pricing Alert: Review recommendation for downtown → airport_corridor

Pricing Goodness Alert

---

Route: downtown → airport_corridor
Primary Scenario: storm
All Scenarios: storm, road_closure
Time: 2024-01-15T14:30:00.000Z
Loyalty Segment: gold
Recommended Adjustment: 20.0%
Goodness Score: 62.0%

---

Corporate Pressure:
• Revenue Goal: 3.0%
• Strategy Notes: Q4 revenue push

---

Risk Flags:
• high_surge
• corporate_overruled_by_guardrails

---

Analyst Notes:
Storm expected to reduce driver availability by 40%.

---

⚠️ This alert was triggered because:
• Goodness score is below 70% threshold.
• High surge pricing detected
• Corporate pressure was overruled by guardrails

Please review this recommendation before it affects customers at scale.
```

## Setup Instructions

### 1. Import the Workflow

1. Open your n8n instance
2. Navigate to **Workflows** → **Add workflow** → **Import from File**
3. Select `infra/n8n/pricing_goodness_alert.json`
4. Click **Import**

### 2. Configure Gmail Credentials

1. Click on the **Send Alert Email** node
2. Under **Credentials**, click **Create New**
3. Select **Gmail OAuth2**
4. Follow the authentication flow
5. Grant necessary permissions

### 3. Update Email Recipient

1. In the **Send Alert Email** node
2. Update the `sendTo` parameter with your email address
3. Optionally update `senderName` (currently "RideFlow")

### 4. Activate the Workflow

1. Click the toggle switch at the top to activate
2. Copy the webhook URL from the **Webhook** node
3. Configure your backend with this URL as `N8N_WEBHOOK_URL`

## Backend Integration

The FastAPI backend should POST to the webhook URL when alert conditions are met:

```python
# backend/app/integrations/n8n_notifier.py
import httpx
from typing import Dict, Any

async def send_pricing_alert(payload: Dict[str, Any], webhook_url: str) -> None:
    """
    Send pricing alert to n8n webhook.
    Non-blocking, logs errors without raising.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(webhook_url, json=payload)
    except Exception as e:
        print(f"Failed to send n8n alert: {e}")
```

## Testing

### Test Payload (High Risk - Should Trigger Alert)

```json
{
  "origin_zone": "downtown",
  "destination_zone": "airport_corridor",
  "recommended_adjustment": 0.2,
  "goodness": 0.62,
  "flags": ["high_surge", "corporate_overruled_by_guardrails"],
  "scenarios": ["storm", "road_closure"],
  "scenario": "storm",
  "time": "2024-01-15T14:30:00.000Z",
  "loyalty_segment": "gold",
  "notes": "Storm expected to reduce driver availability by 40%.",
  "corporate_revenue_goal": 0.03,
  "corporate_strategy_notes": "Q4 revenue push"
}
```

### Test Payload (Normal - Should NOT Trigger Alert)

```json
{
  "origin_zone": "suburbs",
  "destination_zone": "downtown",
  "recommended_adjustment": 0.05,
  "goodness": 0.85,
  "flags": [],
  "scenarios": ["normal_day"],
  "scenario": "normal_day",
  "time": "2024-01-15T10:00:00.000Z",
  "loyalty_segment": "silver",
  "notes": "Regular morning commute",
  "corporate_revenue_goal": 0.02,
  "corporate_strategy_notes": "Standard pricing"
}
```

## Best Practices

1. **Non-Blocking:** Backend should not wait for n8n response or fail if webhook is down
2. **Timeout:** Use reasonable timeout (5 seconds recommended)
3. **Error Handling:** Log errors but don't raise exceptions
4. **Structured Data:** Always send complete JSON payload with all fields
5. **Security:** Keep webhook URL private, consider adding authentication if needed

## Troubleshooting

### Alerts Not Received

1. Check workflow is **Active** in n8n
2. Verify Gmail credentials are valid
3. Check spam/junk folder
4. Review n8n execution logs

### Wrong Data in Email

1. Verify payload structure matches expected format
2. Check pinData in JSON for reference
3. Test with sample payloads first

### Performance Issues

1. Ensure backend uses async/non-blocking calls
2. Set appropriate timeouts
3. Consider rate limiting if sending many alerts

## Maintenance

- **Webhook URL:** Should be configured in backend via environment variable
- **Email Recipients:** Update in the workflow node as team changes
- **Alert Thresholds:** Modify IF node conditions as business rules evolve
- **Email Template:** Update message content in Send Alert Email node

---

**Version:** 1.0  
**Last Updated:** December 3, 2025  
**Maintained By:** RideFlow Engineering Team


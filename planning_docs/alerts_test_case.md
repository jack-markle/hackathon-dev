# n8n Alert Test Case and Validation Steps

Test case for validating n8n webhook integration and alert delivery when pricing recommendations trigger alert conditions.

## Alert Trigger Conditions

The system should trigger n8n alerts when:

1. **Low Goodness Score**: `goodness < 0.60` (pricing recommendation has low confidence/balance)
2. **High Adjustment**: `recommended_adjustment > 0.25` (25%+ price increase)
3. **Guardrail Applied**: Emergency guardrails override corporate pressure
4. **Corporate Tension**: High corporate pressure conflicts with market conditions

---

## Test Setup

### Prerequisites
- [ ] Backend API is running on `http://localhost:8000`
- [ ] n8n workflow is configured and active
- [ ] n8n webhook endpoint is accessible from backend
- [ ] Alert delivery channel is configured (email, Slack, etc.)

### n8n Webhook Configuration
- **Webhook URL**: `http://localhost:5678/webhook/pricing-alert` (example)
- **HTTP Method**: POST
- **Authentication**: (if required)

---

## Test Case 1: Low Goodness Score Alert

### Objective
Verify that alerts are triggered when goodness score falls below 0.60.

### Test Steps

1. **Prepare Test Payload**
   ```json
   {
     "zone": "suburbs",
     "scenario": "normal",
     "time": "2025-12-02T14:00:00Z",
     "loyalty_segment": "standard",
     "corporate_revenue_goal": 0.25,
     "corporate_strategy_notes": "Aggressive revenue targets for Q4"
   }
   ```

2. **Send API Request**
   ```bash
   curl -X POST http://localhost:8000/api/v1/recommendation \
     -H "Content-Type: application/json" \
     -d '{
       "zone": "suburbs",
       "scenario": "normal",
       "time": "2025-12-02T14:00:00Z",
       "loyalty_segment": "standard",
       "corporate_revenue_goal": 0.25,
       "corporate_strategy_notes": "Aggressive revenue targets for Q4"
     }'
   ```

3. **Verify API Response**
   - Check that `goodness < 0.60` in response
   - Note the `recommended_adjustment` value

4. **Check n8n Webhook**
   - Verify webhook was called (check n8n execution logs)
   - Verify webhook received correct payload

5. **Verify Alert Delivery**
   - Check alert delivery channel (email inbox, Slack channel, etc.)
   - Verify alert contains expected information

### Expected Alert Payload (to n8n)
```json
{
  "alert_type": "low_goodness",
  "goodness_score": 0.55,
  "recommended_adjustment": 0.12,
  "zone": "suburbs",
  "scenario": "normal",
  "timestamp": "2025-12-02T14:00:00Z",
  "reason": "Corporate revenue goals conflict with fair-pricing during low-demand period",
  "factors": {
    "environment": "...",
    "supply_demand": "...",
    "loyalty": "...",
    "historical": "...",
    "corporate_pressure": "..."
  }
}
```

### Expected Alert Content
- **Subject/Title**: "Low Goodness Alert: Pricing Recommendation Needs Review"
- **Body**: Should include goodness score, adjustment, zone, scenario, and reason
- **Priority**: Medium (or as configured)

### Validation Checklist
- [ ] API response shows `goodness < 0.60`
- [ ] n8n webhook was triggered
- [ ] Webhook payload matches expected structure
- [ ] Alert was delivered to configured channel
- [ ] Alert content is accurate and actionable

---

## Test Case 2: High Adjustment Alert

### Objective
Verify that alerts are triggered when recommended adjustment exceeds 25%.

### Test Steps

1. **Prepare Test Payload**
   ```json
   {
     "zone": "stadium",
     "scenario": "concert",
     "time": "2025-12-06T21:00:00Z",
     "loyalty_segment": "standard",
     "corporate_revenue_goal": 0.20
   }
   ```

2. **Send API Request**
   ```bash
   curl -X POST http://localhost:8000/api/v1/recommendation \
     -H "Content-Type: application/json" \
     -d '{
       "zone": "stadium",
       "scenario": "concert",
       "time": "2025-12-06T21:00:00Z",
       "loyalty_segment": "standard",
       "corporate_revenue_goal": 0.20
     }'
   ```

3. **Verify API Response**
   - Check that `recommended_adjustment > 0.25` in response
   - Note the `goodness` value

4. **Check n8n Webhook**
   - Verify webhook was called
   - Verify webhook received correct payload

5. **Verify Alert Delivery**
   - Check alert delivery channel
   - Verify alert contains expected information

### Expected Alert Payload (to n8n)
```json
{
  "alert_type": "high_adjustment",
  "goodness_score": 0.72,
  "recommended_adjustment": 0.28,
  "zone": "stadium",
  "scenario": "concert",
  "timestamp": "2025-12-06T21:00:00Z",
  "reason": "High price adjustment recommended - review for market competitiveness",
  "factors": {
    "environment": "...",
    "supply_demand": "...",
    "loyalty": "...",
    "historical": "...",
    "corporate_pressure": "..."
  }
}
```

### Expected Alert Content
- **Subject/Title**: "High Adjustment Alert: 28% Price Increase Recommended"
- **Body**: Should include adjustment percentage, zone, scenario, and market justification
- **Priority**: High (or as configured)

### Validation Checklist
- [ ] API response shows `recommended_adjustment > 0.25`
- [ ] n8n webhook was triggered
- [ ] Webhook payload matches expected structure
- [ ] Alert was delivered to configured channel
- [ ] Alert content is accurate and actionable

---

## Test Case 3: Emergency Guardrail Alert

### Objective
Verify that alerts are triggered when emergency guardrails override corporate pressure.

### Test Steps

1. **Prepare Test Payload**
   ```json
   {
     "zone": "downtown",
     "scenario": "emergency",
     "time": "2025-12-03T14:00:00Z",
     "loyalty_segment": "standard",
     "corporate_revenue_goal": 0.25,
     "corporate_strategy_notes": "Aggressive revenue push - but should be overridden"
   }
   ```

2. **Send API Request**
   ```bash
   curl -X POST http://localhost:8000/api/v1/recommendation \
     -H "Content-Type: application/json" \
     -d '{
       "zone": "downtown",
       "scenario": "emergency",
       "time": "2025-12-03T14:00:00Z",
       "loyalty_segment": "standard",
       "corporate_revenue_goal": 0.25,
       "corporate_strategy_notes": "Aggressive revenue push - but should be overridden"
     }'
   ```

3. **Verify API Response**
   - Check that `recommended_adjustment == 0.0` (emergency override)
   - Check that `guardrails` factor is present
   - Note the `goodness` value (should be high)

4. **Check n8n Webhook**
   - Verify webhook was called
   - Verify webhook received correct payload with guardrail information

5. **Verify Alert Delivery**
   - Check alert delivery channel
   - Verify alert emphasizes ethical override

### Expected Alert Payload (to n8n)
```json
{
  "alert_type": "guardrail_applied",
  "goodness_score": 0.90,
  "recommended_adjustment": 0.0,
  "zone": "downtown",
  "scenario": "emergency",
  "timestamp": "2025-12-03T14:00:00Z",
  "reason": "Emergency guardrails applied - surge pricing blocked despite corporate pressure",
  "guardrail_type": "emergency",
  "corporate_pressure_overridden": true,
  "factors": {
    "environment": "Emergency situation detected - applying ethical guardrails (no surge)",
    "supply_demand": "...",
    "loyalty": "...",
    "historical": "...",
    "corporate_pressure": "...",
    "guardrails": "EMERGENCY_GUARDRAIL: Surge pricing blocked due to emergency situation"
  }
}
```

### Expected Alert Content
- **Subject/Title**: "Guardrail Alert: Emergency Override Applied"
- **Body**: Should emphasize ethical pricing override and corporate pressure conflict
- **Priority**: High (ethical compliance)

### Validation Checklist
- [ ] API response shows `recommended_adjustment == 0.0`
- [ ] Guardrails factor is present in response
- [ ] n8n webhook was triggered
- [ ] Webhook payload indicates guardrail override
- [ ] Alert was delivered to configured channel
- [ ] Alert emphasizes ethical compliance

---

## Test Case 4: Corporate Tension Alert

### Objective
Verify that alerts are triggered when corporate pressure conflicts with market conditions.

### Test Steps

1. **Prepare Test Payload**
   ```json
   {
     "zone": "suburbs",
     "scenario": "normal",
     "time": "2025-12-02T14:00:00Z",
     "loyalty_segment": "standard",
     "corporate_revenue_goal": 0.25,
     "corporate_strategy_notes": "High revenue pressure without market justification"
   }
   ```

2. **Send API Request**
   ```bash
   curl -X POST http://localhost:8000/api/v1/recommendation \
     -H "Content-Type: application/json" \
     -d '{
       "zone": "suburbs",
       "scenario": "normal",
       "time": "2025-12-02T14:00:00Z",
       "loyalty_segment": "standard",
       "corporate_revenue_goal": 0.25,
       "corporate_strategy_notes": "High revenue pressure without market justification"
     }'
   ```

3. **Verify API Response**
   - Check that `goodness < 0.70` (tension between corporate and market)
   - Check factors for tension indicators
   - Note the `recommended_adjustment` value

4. **Check n8n Webhook**
   - Verify webhook was called
   - Verify webhook received correct payload

5. **Verify Alert Delivery**
   - Check alert delivery channel
   - Verify alert highlights tension

### Expected Alert Payload (to n8n)
```json
{
  "alert_type": "corporate_tension",
  "goodness_score": 0.65,
  "recommended_adjustment": 0.08,
  "zone": "suburbs",
  "scenario": "normal",
  "timestamp": "2025-12-02T14:00:00Z",
  "reason": "Corporate revenue goals conflict with fair-pricing during low-demand period",
  "corporate_goal": 0.25,
  "market_support": 0.02,
  "factors": {
    "environment": "...",
    "supply_demand": "...",
    "loyalty": "...",
    "historical": "...",
    "corporate_pressure": "..."
  }
}
```

### Expected Alert Content
- **Subject/Title**: "Corporate Tension Alert: Revenue Goals vs Market Reality"
- **Body**: Should highlight conflict between corporate pressure and market conditions
- **Priority**: Medium

### Validation Checklist
- [ ] API response shows tension indicators
- [ ] Goodness score reflects tension
- [ ] n8n webhook was triggered
- [ ] Webhook payload indicates corporate tension
- [ ] Alert was delivered to configured channel
- [ ] Alert highlights the conflict

---

## Integration Validation

### Backend Integration Check
- [ ] `app/integrations/n8n_notifier.py` is implemented
- [ ] Notifier is called after recommendation generation
- [ ] Alert conditions are correctly evaluated
- [ ] Webhook payload is correctly formatted

### n8n Workflow Check
- [ ] Webhook trigger is configured correctly
- [ ] Workflow processes alert payload
- [ ] Alert formatting is correct
- [ ] Delivery channel is configured
- [ ] Error handling is in place

### End-to-End Validation
- [ ] Complete flow: API → Backend → n8n → Alert Delivery
- [ ] All alert types are tested
- [ ] Alert content is accurate
- [ ] No duplicate alerts are sent
- [ ] Alert rate limiting works (if implemented)

---

## Test Results Summary

**Tester Name:** ________________  
**Date:** ________________  
**n8n Version:** ________________  
**Backend Version:** ________________  

**Test Case 1 (Low Goodness):** [ ] Pass [ ] Fail  
**Test Case 2 (High Adjustment):** [ ] Pass [ ] Fail  
**Test Case 3 (Emergency Guardrail):** [ ] Pass [ ] Fail  
**Test Case 4 (Corporate Tension):** [ ] Pass [ ] Fail  

**Issues Found:**
1. 
2. 
3. 

**Notes:**
_Add any additional observations or issues here_


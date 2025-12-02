# Explanation Review Template

Template for reviewing explanation quality per scenario. Use this to ensure explanations align with corporate strategy, business logic, and provide clear, actionable insights.

---

## Scenario Information

**Scenario ID:** ________________  
**Scenario Name:** ________________  
**Review Date:** ________________  
**Reviewer:** ________________  

---

## Input/Output Data

### Request Payload
```json
{
  "zone": "",
  "scenario": "",
  "time": "",
  "loyalty_segment": "",
  "notes": "",
  "corporate_revenue_goal": null,
  "corporate_strategy_notes": ""
}
```

### Response Output
```json
{
  "recommended_adjustment": 0.0,
  "goodness": 0.0,
  "factors": {
    "environment": "",
    "supply_demand": "",
    "loyalty": "",
    "historical": "",
    "corporate_pressure": ""
  },
  "reasoning": ""
}
```

**Paste actual request/response here:**

---

## Explanation Quality Checklist

### 1. Corporate Strategy Alignment

- [ ] **Corporate goals acknowledged**: Explanation mentions corporate revenue goals when present
- [ ] **Strategy notes referenced**: Corporate strategy notes are incorporated into explanation
- [ ] **Balanced perspective**: Explanation balances corporate objectives with market reality
- [ ] **Tension addressed**: If corporate pressure conflicts with market, tension is acknowledged

**Notes:**
_How well does the explanation align with corporate strategy?_

---

### 2. Business Logic Coherence

- [ ] **Factor relationships clear**: Explanation shows how factors combine to create recommendation
- [ ] **Market justification**: Market factors (supply/demand, environment) are clearly explained
- [ ] **Loyalty impact**: Loyalty discounts are clearly explained and justified
- [ ] **Historical context**: Historical patterns are referenced appropriately
- [ ] **Logical flow**: Explanation follows a logical sequence (context → factors → recommendation)

**Notes:**
_Is the business logic coherent and easy to follow?_

---

### 3. Guardrail Acknowledgment

- [ ] **Guardrails mentioned**: If guardrails are applied, they are clearly mentioned
- [ ] **Ethical reasoning**: Emergency guardrails are explained with ethical justification
- [ ] **Override explanation**: When guardrails override corporate pressure, it's clearly explained
- [ ] **Transparency**: System is transparent about guardrail application

**Notes:**
_Are guardrails properly acknowledged and explained?_

---

### 4. Clarity and Conciseness

- [ ] **Clear language**: Explanation uses business-friendly language (not overly technical)
- [ ] **Concise**: Explanation is not overly verbose (ideally 3-5 sentences)
- [ ] **Key values highlighted**: Adjustment percentage and goodness score are emphasized
- [ ] **Actionable**: Explanation provides actionable insights for decision-makers
- [ ] **Scannable**: Key information is easy to find quickly

**Notes:**
_Is the explanation clear, concise, and actionable?_

---

### 5. Goodness Score Justification

- [ ] **Goodness explained**: Explanation addresses why goodness score is high/low
- [ ] **Balance described**: Explanation describes balance between revenue, fairness, ethics
- [ ] **Tension indicators**: If goodness is low, tension is explained
- [ ] **Confidence level**: Goodness score is presented as confidence/balance indicator

**Notes:**
_Is the goodness score properly justified?_

---

### 6. Customer-Facing Appropriateness

- [ ] **Customer-friendly**: Explanation could be shown to customers (if applicable)
- [ ] **Fairness emphasized**: Fair pricing is emphasized when relevant
- [ ] **Loyalty rewarded**: Loyalty benefits are clearly communicated
- [ ] **Transparency**: System is transparent about pricing factors

**Notes:**
_Is the explanation appropriate for customer-facing contexts?_

---

## Prompt Tuning Suggestions

### For Dev-1/Dev-2 (LangChain Integration)

**Current Prompt Issues:**
_What issues exist with current explanation generation?_

**Suggested Prompt Improvements:**
1. 
2. 
3. 

**Example Improved Prompt:**
```
[Paste suggested prompt improvements here]
```

---

## Factor Weight Adjustments

### Current Factor Weights
- Environment: 1.0x
- Supply/Demand: 1.0x
- Historical: 0.6x
- Corporate Pressure: 0.4x
- Loyalty: 1.0x (discount)

### Suggested Adjustments
_Are factor weights appropriate? Should any be adjusted?_

**Environment Weight:** [ ] Keep [ ] Increase [ ] Decrease  
**Supply/Demand Weight:** [ ] Keep [ ] Increase [ ] Decrease  
**Historical Weight:** [ ] Keep [ ] Increase [ ] Decrease  
**Corporate Pressure Weight:** [ ] Keep [ ] Increase [ ] Decrease  
**Loyalty Weight:** [ ] Keep [ ] Increase [ ] Decrease  

**Reasoning:**
_Why should weights be adjusted?_

---

## Example Explanation Review

### Scenario: Airport Corridor Road Closure with Corporate Push

**Request:**
```json
{
  "zone": "airport_corridor",
  "scenario": "road_closure",
  "time": "2025-12-01T18:00:00Z",
  "loyalty_segment": "gold",
  "corporate_revenue_goal": 0.20,
  "corporate_strategy_notes": "Q4 end-of-quarter revenue push"
}
```

**Response Reasoning (Example):**
> "Based on current conditions in the airport corridor, we recommend a +12% price adjustment. The evening commute peak (6 PM) combined with the road closure creates strong market justification for surge pricing. Your Gold loyalty status provides a -5% discount, softening the impact. Corporate revenue goals of 20% are factored in but capped at +8% influence to maintain competitive positioning. Historical patterns show similar airport evening trips succeed at this pricing level. The recommendation balances revenue objectives with customer fairness."

**Review:**

✅ **Corporate Strategy Alignment**: Corporate goals are acknowledged, cap is explained  
✅ **Business Logic Coherence**: Factors are clearly explained in logical sequence  
✅ **Guardrail Acknowledgment**: Corporate pressure cap is mentioned  
✅ **Clarity**: Clear, concise, business-friendly language  
✅ **Goodness Justification**: Implicitly addressed through balance description  
✅ **Customer-Facing**: Appropriate for customer communication  

**Prompt Tuning Suggestions:**
- Could emphasize goodness score more explicitly
- Could add more specific historical context (e.g., "similar scenarios in past 30 days")

**Factor Weight Adjustments:**
- Current weights seem appropriate for this scenario
- No adjustments needed

---

## Review Summary

### Overall Assessment

**Explanation Quality:** [ ] Excellent [ ] Good [ ] Acceptable [ ] Needs Improvement

**Strengths:**
1. 
2. 
3. 

**Weaknesses:**
1. 
2. 
3. 

### Priority Actions

**High Priority:**
1. 
2. 

**Medium Priority:**
1. 
2. 

**Low Priority:**
1. 
2. 

---

## Next Steps

- [ ] Share review with Dev-1/Dev-2 for prompt tuning
- [ ] Update factor weights if needed
- [ ] Re-test scenario after improvements
- [ ] Document improvements in explanation generation

**Follow-up Date:** ________________


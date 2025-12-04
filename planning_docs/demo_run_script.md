# Demo Run Script - Step-by-Step Guide

Complete script for running the hackathon demo, including timing, narration, and UI actions.

**Total Demo Time**: 10-15 minutes  
**Target Audience**: Hackathon judges, Honeywell sponsors, technical evaluators

---

## Pre-Demo Setup (5 minutes before)

### Technical Setup
- [ ] Backend API running on `http://localhost:8000`
- [ ] Frontend UI accessible and responsive
- [ ] n8n workflow configured (if demonstrating alerts)
- [ ] Browser console cleared (no errors)
- [ ] Demo scenarios loaded in `demo_scenarios.json` accessible

### Preparation
- [ ] Open demo scenarios JSON file for reference
- [ ] Have backup scenarios ready (in case demo fails)
- [ ] Test internet connection (if using external APIs)
- [ ] Close unnecessary browser tabs/applications
- [ ] Prepare screen sharing (if remote presentation)

### Team Coordination
- [ ] Assign roles: Presenter, Demo Operator, Backup
- [ ] Establish hand signals for timing
- [ ] Prepare backup plan if demo fails

---

## Demo Script

### Opening (30 seconds)

**Narration:**
> "Thank you for your attention. Today we're demonstrating an AI-powered dynamic pricing advisor that balances corporate revenue goals with ethical constraints and customer trust. Let me show you how it works."

**Actions:**
- [ ] Open frontend UI
- [ ] Show clean initial state
- [ ] Point out form fields

**Visual Focus:** Clean UI, professional appearance

---

### Scenario 1: Airport Corridor Road Closure + Corporate Push (2.5 minutes)

**Story Setup (30 seconds):**
> "Imagine it's 6 PM on a weekday - peak evening commute time. A major freeway closure near the airport has created significant traffic delays. Meanwhile, corporate leadership has set an aggressive Q4 revenue target of 20% increase. Let's see how our system handles this."

**UI Actions:**
1. [ ] Select "airport_corridor" from zone dropdown
   - **Narrate**: "We're in the airport corridor zone"
2. [ ] Select "road_closure" from scenario dropdown
   - **Narrate**: "There's a road closure causing delays"
3. [ ] Set time to "2025-12-01T18:00:00" (6:00 PM)
   - **Narrate**: "It's evening rush hour - peak demand time"
4. [ ] Select "gold" from loyalty segment
   - **Narrate**: "The customer is a Gold member - a loyal customer"
5. [ ] Enter corporate revenue goal: "0.20" (20%)
   - **Narrate**: "Corporate wants a 20% revenue increase"
6. [ ] Add strategy notes: "Q4 end-of-quarter revenue push"
   - **Narrate**: "This is an aggressive Q4 push"
7. [ ] Click "Get Recommendation" button
   - **Narrate**: "Let's see what the system recommends"

**Results Review (1.5 minutes):**
- [ ] Wait for API response (2-3 seconds)
- [ ] Point out recommended adjustment (e.g., "+12%")
  - **Narrate**: "The system recommends a 12% price adjustment"
- [ ] Highlight factor breakdown:
  - **Environment**: "Road closure adds 5%"
  - **Supply/Demand**: "Peak hours add 15%"
  - **Loyalty**: "Gold discount reduces by 5%"
  - **Corporate Pressure**: "Corporate goal of 20% is capped at 8% influence"
  - **Narrate**: "Notice how corporate pressure is capped - it can't override market physics"
- [ ] Point out goodness score (e.g., "0.78")
  - **Narrate**: "Goodness score of 0.78 shows good balance between revenue and fairness"
- [ ] Read explanation (or summarize)
  - **Narrate**: "The explanation shows how all factors combine"

**Key Talking Points:**
- Corporate pressure is present but doesn't override market conditions
- Loyal customers get meaningful discounts
- System respects guardrails

**Transition:**
> "Now let's see what happens when we remove corporate pressure entirely."

---

### Scenario 2: Downtown Storm - No Corporate Pressure (2 minutes)

**Story Setup (20 seconds):**
> "Same storm conditions, but this time there's NO corporate revenue pressure. The company is prioritizing customer trust during the disruption."

**UI Actions:**
1. [ ] Select "downtown" from zone dropdown
2. [ ] Select "storm" from scenario dropdown
3. [ ] Set time to "2025-12-02T08:00:00" (8:00 AM)
4. [ ] Select "silver" from loyalty segment
5. [ ] **IMPORTANT**: Leave corporate revenue goal EMPTY
   - **Narrate**: "Notice we're NOT setting a corporate goal - trust-first approach"
6. [ ] Click "Get Recommendation"

**Results Review (1.5 minutes):**
- [ ] Point out recommended adjustment (e.g., "+15%")
  - **Narrate**: "System recommends 15% - fully market-justified"
- [ ] Compare goodness score to Scenario 1
  - **Narrate**: "Goodness score is higher - 0.82 vs 0.78 - no tension between revenue and ethics"
- [ ] Highlight absence of corporate pressure in factors
  - **Narrate**: "No corporate pressure factor - clean market-driven pricing"
- [ ] Emphasize trust-first approach
  - **Narrate**: "This shows the system works well even without corporate pressure"

**Key Talking Points:**
- System works well without corporate pressure
- Higher goodness when no tension
- Trust-first approach maintains customer relationships

**Transition:**
> "Most importantly, let's see how the system handles ethical guardrails."

---

### Scenario 3: Emergency Guardrail Override (2 minutes)

**Story Setup (20 seconds):**
> "A natural disaster or public emergency has occurred. Despite high corporate revenue pressure, the system MUST apply ethical guardrails."

**UI Actions:**
1. [ ] Select "downtown" from zone dropdown
2. [ ] Select "emergency" from scenario dropdown
   - **Narrate**: "Emergency situation declared"
3. [ ] Set time to "2025-12-03T14:00:00" (2:00 PM)
4. [ ] Select "standard" from loyalty segment
5. [ ] Enter corporate revenue goal: "0.25" (25%)
   - **Narrate**: "Even with 25% corporate pressure..."
6. [ ] Add strategy notes: "Aggressive revenue push"
7. [ ] Click "Get Recommendation"

**Results Review (1.5 minutes):**
- [ ] Point out recommended adjustment: "0%" (ZERO)
  - **Narrate**: "System recommends 0% - ethics override revenue"
- [ ] Highlight guardrail message in factors
  - **Narrate**: "See the guardrail message: 'Emergency guardrail applied'"
- [ ] Point out high goodness score (e.g., "0.90")
  - **Narrate**: "High goodness score - ethical pricing is 'good'"
- [ ] Emphasize override
  - **Narrate**: "Corporate pressure CANNOT override emergency protocols"

**Key Talking Points:**
- Ethics override revenue goals
- Guardrails protect service availability during crises
- High goodness reflects ethical compliance

**Transition:**
> "Let's see one more scenario that shows alignment between corporate goals and market reality."

---

### Scenario 4: Holiday Airport with Moderate Goal (1.5 minutes) [Optional]

**Story Setup (15 seconds):**
> "Christmas Day at the airport - holiday travel surge. Corporate has set a moderate revenue goal aligned with expected demand."

**UI Actions:**
1. [ ] Select "airport_corridor" from zone dropdown
2. [ ] Select "holiday" from scenario dropdown
3. [ ] Set time to "2025-12-25T16:00:00" (4:00 PM, Christmas Day)
4. [ ] Select "platinum" from loyalty segment
5. [ ] Enter corporate revenue goal: "0.12" (12%)
6. [ ] Add strategy notes: "Balanced growth strategy"
7. [ ] Click "Get Recommendation"

**Results Review (1 minute):**
- [ ] Point out recommended adjustment (e.g., "+10%")
- [ ] Highlight high goodness score (e.g., "0.87")
  - **Narrate**: "High goodness - corporate goals align with market reality"
- [ ] Show Platinum loyalty protection
  - **Narrate**: "Premium customers are protected even during surge"

**Key Talking Points:**
- Ideal scenario: alignment between goals and market
- Premium customers protected
- Sustainable pricing

**Transition:**
> "This demonstrates the ideal scenario - when corporate goals align with market conditions."

---

### Closing Summary (1 minute)

**Narration:**
> "In summary, our AI-powered pricing advisor:
> - Balances multiple factors: market conditions, loyalty, historical patterns, and corporate goals
> - Applies ethical guardrails: emergencies can't be exploited
> - Provides transparency: every recommendation is explainable
> - Sends alerts: notifies when tensions arise between revenue and ethics
> 
> This approach applies to Honeywell's industrial pricing challenges - balancing revenue goals with long-term customer relationships and regulatory compliance.
> 
> Thank you. Questions?"

**Actions:**
- [ ] Return to main UI screen
- [ ] Show architecture diagram (if available)
- [ ] Prepare for Q&A

---

## Backup Scenarios (If Demo Fails)

### Quick Recovery Options

**Option 1: Pre-recorded Video**
- Have screen recording of demo scenarios ready
- Play video if live demo fails
- Narrate over video

**Option 2: Static Screenshots**
- Prepare screenshots of each scenario result
- Show screenshots and explain results
- Less impressive but functional

**Option 3: API Console Demo**
- Use curl commands or Postman
- Show API responses directly
- Explain results from JSON

**Option 4: Skip to Architecture**
- If all demos fail, focus on architecture explanation
- Use diagrams and code walkthrough
- Emphasize technical innovation

---

## Common Issues and Solutions

### Issue: API Not Responding
**Solution:**
- Check backend is running: `curl http://localhost:8000/api/v1/health`
- Restart backend if needed
- Use backup scenario (pre-recorded)

### Issue: Frontend Not Loading
**Solution:**
- Refresh page
- Check browser console for errors
- Use API console demo as backup

### Issue: Slow API Response
**Solution:**
- Acknowledge delay: "The system is processing..."
- Explain what's happening: "AI agents are analyzing factors..."
- Have patience - 3-5 seconds is acceptable

### Issue: Unexpected Results
**Solution:**
- Acknowledge: "Interesting - let me explain what's happening"
- Use it as teaching moment
- Explain factor interactions

### Issue: Network Problems
**Solution:**
- Use local demo (no external APIs)
- Have offline backup ready
- Explain architecture if demo completely fails

---

## Post-Demo Checklist

- [ ] Thank audience
- [ ] Provide contact information
- [ ] Share repository link (if applicable)
- [ ] Offer to answer questions
- [ ] Collect feedback (if appropriate)

---

## Demo Timing Summary

| Section | Time | Cumulative |
|---------|------|------------|
| Opening | 0:30 | 0:30 |
| Scenario 1 | 2:30 | 3:00 |
| Scenario 2 | 2:00 | 5:00 |
| Scenario 3 | 2:00 | 7:00 |
| Scenario 4 (Optional) | 1:30 | 8:30 |
| Closing | 1:00 | 9:30 |
| Q&A Buffer | 0:30-5:30 | 10:00-15:00 |

**Total**: 10-15 minutes

---

## Success Criteria

**Demo is successful if:**
- [ ] All scenarios execute without errors
- [ ] Results match expected ranges
- [ ] Key talking points are covered
- [ ] Audience understands value proposition
- [ ] Technical innovation is clear
- [ ] Honeywell connection is made

**Good luck with your demo!**


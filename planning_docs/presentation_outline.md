# Presentation Outline - Honeywell Dynamic Pricing Hackathon

Slide structure and talking points for 10-15 minute hackathon presentation.

---

## Slide 1: Title Slide

**Content:**
- Project Title: "AI-Powered Dynamic Pricing Advisor with Ethical Guardrails"
- Team Name / Members
- Hackathon Name / Date
- Honeywell Sponsor Logo

**Talking Points:**
- Brief introduction of team
- Thank Honeywell for sponsorship
- Set context: solving real-world pricing challenges

**Time:** 30 seconds

---

## Slide 2: Problem Framing

**Content:**
- **The Challenge**: Dynamic pricing in rideshare/transportation
- **Key Tensions**:
  - Corporate revenue goals vs. customer trust
  - Market-driven pricing vs. ethical constraints
  - Short-term revenue vs. long-term customer relationships
- **Real-World Impact**: How pricing decisions affect brand reputation

**Talking Points:**
- "Dynamic pricing is everywhere - rideshare, airlines, hotels"
- "But there's a tension: maximize revenue vs. maintain customer trust"
- "What happens when corporate pushes for 20% revenue increase during a storm?"
- "How do we balance business objectives with ethical pricing?"

**Time:** 1.5 minutes

---

## Slide 3: System Concept

**Content:**
- **Core Idea**: AI-powered pricing advisor that balances multiple factors
- **Key Features**:
  - Multi-factor analysis (environment, supply/demand, loyalty, historical, corporate)
  - Ethical guardrails (emergency override, loyalty protection)
  - Transparency (explainable AI with factor breakdown)
  - Alert system (notify when tensions arise)
- **Value Proposition**: "Smart pricing that respects both revenue goals and customer trust"

**Talking Points:**
- "We built an AI system that doesn't just maximize revenue - it balances multiple factors"
- "It considers market conditions, customer loyalty, historical patterns, AND corporate goals"
- "But it has ethical guardrails - emergencies can't be exploited"
- "And it's transparent - we explain every recommendation"

**Time:** 2 minutes

---

## Slide 4: Architecture Flow

**Content:**
- **System Diagram**:
  ```
  User Input → FastAPI Backend
                ↓
         LangChain Orchestrator
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
  Agents    Agents    Agents
  (Env)   (Supply)  (Loyalty)
    ↓           ↓           ↓
    └───────────┼───────────┘
                ↓
         Factor Combination
                ↓
         Guardrail Application
                ↓
         Explanation Generation
                ↓
         n8n Alert (if needed)
                ↓
         Response to User
  ```

**Talking Points:**
- "FastAPI backend receives pricing requests"
- "LangChain orchestrator coordinates multiple AI agents"
- "Each agent analyzes a different factor"
- "Factors are combined, guardrails applied, explanation generated"
- "If tensions arise, alerts are sent via n8n"

**Time:** 2 minutes

---

## Slide 5: Key Components

**Content:**
- **Five Factor Agents**:
  1. Environment Agent (weather, road closures, emergencies)
  2. Supply/Demand Agent (time of day, driver availability)
  3. Loyalty Agent (customer tier discounts)
  4. Historical Agent (past pricing patterns)
  5. Corporate Pressure Agent (revenue goals)
- **Guardrails**:
  - Emergency override (0% surge during disasters)
  - Loyalty protection (caps for premium customers)
  - Maximum surge limits
- **Explanation Chain**: LangChain generates natural language explanations

**Talking Points:**
- "Five specialized agents analyze different aspects"
- "Guardrails ensure ethical pricing - emergencies can't be exploited"
- "Every recommendation comes with an explanation"

**Time:** 1.5 minutes

---

## Slide 6: Demo Walkthrough - Scenario 1

**Content:**
- **Scenario**: Airport Corridor Road Closure + Corporate Push
- **Input**: Zone, scenario, time, loyalty (Gold), corporate goal (20%)
- **Output**: +12% adjustment, goodness 0.78
- **Key Highlight**: Corporate pressure capped at 8% influence

**Talking Points:**
- "Let's see it in action"
- "Evening commute, road closure, corporate wants 20% revenue increase"
- "System recommends +12% - balances market conditions with corporate goals"
- "Notice: corporate pressure is capped - can't override market physics"

**Time:** 2 minutes (includes live demo)

---

## Slide 7: Demo Walkthrough - Scenario 2

**Content:**
- **Scenario**: Downtown Storm - No Corporate Pressure
- **Input**: Zone, scenario (storm), time, loyalty (Silver), NO corporate goal
- **Output**: +15% adjustment, goodness 0.82
- **Key Highlight**: Higher goodness when no corporate tension

**Talking Points:**
- "Now let's see trust-first approach"
- "Same storm conditions, but NO corporate pressure"
- "System recommends +15% - fully market-justified"
- "Notice higher goodness score - no tension between revenue and ethics"

**Time:** 1.5 minutes (includes live demo)

---

## Slide 8: Demo Walkthrough - Scenario 3

**Content:**
- **Scenario**: Emergency Guardrail Override
- **Input**: Emergency scenario, high corporate pressure (25%)
- **Output**: 0% adjustment, goodness 0.90
- **Key Highlight**: Ethics override revenue goals

**Talking Points:**
- "Most importantly - ethical guardrails"
- "Emergency declared, corporate wants 25% revenue increase"
- "System recommends 0% - ethics override revenue"
- "High goodness score - ethical pricing is 'good'"

**Time:** 1.5 minutes (includes live demo)

---

## Slide 9: Honeywell Mapping

**Content:**
- **Industrial Pricing Applications**:
  - Manufacturing parts pricing (supply chain disruptions)
  - Service contracts (demand fluctuations)
  - Equipment rental (seasonal demand)
- **Corporate Pressure Scenarios**:
  - Quarterly revenue targets
  - Market share goals
  - Competitive positioning
- **Guardrails for Industrial Context**:
  - Customer relationship protection
  - Long-term contract considerations
  - Regulatory compliance

**Talking Points:**
- "How does this apply to Honeywell?"
- "Same principles: balance revenue goals with customer relationships"
- "Industrial pricing faces similar tensions"
- "Guardrails protect long-term partnerships"

**Time:** 2 minutes

---

## Slide 10: Extension Ideas

**Content:**
- **Future Enhancements**:
  - Real-time market data integration
  - Machine learning model training on historical data
  - Multi-zone optimization
  - Customer segmentation refinement
  - A/B testing framework
- **Scalability**:
  - Cloud deployment (AWS/Azure)
  - Microservices architecture
  - Real-time streaming data

**Talking Points:**
- "This is a foundation - many extensions possible"
- "Real-time data integration"
- "ML model training"
- "Scalable architecture"

**Time:** 1 minute

---

## Slide 11: Key Takeaways

**Content:**
- **Three Key Points**:
  1. AI can balance revenue goals with ethical constraints
  2. Transparency builds trust (explainable AI)
  3. Guardrails protect both customers and brand reputation
- **Business Value**:
  - Sustainable revenue growth
  - Customer trust maintenance
  - Ethical compliance

**Talking Points:**
- "Three key takeaways"
- "AI can balance competing objectives"
- "Transparency builds trust"
- "Guardrails protect everyone"

**Time:** 1 minute

---

## Slide 12: Q&A

**Content:**
- "Questions?"
- Contact information
- GitHub repository link (if applicable)
- Demo access information

**Talking Points:**
- "Thank you for your attention"
- "We're happy to answer questions"
- "Demo is available for hands-on exploration"

**Time:** 2-3 minutes (as needed)

---

## Presentation Timing Summary

- **Total Time**: 10-15 minutes
- **Slides 1-5**: 7 minutes (setup and architecture)
- **Slides 6-8**: 5 minutes (demo scenarios)
- **Slides 9-12**: 3-4 minutes (mapping, extensions, Q&A)

**Buffer Time**: 1-2 minutes for transitions and questions

---

## Presentation Tips

1. **Demo Preparation**:
   - Pre-load demo scenarios in UI
   - Have backup scenarios ready
   - Test API connectivity before presentation

2. **Storytelling**:
   - Start with problem (tension between revenue and trust)
   - Show solution (balanced AI system)
   - Demonstrate value (live demos)
   - Connect to sponsor (Honeywell mapping)

3. **Visual Aids**:
   - Use diagrams for architecture
   - Show actual UI during demos
   - Highlight key numbers (adjustment %, goodness)

4. **Engagement**:
   - Ask rhetorical questions
   - Pause after key points
   - Make eye contact with judges/sponsors

5. **Handling Questions**:
   - Prepare answers for common questions:
     - "How does this differ from existing solutions?"
     - "What's the accuracy of recommendations?"
     - "How do you handle edge cases?"
     - "What's the scalability?"


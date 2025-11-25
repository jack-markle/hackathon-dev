## DRAFT – Hackathon Plan Proposal
*Working title:* AI Pricing Monitor & Advisor (internal BA console)
### 1. TL;DR
Instead of building a full-blown consumer ride-pricing system, we focus on a *tech demo for a business analyst*:
An internal console where a pricing analyst can ask,
“Given situation X, what pricing adjustment do you recommend and why?”
Under the hood, an AI “orchestrator” looks at environmental conditions, supply/demand, loyalty, and historical data, then returns:
* a suggested price adjustment,
* a “goodness” score, and
* a clear explanation.
We keep the implementation thin and demo-friendly so we can actually finish in 3 build days and use Day 4 to polish the presentation.
---
### 2. Problem & Target User (Sponsor Framing)
Sponsor’s situation (rephrased):
* Revenue is down and *current pricing strategy is slow to adapt*.
* Competitors have access to the same raw data (rides, locations, time, etc.), so “we use data” is not a differentiator.
* They want *dynamic pricing that is competitive, profitable, and fair*, and they explicitly care about:
  * speed of adjustment,
  * explainability,
  * and guardrails.
We are *not* building the final production system.
We’re giving their *AI Lead and pricing team a pattern*:
“Here’s how an AI assistant could watch key signals, suggest adjustments, and justify those suggestions in human terms.”
Target user:
*Internal pricing analyst / business owner*, not a rider.
---
### 3. Concept: AI Pricing Monitor & Advisor
*Core idea:*
A single internal console where a pricing analyst can:
* Ask scenario-based questions:
  * “Construction is closing the main airport route. What should we do to prices?”
  * “Storm tonight, driver supply low—how should we adjust downtown vs suburbs?”
* Get back:
  * a recommended *price adjustment* (e.g. “+10% in Zone A for the next 2 hours”),
  * a *goodness score* (how well this balances profit & fairness),
  * a *reasoning summary* (referencing environment, supply/demand, loyalty, historical behavior).
* Optionally trigger automatic *logging/alerts via n8n* when goodness drops or certain thresholds are hit.
Conceptually, this uses our four “agents”:
1. *Environmental Agent* – disasters, weather, road closures, gas shortages, etc.
2. *Loyalty Agent* – customer loyalty tiers, ratings, discount impact.
3. *Supply & Demand Agent* – online drivers, requests, time of day, holidays.
4. *Historical Data Agent* – what worked recently for similar trips.
For the hackathon MVP, these can be *simple functions & heuristics plus one LangChain chain*, and we present them as “agents” in our architecture and reasoning.
---
### 4. MVP Scope (Realistic in ~3 Dev Days)
#### 4.1 Backend – FastAPI
* Single main endpoint, e.g. POST /recommendation
  * Input (example):
json
    {
      "zone": "airport_corridor",
      "scenario": "road_closure",
      "time": "2025-11-27T18:00:00",
      "loyalty_segment": "gold",
      "notes": "evening commute, partial freeway closure"
    }
    
  * Backend computes:
    * environment_factor (e.g. +5% for road closure, unless emergency)
    * supply_demand_factor (e.g. +10% if high demand / low drivers)
    * loyalty_factor (e.g. −5% for loyal riders)
    * historical_factor (e.g. “similar trips succeed around 1.05x here”)
  * Combines into:
json
    {
      "recommended_adjustment": 0.10,
      "goodness": 0.78,
      "factors": {
        "environment": "...short summary...",
        "supply_demand": "...",
        "loyalty": "...",
        "historical": "..."
      },
      "reasoning": "...BA-friendly explanation..."
    }
    
* Basic “goodness” metric:
  Something simple but believable, e.g. a weighted combination of revenue proxy + acceptance proxy + fairness constraints. It doesn’t have to be mathematically perfect, just coherent.
#### 4.2 LangChain
* One LLM chain (or similar) that:
  * Takes the factors (environment, supply/demand, loyalty, historical, recommended_adjustment, goodness),
  * Returns a *natural-language explanation*:
    * why this adjustment,
    * what trade-offs are involved,
    * how it balances profit vs fairness and loyalty.
We talk about the 4 conceptual agents, but in code we keep it to one orchestrator + one chain to stay sane on time.
#### 4.3 Frontend – Next.js
* Single page: *“Pricing Analyst Console”*
  * Form inputs:
    * Zone/region dropdown (Downtown / Airport / Suburbs / Stadium, etc.)
    * Scenario dropdown (Normal day / Concert / Storm / Road closure / Holiday)
    * Optional notes box (free text)
  * Button: *“Analyze and Recommend”*
  * Output area:
    * Recommended adjustment (e.g. *“+10% in Airport Corridor – Next 2 hours”*)
    * Goodness score (numeric, maybe color-coded)
    * Reasoning box (separate panel labeled “AI reasoning”)
We demo as:
“Analyst plugs in a scenario → gets a suggested adjustment + explanation.”
#### 4.4 n8n Integration
Lightweight, demo-level integration:
* Simple workflow:
  * Webhook node: receives { zone, adjustment, goodness }
  * Condition: if goodness < threshold (e.g. 0.7) OR certain risk flags present
  * Action: log to a sheet/DB or send email/slack-style message:
    > “Alert: Pricing goodness low in Zone X. Please review AI recommendations.”
In FastAPI, after generating a recommendation, we POST to this webhook.
We show the workflow in:
* Our *architecture diagram*
* Optionally a quick “here’s the alert it would send” in the demo/video
---
### 5. How This Addresses the Sponsor Brief
*Sponsor wants:*
* Faster pricing adjustments
* Use of “agentic AI”
* Profitability + fairness
* Something concrete enough to inspire their own AI implementation
*Our MVP delivers:*
* An *internal AI advisor* that:
  * scans conceptual factors (env, supply/demand, loyalty, historical),
  * proposes concrete adjustments per zone/time,
  * provides transparent reasoning, not just black-box numbers.
* “Agentic AI” is expressed as:
  * distinct roles (4 conceptual agents),
  * orchestrated into a single recommendation.
* *Goodness metric* and *guardrails*:
  * We explicitly show how we avoid over-surge in emergencies or fragile segments.
* *Extensibility*:
  * With more time, they can:
    * plug in real data sources (traffic, real historical DB),
    * refine the metrics,
    * expand agents and policies.
This is exactly the type of pattern an AI lead can adopt, refine, and scale.
---
### 6. Architecture Summary (for slides)
High-level diagram:
* *Pricing Analyst Console (Next.js)*
  * UI where analyst defines scenario and zones.
→ *Pricing Orchestrator (FastAPI + LangChain)*
* Conceptual agents:
  * Environmental Agent
  * Supply & Demand Agent
  * Loyalty Agent
  * Historical Data Agent
* Combines their “votes” into:
  * recommended adjustment
  * goodness score
  * reasoning explanation
→ *n8n Workflow*
* Logs key events
* Sends alerts when “goodness” drops or guardrails trip
Mock data (Python constants / simple structures) stand in for real databases during the demo.
---
### 7. Rough Timeline (Assuming 3 Build Days + Presentation Day)
This is flexible, but as a starting point:
*Day 1 – Skeletons & Alignment*
* Agree on this scope (or adjust).
* FastAPI:
  * create /recommendation endpoint with static fake output.
* Next.js:
  * build single-page console UI wired to call the endpoint.
* LangChain:
  * stub simple chain that returns explanation text.
*Day 2 – Logic & Glue*
* Implement simple factor calculations for:
  * environment, supply/demand, loyalty, historical.
* Wire factors → LangChain explanation.
* Have at least 2–3 scripted scenarios working end-to-end.
* Set up n8n workflow + FastAPI POST to its webhook.
*Day 3 – Polish & Prep*
* Refine prompts so explanations sound like BA output, not random chatbot babble.
* Clean up UI (labels, layout, reasoning box).
* Finalize “goodness” metric explanation.
* Start slide deck:
  * Problem framing, concept, architecture diagram,
  * 2–3 example scenarios and what the AI recommends.
*Day 4 – Presentation Focus*
* Finish slides.
* Record the 10-min video walk-through (slides + demo).
* Do one practice run of the 15-min live talk:
  * Who says what,
  * Which scenario you show,
  * How you tie it back to sponsor’s reality.
---
If the team is okay with this, we get:
* A *realistic scope* for the time we actually have,
* A demo that *makes sense to a business analyst*,
* And something the sponsor’s AI lead can look at and think:
  > “Okay, this is a pattern we can adapt, not just a toy example.”
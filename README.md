# AI Pricing Monitor & Advisor

## Demo Video Link

Hackathon Team 4 Demo Video: https://www.youtube.com/watch?v=zpY9j4uK6q8

## Architecture Diagram

The architecture diagram for our project can be viewed via `architecture.png`.

This project is a dynamic pricing recommendation system designed to help ride-sharing services adjust prices based on real-time conditions, historical data, and corporate strategy. It consists of a modern web frontend and a robust Python backend.

## Project Structure & Implementation

The repository is organized into two main applications:

### Frontend (`/frontend`)
Built with **Next.js 15**, **React 19**, and **Tailwind CSS 4**.
- **User Interface**: Provides a dashboard for operations teams to input scenario parameters (e.g., weather, traffic, demand) and corporate goals.
- **Integration**: Communicates with the backend API to fetch pricing recommendations and display detailed reasoning.

### Backend (`/backend`)
Built with **FastAPI**, **Pydantic**, and **Pandas**.
- **Architecture**:
  - **API Layer** (`app/api`): Thin routes that handle request/response validation using Pydantic models.
  - **Service Layer** (`app/services`): Contains the core business logic, including the `RecommendationService`.
  - **Data Layer**: Loads and processes historical data (`dynamic_pricing.csv`) and configuration files (JSON) for loyalty tiers and zone patterns.
- **Key Technologies**:
  - **LangChain**: Used for orchestrating complex reasoning steps (if enabled/implemented in specific workflows).
  - **n8n Integration**: Optional webhook capabilities for alerts and logging.

## Dynamic Pricing & Corporate Strategy

The core feature of this application is its ability to translate high-level corporate goals into specific, actionable pricing adjustments while maintaining market stability and customer trust.

### How It Works
The system calculates a "Recommended Adjustment" (price multiplier) based on five key factors:

1.  **Environment**: Impact of weather events, road closures, or emergencies.
2.  **Supply & Demand**: Real-time balance of riders vs. drivers.
3.  **Loyalty**: Programmatic discounts for different customer tiers (e.g., Gold, Platinum).
4.  **Historical**: Analysis of past ride costs and acceptance rates for similar routes.
5.  **Corporate Pressure**: This is where the **Corporate Pricing Catalog** adjustments come into play.

### Adjusting the Corporate Pricing Catalog
When a corporate strategy is input (e.g., "Increase Q4 Revenue by 15%"), the system doesn't just blindly raise prices. Instead:
- It interprets the **Revenue Goal** and **Strategy Notes** to calculate a "pressure" factor.
- It applies **Guardrails** (Ethical and Market-based) to ensure the suggested price doesn't exceed reasonable limits (preventing price gouging during emergencies or pricing out loyal customers).
- It produces a **Goodness Score** indicating confidence in the recommendation.

This allows the business to dynamically adjust its "catalog" of base prices in response to strategic objectives, ensuring that pricing changes are data-driven, explained clearly, and safety-bounded.

---

**Developer Note:**
After you clone this repo, if you want the planning docs to be pulled down into this repo (for prompting), use:
`git submodule update --init`

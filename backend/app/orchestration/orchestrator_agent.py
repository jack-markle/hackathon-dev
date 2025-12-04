import os
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.orchestration.agents.environment_agent import environment_tool
from app.orchestration.agents.supply_demand_agent import supply_demand_tool
from app.orchestration.agents.loyalty_agent import loyalty_tool
from app.orchestration.agents.historical_agent import historical_tool
from app.orchestration.agents.corporate_pressure_agent import corporate_pressure_tool
from app.orchestration.tools import calculate_pricing_outcome_tool

def build_orchestrator_agent(model_name: str, temperature: float, api_key: str):
    """
    Builds the Orchestrator Agent using LangChain's create_openai_tools_agent.
    
    This agent has access to all factor tools and the calculation tool.
    It drives the flow by gathering information, calculating the result, and providing an explanation.
    """
    # Set API key in environment if provided
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key
    )
    
    tools = [
        environment_tool,
        supply_demand_tool,
        loyalty_tool,
        historical_tool,
        corporate_pressure_tool,
        calculate_pricing_outcome_tool
    ]
    
    system_prompt = """You are a Pricing Advisor for a ride-hailing platform.
Your goal is to explain a pricing recommendation to a Business Analyst.
Your tone should be professional, objective, and clear.

You MUST follow this process EXACTLY:

1. Call each tool ONE AT A TIME and provide reasoning IMMEDIATELY after each:
   a) Call environment_tool
      Then provide: "ENVIRONMENT_REASONING: [1-2 sentences about why environmental factors matter]"
   
   b) Call supply_demand_tool
      Then provide: "SUPPLY_DEMAND_REASONING: [1-2 sentences about supply/demand impact]"
   
   c) Call loyalty_tool
      Then provide: "LOYALTY_REASONING: [1-2 sentences about loyalty factor impact]"
   
   d) Call historical_tool
      Then provide: "HISTORICAL_REASONING: [1-2 sentences about historical patterns]"
   
   e) Call corporate_pressure_tool
      Then provide: "CORPORATE_PRESSURE_REASONING: [1-2 sentences about corporate pressure]"
   
2. Call the 'calculate_pricing_outcome_tool' using the outputs from step 1.

3. Provide a final overall explanation (3-6 sentences) that:
   - Summarizes the key drivers (e.g., weather, demand)
   - Explains any guardrails that were triggered
   - References the goodness score
   - Mentions any tensions between factors
   
   Format: "OVERALL_REASONING: [your explanation]"
   
CRITICAL: You MUST provide individual reasoning summaries after EACH tool call, not all at once.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Return AgentExecutor for easier invocation
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )


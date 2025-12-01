"""
LangChain-based pricing explanation chain - STUB for Dev 2

Responsibility: Generate natural language reasoning for pricing recommendations.

Current state: Dev 1 has implemented a placeholder reasoning generator in
recommendation_service._generate_placeholder_reasoning().

Dev 2 should:
1. Create a LangChain chain with proper prompts
2. Configure it to reference all five factors + goodness score
3. Replace the placeholder reasoning with LLM-generated text
"""
from typing import Any, Dict


def build_pricing_explanation_chain(llm=None):
    """
    Build a LangChain chain for generating pricing explanations.
    
    TODO (Dev 2):
    1. Set up ChatPromptTemplate with system and human messages
    2. Configure to reference environment, supply/demand, loyalty, historical,
       corporate pressure factors and goodness score
    3. Use BA-friendly tone and explain trade-offs
    4. Return a Runnable chain
    
    Example structure:
    ```python
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_openai import ChatOpenAI
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a pricing advisor for ride-hailing..."),
        ("human", "Given these factors: {factors}, recommend: {adjustment}..."),
    ])
    
    chain = template | llm | StrOutputParser()
    return chain
    ```
    """
    raise NotImplementedError(
        "Dev 2: Implement LangChain explanation chain here. "
        "See backend/app/services/recommendation_service.py for the "
        "placeholder implementation to replace."
    )


def generate_explanation(
    request: Dict[str, Any],
    factors: Dict[str, str],
    adjustment: float,
    goodness: float
) -> str:
    """
    Generate a natural language explanation for the pricing recommendation.
    
    TODO (Dev 2): Implement this using the LangChain chain above.
    
    Args:
        request: Original request context (zone, scenario, time, etc.)
        factors: Dictionary of factor summaries
        adjustment: Recommended adjustment value
        goodness: Goodness score
    
    Returns:
        Natural language explanation string
    """
    raise NotImplementedError(
        "Dev 2: Use build_pricing_explanation_chain() to generate "
        "LLM-powered explanation here."
    )


"""Utility functions for the Perplexity MCP."""

import os
import logging
from typing import Dict, List, Any


def validate_perplexity_key() -> bool:
    """
    Validate that the Perplexity API key is set.
    
    Returns:
        bool: True if the API key is set, False otherwise
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    return api_key is not None and len(api_key) > 0


def get_available_models() -> Dict[str, str]:
    """
    Get the available Perplexity models and their descriptions.
    
    Returns:
        Dict[str, str]: A dictionary of model names and descriptions
    """
    return {
        "sonar-deep-research": "128k context - Enhanced research capabilities",
        "sonar-reasoning-pro": "128k context - Advanced reasoning with professional focus",
        "sonar-reasoning": "128k context - Enhanced reasoning capabilities",
        "sonar-pro": "200k context - Professional grade model",
        "sonar": "128k context - Default model",
        "r1-1776": "128k context - Alternative architecture"
    }


def log_model_info():
    """Log information about the selected model and available models."""
    model = os.getenv("PERPLEXITY_MODEL", "sonar")
    logging.info(f"Using Perplexity AI model: {model}")
    
    available_models = get_available_models()
    
    logging.info("Available Perplexity models (set with PERPLEXITY_MODEL environment variable):")
    for model_name, description in available_models.items():
        marker = "→" if model_name == model else " "
        logging.info(f" {marker} {model_name}: {description}")


def format_response_with_citations(content: str, citations: List[str]) -> str:
    """
    Format a response with citations.
    
    Args:
        content: The content of the response
        citations: A list of citation URLs
        
    Returns:
        str: The formatted response with citations
    """
    if not citations:
        return content
        
    formatted_citations = "\n\nCitations:\n" + "\n".join(
        f"[{i+1}] {url}" for i, url in enumerate(citations)
    )
    return content + formatted_citations


def get_perplexity_payload(query: str, recency: str) -> Dict[str, Any]:
    """
    Get the payload for a Perplexity API request.
    
    Args:
        query: The search query
        recency: The recency filter ("day", "week", "month", "year")
        
    Returns:
        Dict[str, Any]: The payload for the request
    """
    model = os.getenv("PERPLEXITY_MODEL", "sonar")
    
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": query},
        ],
        "max_tokens": "512",
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": recency,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "return_citations": True,
        "search_context_size": "low",
    }
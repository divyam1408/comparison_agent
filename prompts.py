"""
Prompt templates for the Comparison Workflow system.

This module contains all the prompt templates used by the ComparisonWorkflow class,
separated for easier maintenance and modification.
"""

# Search Query Generation Prompts
SEARCH_QUERY_SYSTEM_PROMPT = """You generate concise, effective web search queries. Return ONLY a SINGLE search query, no explanations."""

SEARCH_QUERY_USER_PROMPT = """You are generating a web search query for an information retrieval system.

First analyse the user query to find essential keywords to answer it.
Once you have analyzed it, produce:
- ONE concise web search query
- Maximum 8–12 words
- Include only essential keywords
- No explanations, no punctuation beyond spaces
- Do not include questions or full sentences

User query:
{user_query}

Output:"""

# Comparison Report Generation Prompts
COMPARISON_SYSTEM_PROMPT = """You are an expert assistant helping users to choose between multiple options by providing detailed explanations and reasoning for every option.
Although you are quite knowledgable in various topics, but still to help you give better comparison, some information from web relevent to user query is also provided.
Use the web context provided along with your own understanding about the topic to answer the user query."""

COMPARISON_USER_PROMPT = """Original comparison request: {user_query}

Web search context:
{search_context}"""

# Main User Query Template (Jinja2)
USER_PROMPT_TEMPLATE = """Compare the following options in a clear and neutral way.

<options>
{% for opt in options %}
{{ loop.index }}. {{ opt }}
{% endfor %}
</options>

{% if constraints %}
Restrict the comparison to the following dimensions only:
<constraints>
{% for c in constraints %}
- {{ c }}
{% endfor %}
</constraints>
{% endif %}

Instructions:
- Compare options only along the specified dimensions if provided
- Otherwise, choose relevant comparison dimensions
- Explain key differences and trade-offs
- Use clear section headings by dimension
- Cover all options consistently
- Keep corresponding dimension in same units

Output:
1. Detailed comparison by specified dimension
2. Final summary MUST include:
    - Aggregated pros and cons.
    - A concise comparison table containing essential attributes.

Formatting guidelines:
- Do NOT use markdown emphasis such as **bold**, italics, or inline styling
- Use clear section titles on their own lines (no special characters)
- Use bullet points only for lists
- Keep formatting simple and readable


Constraints:
- Do not recommend a final option"""


def get_search_query_messages(user_query: str) -> list:
    """
    Generate messages for search query generation.
    
    Args:
        user_query: The user's comparison request
        
    Returns:
        List of message dictionaries for LLM API
    """
    return [
        {
            "role": "system",
            "content": SEARCH_QUERY_SYSTEM_PROMPT
        },
        {
            "role": "user", 
            "content": SEARCH_QUERY_USER_PROMPT.format(user_query=user_query)
        }
    ]


def get_comparison_messages(user_query: str, search_context: str) -> list:
    """
    Generate messages for comparison report generation.
    
    Args:
        user_query: The original user comparison request
        search_context: Aggregated web search results
        
    Returns:
        List of message dictionaries for LLM API
    """
    return [
        {
            "role": "system",
            "content": COMPARISON_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": COMPARISON_USER_PROMPT.format(
                user_query=user_query,
                search_context=search_context
            )
        }
    ]
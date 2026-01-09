import os
import json
import sys
from jinja2 import Template
from typing import List, Dict, Any
import aisuite as ai
from tavily import TavilyClient
from prompts import get_search_query_messages, get_comparison_messages, USER_PROMPT_TEMPLATE

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Make sure environment variables are set manually.")

# Validate required API keys
required_keys = ["OPENAI_API_KEY", "HUGGINGFACE_API_KEY", "TAVILY_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]

if missing_keys:
    print(f"Error: Missing required environment variables: {', '.join(missing_keys)}")
    print("Please set these in your environment or create a .env file.")
    print("See .env.example for the required format.")
    sys.exit(1)


class ComparisonWorkflow:
    """Implements a workflow for comparing options using LLM and web search."""
    
    def __init__(self):
        self.llm_client = ai.Client()
        self.search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.model = "huggingface:mistralai/Mistral-7B-Instruct-v0.2"  # Using tested Mistral model
    
    def generate_search_query(self, user_query: str) -> str:
        """Generate a concise web search query from user's comparison request."""
        messages = get_search_query_messages(user_query)
        
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )
        
        return response.choices[0].message.content.strip()
    
    def perform_web_search(self, search_query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Perform web search and return results."""
        response = self.search_client.search(
            query=search_query,
            search_depth="advanced",
            max_results=max_results
        )
        
        return response.get("results", [])
    
    def aggregate_search_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Aggregate web search results into textual context."""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            
            context_parts.append(f"Source {i}: {title}\n{content}\nURL: {url}\n")
        
        return "\n".join(context_parts)
    
    def generate_comparison_report(self, user_query: str, search_context: str) -> str:
        """Generate detailed comparison report using original query and search context."""
        messages = get_comparison_messages(user_query, search_context)
        
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.4
        )
        
        return response.choices[0].message.content.strip()
    
    def run_comparison(self, options: list[str], constraints: list[str] | None = None) -> Dict[str, str]:
        """
            Full pipeline: LLM → Tavily → LLM
            Args:
                model: The name of the model to use.
                options: The options to compare.
                constraints: Optional list of comparison constraints.
        """

        user_prompt_template = USER_PROMPT_TEMPLATE
        template = Template(user_prompt_template)
        user_prompt = template.render(options=options, constraints=constraints)
        # Step 1: Generate search query
        search_query = self.generate_search_query(user_prompt)
        
        # Step 2: Perform web search
        search_results = self.perform_web_search(search_query)
        
        # Step 3: Aggregate search context
        search_context = self.aggregate_search_context(search_results)
        
        # Step 4: Generate comparison report
        comparison_report = self.generate_comparison_report(user_prompt, search_context)
        
        return {
            "original_query": user_prompt,
            "search_query": search_query,
            "search_context": search_context,
            "comparison_report": comparison_report
        }


def main():
    """Command-line interface for the comparison workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Compare multiple options using LLM and web search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python comparison_workflow.py Python JavaScript
  python comparison_workflow.py -c "Performance,Learning curve" React Vue.js Angular
  python comparison_workflow.py --constraints "Cost,Features" "AWS Lambda" "Google Cloud Functions"
        """
    )
    
    parser.add_argument(
        'options',
        nargs='+',
        help='Two or more options to compare'
    )
    
    parser.add_argument(
        '-c', '--constraints',
        type=str,
        help='Comma-separated list of comparison constraints'
    )
    
    args = parser.parse_args()
    
    # Validate minimum options
    if len(args.options) < 2:
        parser.error("At least 2 options are required for comparison")
    
    # Parse constraints
    constraints = None
    if args.constraints:
        constraints = [c.strip() for c in args.constraints.split(',') if c.strip()]
    
    # Run the workflow
    try:
        workflow = ComparisonWorkflow()
        result = workflow.run_comparison(args.options, constraints)
        
        # Display results
        print("=" * 60)
        print("COMPARISON WORKFLOW RESULTS")
        print("=" * 60)
        print(f"Options: {', '.join(args.options)}")
        if constraints:
            print(f"Constraints: {', '.join(constraints)}")
        print(f"Search Query: {result['search_query']}")
        print()
        print("=" * 60)
        print("COMPARISON REPORT")
        print("=" * 60)
        print(result['comparison_report'])
        
    except Exception as e:
        print(f"Error running comparison: {e}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
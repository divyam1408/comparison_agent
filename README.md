# Comparison Workflow

A Python implementation for comparing options using LLM and web search integration with Mistral AI.

## Features

- Two-stage LLM workflow: search query generation + comparison analysis
- Web search integration using Tavily for current information
- Neutral, objective comparison reports with no final recommendations
- Template-based query generation with Jinja2
- Extensible pipeline design
- Secure API key management with environment variables

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

**Option A: Using .env file (Recommended)**
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Option B: Set environment variables directly**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export HUGGINGFACE_API_KEY="your_huggingface_api_key_here"
export TAVILY_API_KEY="your_tavily_api_key_here"
```

### 3. API Key Sources
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Hugging Face API Key**: Get from [Hugging Face Settings](https://huggingface.co/settings/tokens)
- **Tavily API Key**: Get from [Tavily Console](https://app.tavily.com/)

The workflow uses `huggingface:mistralai/Mistral-7B-Instruct-v0.2` model by default.

## Usage

### Command Line Interface
```bash
# Basic comparison
python comparison_workflow.py Python JavaScript

# With constraints
python comparison_workflow.py -c "Performance,Learning curve" React Vue.js Angular

# Using shell wrapper
./run_comparison.sh "AWS Lambda" "Google Cloud Functions"
./run_comparison.sh --constraints "Cost,Features" Docker Kubernetes
```

### Python API

#### Basic Usage
```python
from comparison_workflow import ComparisonWorkflow

workflow = ComparisonWorkflow()

# Compare options with list format
options = ["Python", "JavaScript"]
result = workflow.run_comparison(options)

print(result['comparison_report'])
```

#### Advanced Usage with Constraints
```python
# Compare with specific constraints
options = ["React", "Vue.js", "Angular"]
constraints = ["Learning curve", "Performance", "Community support"]

result = workflow.run_comparison(options, constraints)
print(result['comparison_report'])
```

#### Full Result Structure
```python
result = workflow.run_comparison(["Option A", "Option B"])

# Available result keys:
# - result['original_query']: Generated comparison prompt
# - result['search_query']: Optimized web search query  
# - result['search_context']: Aggregated search results
# - result['comparison_report']: Final comparison analysis
```

## Architecture

### Core Components
- `ComparisonWorkflow`: Main pipeline orchestrator
- `generate_search_query()`: LLM call #1 - converts comparison request to search query
- `perform_web_search()`: Tavily search execution with configurable result count
- `aggregate_search_context()`: Structures search results into context
- `generate_comparison_report()`: LLM call #2 - creates final analysis
- `run_comparison()`: Complete workflow with template-based prompt generation
- `prompts.py`: Centralized prompt templates and message generation functions

### Template System
Uses Jinja2 templates for flexible prompt generation:
- Centralized in `prompts.py` for easy maintenance
- Supports multiple options in list format
- Optional constraints for focused comparisons
- Consistent formatting across different comparison types
- Helper functions for message generation

### LLM Configuration
- **Model**: `huggingface:mistralai/Mistral-7B-Instruct-v0.2`
- **Search Query Generation**: Temperature 0 (deterministic)
- **Comparison Generation**: Temperature 0.3 (slightly creative)
- **Provider**: Hugging Face via aisuite client

## Extension Points

The pipeline is designed for easy extension:
- Add reflection loops after comparison generation
- Implement result reranking and validation
- Add multiple search sources (Google, Bing, etc.)
- Include fact-checking steps
- Add custom comparison templates
- Integrate additional LLM providers

## Example Output Structure

The workflow generates structured comparisons with:
1. **Detailed Analysis**: Section-by-section comparison across dimensions
2. **Pros and Cons**: Aggregated advantages/disadvantages per option  
3. **Comparison Table**: Concise side-by-side feature comparison
4. **No Recommendations**: Neutral presentation for user decision-making

## Dependencies

- `aisuite`: Multi-provider LLM client
- `tavily-python`: Web search API client
- `jinja2`: Template engine for prompt generation
- `pydantic`: Data validation (aisuite dependency)
- `openai`: OpenAI provider support
- `huggingface_hub`: Hugging Face model access
- `transformers`: Transformer model support
- `torch`: PyTorch backend for model execution
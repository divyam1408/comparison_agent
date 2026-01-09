# Technology Stack

## Core Technologies
- **Python 3**: Primary language
- **aisuite**: Multi-provider LLM client for AI model access
- **Tavily API**: Web search integration
- **Jinja2**: Template engine for prompt generation
- **Hugging Face**: Model provider (Mistral-7B-Instruct-v0.2)

## Dependencies
```
aisuite
tavily-python
jinja2
pydantic
openai
huggingface_hub
transformers
torch
python-dotenv
```

## LLM Configuration
- **Primary Model**: `huggingface:mistralai/Mistral-7B-Instruct-v0.2`
- **Search Query Generation**: Temperature 0 (deterministic)
- **Comparison Generation**: Temperature 0.3 (slightly creative)
- **Fallback**: OpenAI API support available

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys (copy and edit .env file)
cp .env.example .env
# Edit .env with your actual API keys

# Make shell script executable
chmod +x run_comparison.sh
```

### Running Comparisons
```bash
# Python API
python3 comparison_workflow.py option1 option2

# With constraints
python3 comparison_workflow.py -c "Performance,Cost" option1 option2

# Shell wrapper
./run_comparison.sh option1 option2
./run_comparison.sh --constraints "Learning curve,Community" React Vue.js
```

### Development
```bash
# Run with Python directly
python3 -c "from comparison_workflow import ComparisonWorkflow; w = ComparisonWorkflow(); print(w.run_comparison(['A', 'B']))"
```

## API Keys
Secure environment variable configuration:
- `OPENAI_API_KEY` - Set in .env file or environment
- `HUGGINGFACE_API_KEY` - Set in .env file or environment
- `TAVILY_API_KEY` - Set in .env file or environment

**Security**: API keys are loaded from environment variables using python-dotenv, never hardcoded in source.

## Architecture Notes
- Single-file main implementation (`comparison_workflow.py`)
- Shell wrapper for convenience (`run_comparison.sh`)
- Template-based prompt generation for consistency
- Modular pipeline design for extensibility
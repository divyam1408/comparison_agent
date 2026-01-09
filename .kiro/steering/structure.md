# Project Structure

## Root Directory Layout
```
.
├── .kiro/                    # Kiro IDE configuration
│   └── steering/            # AI assistant steering rules
├── .vscode/                 # VS Code configuration
├── __pycache__/             # Python bytecode cache
├── venv/                    # Python virtual environment
├── comparison_workflow.py   # Main implementation
├── prompts.py              # Centralized prompt templates
├── run_comparison.sh        # Shell wrapper script
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Core Files

### `comparison_workflow.py`
- **Main implementation**: Core workflow logic
- **Class**: `ComparisonWorkflow` - main pipeline orchestrator
- **Methods**: 
  - `generate_search_query()` - LLM call #1
  - `perform_web_search()` - Tavily integration
  - `aggregate_search_context()` - Context preparation
  - `generate_comparison_report()` - LLM call #2
  - `run_comparison()` - Full pipeline execution
- **CLI**: Command-line interface with argparse
- **API Keys**: Hardcoded environment variable setup

### `prompts.py`
- **Prompt templates**: All LLM prompts centralized
- **Constants**: System and user prompt templates
- **Helper functions**: Message generation utilities
- **Jinja2 templates**: Main user query template with options/constraints

### `run_comparison.sh`
- Shell wrapper for convenience
- Error handling and validation
- Passes all arguments to Python script

### `requirements.txt`
- Minimal dependency list
- No version pinning (uses latest)

## Code Organization Principles

### Single-File Design
- All core logic in one Python file for simplicity
- No complex module structure needed
- Easy to understand and modify

### Pipeline Architecture
- Clear separation of workflow stages
- Each method handles one responsibility
- Easy to extend or modify individual stages

### Template-Based Prompts
- Jinja2 templates centralized in `prompts.py`
- Helper functions for message generation
- Supports dynamic option lists and constraints
- Easy to modify and maintain prompts separately

## Extension Points
- Add new methods to `ComparisonWorkflow` class
- Modify templates in `prompts.py` for different prompt styles
- Add new search providers alongside Tavily
- Implement result validation/reflection loops
- Create new prompt templates for specialized comparisons
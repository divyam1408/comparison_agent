# Product Overview

This is a **Comparison Workflow** tool that helps users make informed decisions by comparing multiple options using AI and web search.

## Core Purpose
- Generate neutral, objective comparison reports between 2+ options
- Leverage LLM reasoning combined with current web information
- Provide structured analysis without making final recommendations

## Key Features
- Two-stage LLM pipeline: search query generation → comparison analysis
- Web search integration via Tavily API for current information
- Template-based prompt generation with Jinja2
- Support for optional comparison constraints/dimensions
- Command-line interface and Python API
- Pre-configured API keys for immediate use

## Target Use Cases
- Technology stack comparisons (frameworks, languages, tools)
- Product/service evaluations
- Decision support across any domain requiring objective analysis
- Research and analysis workflows

## Design Philosophy
- **Neutral stance**: No final recommendations, just structured analysis
- **Extensible**: Pipeline designed for easy modification and enhancement
- **Current information**: Web search ensures up-to-date context
- **Structured output**: Consistent format with pros/cons, comparison tables
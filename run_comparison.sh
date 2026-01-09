#!/bin/bash

# Comparison Workflow Shell Script
# Usage: ./run_comparison.sh [OPTIONS] option1 option2 [option3 ...]
# 
# OPTIONS:
#   -c, --constraints "constraint1,constraint2,..."  Specify comparison constraints
#   -h, --help                                       Show this help message
#
# Examples:
#   ./run_comparison.sh Python JavaScript
#   ./run_comparison.sh -c "Performance,Learning curve" React Vue.js Angular
#   ./run_comparison.sh --constraints "Cost,Features" "AWS Lambda" "Google Cloud Functions"

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/comparison_workflow.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: comparison_workflow.py not found in $SCRIPT_DIR" >&2
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed." >&2
    exit 1
fi

# Run the Python script with all arguments passed through
cd "$SCRIPT_DIR"
python3 "$PYTHON_SCRIPT" "$@"
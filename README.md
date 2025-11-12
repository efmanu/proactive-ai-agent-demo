# Proactive AI Agent Demo

## Overview
A minimal demo showing a proactive AI agent implemented in Python that periodically observes system state, plans via a PydanticAI agent, and executes actions automatically.

## Features
- Lightweight agent loop: observe → plan → act
- Configurable triggers and action handlers
- Example integrations (CLI / script) to demonstrate behavior

## Prerequisites
- Python 3.10+
- pip
- Optional: a virtual environment tool (venv, virtualenv)

## Dependencies
The demo uses:
- pydantic
- pydantic-ai
- apscheduler
- any provider client required by pydantic-ai (e.g., DeepSeekProvider)

You can install requirements (create a requirements.txt if needed) or install packages manually:
pip install pydantic pydantic-ai apscheduler

## Configuration / Environment
Required environment variables:
- DEEPSEEK_API_KEY — API key for the DeepSeek provider used by the demo agent.

Export the variable before running:
Unix/macOS:
export DEEPSEEK_API_KEY="your-api-key"
Windows (PowerShell):
$env:DEEPSEEK_API_KEY="your-api-key"

## Quick setup
1. Clone repo:
   `git clone <repo-url>`
2. Create and activate a virtual environment (recommended) and install dependencies:
   `uv sync`

## Running the demo
Run the Python script:
`uv run python main.py`

The script starts an AsyncIO scheduler that runs the monitoring loop every 5 seconds (configured in main.py). The agent checks the temperature and prints status; if alert is triggered it calls send_alert (currently a console print).

## Example usage
1. Ensure DEEPSEEK_API_KEY is set.
2. Start the agent:
   python main.py
3. Observe logs like:
   [12:34:56] Temperature normal: 71.2°C
   📩 Sending alert: High temperature detected: 78.3°C

## Configuration notes
- Change the monitoring interval in main.py (AsyncIOScheduler.add_job(..., seconds=5)) to adjust polling frequency.
- The agent uses a Pydantic model (CheckResult) and a tool get_current_temperature to simulate sensor readings. Customize those for real sensors or integrations.

## Troubleshooting
- If you see import errors, confirm dependencies are installed in the active environment.
- If the provider fails, verify DEEPSEEK_API_KEY and network connectivity.




# proactive_agent.py
import random
import asyncio
import os
from datetime import datetime
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider


# Step 1: Define the schema for the agent's reasoning output
class CheckResult(BaseModel):
    temperature: float
    alert: bool
    message: str


# Step 2: Create the PydanticAI agent with reasoning logic
model = OpenAIChatModel(
    'deepseek-chat',
    provider=DeepSeekProvider(api_key=os.environ.get('DEEPSEEK_API_KEY', 'your-api-key-here')),
)

agent = Agent(
    model=model,
    name="TemperatureMonitor",
    instructions="""You are a temperature monitoring agent. Analyze the current temperature and determine:
    1. Whether an alert is needed (temperatures above 75°C are concerning)
    2. Provide an appropriate message about the temperature status
    
    Be concise and clear in your assessment.""",
    output_type=CheckResult,
)


# Step 3: Define a tool for the agent to get current temperature
@agent.tool
async def get_current_temperature(ctx: RunContext[None]) -> float:
    """Get the current system temperature reading."""
    # Simulate getting temperature from a sensor
    temp = random.uniform(60, 90)
    return temp


# Step 4: Define the proactive loop
async def monitor_loop():
    """Periodically collects context and invokes the agent."""
    try:
        # Run the agent and let it decide what to do
        result = await agent.run(
            "Check the current system temperature and determine if an alert is needed."
        )
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {result.output.message}")
        
        if result.output.alert:
            send_alert(result.output.message)
    except Exception as e:
        print(f"Error in monitoring loop: {e}")


# Step 5: Define the action layer (e.g., alert system)
def send_alert(message: str):
    """Simulate alert action (e.g., email, Slack, API call)."""
    print(f"📩 Sending alert: {message}")


# Step 6: Schedule the proactive agent
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitor_loop, "interval", seconds=5)
    scheduler.start()
    print("🚀 Proactive agent started. Monitoring system...\n")
    
    try:
        await asyncio.Event().wait()  # keep running
    except KeyboardInterrupt:
        print("\n👋 Shutting down agent...")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
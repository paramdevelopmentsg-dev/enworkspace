
from trace import Trace
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from openai import AsyncOpenAI
import os
from pydantic import BaseModel
from datetime import datetime


load_dotenv(override=True)


google_api_key = os.getenv('GOOGLE_API_KEY')


if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:6]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

@function_tool
def get_current_time():
    """
    Returns the current date and time as a string.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")



support_agent=Agent(name="support_agent",instructions="support Agent ",tools=[get_current_time],model=gemini_model)
with trace("Concierge Agent Trace"):
    response=await Runner.run(support_agent,"what is the current time")
    print(response.final_output)

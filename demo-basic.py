from trace import Trace
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, trace
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

agent=Agent(name="demo_agent",instructions="You are helpful assistant ",model=gemini_model)

response=Runner.run_sync(agent, "Write about the OpenAI SDK.")
print(response.final_output)



#basic Agent program to perform the basic query and generate the output
# Here we are using Gemini ,generate the API Key from Gemini 
# store those API key into .env 

from dotenv import load_dotenv
from agents import Agent, Runner, trace
from openai import AsyncOpenAI
import os

load_dotenv(override=True)


google_api_key = os.getenv('GOOGLE_API_KEY')


if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:6]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

instruction="generate the Travel Planner for 3 days trip to Singapore for 3 Pax and starting from 25 dec 25 and budget is low"
concierge_agent=Agent(name="concierge_agent",instructions=instruction,model=gemini_model)

response=await Runner.run(concierge_agent,"Generate the Travel Planner")

print(response.final_output)












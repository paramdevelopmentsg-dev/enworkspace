
# Generate the output from input of first one
# enable the trace to see the result 


from trace import Trace
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

instruction="list out best hotel and tourist places in singapore \
    and generate the Travel Planner for 3 days trip to Singapore for 3 Pax and starting from 25 dec 25 and budget is low"
concierge_agent=Agent(name="concierge_agent",instructions=instruction,model=gemini_model)
with trace("Concierge Agent Trace"):
    response=await Runner.run(concierge_agent,"List out best hotel and toursit places in Singapore")
    second_response=await Runner.run(concierge_agent,"Generate the Travel Planner")
    print(second_response.final_output)





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
def get_restuartents(city:str):
    " To returns the list of famous hotel from specific city  "
    " need to call the Dining API to pulls the hotels details based on the city in future "
    hotels = {
            "Paris": ["Ritz Paris", "Hotel Lutetia", "Le Meurice"],
            "London": ["The Savoy", "The Connaught", "The Langham"],
            "New York": ["The Plaza", "Mandarin Oriental", "The Ritz-Carlton"]
        }
    result = hotels.get(city, ["No hotel data available"])
    return f"Top hotels in {city}: {', '.join(result)}"



@function_tool
def financial_outcome(customer_id:str):
    " to fetch the balance based on the customer id "
    " to update the redeem and get the balance again "

    accounts = {
        "C1001": {"balance": 1200.50, "redeem_points": 150},
        "C2002": {"balance": 560.75, "redeem_points": 80},
        "C3003": {"balance": 980.00, "redeem_points": 220}
    }
    customer = accounts.get(customer_id, None)
    return (
        f"Customer {customer_id}:\n"
        f"  Balance: ${customer['balance']}\n"
        f"  Redeemable Points: {customer['redeem_points']}"
    )

routing_instruction=" if the queries related to Hotel then calls the get_restuartents \
 if the query related to balance,redeem then call the financial_outcome "

service_manager_agent=Agent(name="service_manager_agent",instructions=routing_instruction,model=gemini_model,
                    tools=[get_restuartents,financial_outcome]     )
with trace("agent manager "):
    response=await Runner.run(service_manager_agent,"what is the list of famous hotel in London   ")
    print(response.final_output)

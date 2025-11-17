from trace import Trace
from typing import List
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, trace
from openai import AsyncOpenAI
import os
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio

load_dotenv(override=True)


google_api_key = os.getenv('GOOGLE_API_KEY')


if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:6]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

class TravelPlanner(BaseModel):
    destination:str
    budget:float
    noOfDays: int
    activities: List[str]= Field (description="List of activities ")
    specialNotes: str




instructions="""
    You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can create personalized travel itineraries based on the user's interests and preferences.
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """

queries = [
        "I'm planning a trip to Singapore for 5 days with a budget of $2000. What should I do there?",
        "I want to visit Chennai for a week with a budget of $3000. What activities do you recommend?"
    ]

async def main():

    travelagent=Agent(name="travelAgent",instructions=instructions,model=gemini_model,output_type=TravelPlanner)

    for query in queries:
                print("\n" + "="*50)
                print(f"QUERY: {query}")
                
                result = await Runner.run(travelagent, query)
                
                print("\nFINAL RESPONSE:")
                travel_plan = result.final_output
                
                # Format the output in a nicer way
                print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
                print(f"Duration: {travel_plan.noOfDays} days")
                print(f"Budget: ${travel_plan.budget}")
                
                print("\n🎯 RECOMMENDED ACTIVITIES:")
                for i, activity in enumerate(travel_plan.activities, 1):
                    print(f"  {i}. {activity}")
                
                print(f"\n📝 NOTES: {travel_plan.specialNotes}")


if __name__ == "__main__":
    asyncio.run(main())

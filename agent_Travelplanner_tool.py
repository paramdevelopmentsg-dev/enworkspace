
from trace import Trace
from typing import List
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, trace
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


@function_tool
def getweather_report(city: str, date: str) -> str:
    """Get the weather forecast for a city on a specific date."""
    # In a real implementation, this would call a weather API
    weather_data = {
        "Singapore": {"sunny": 0.3, "rainy": 0.4, "cloudy": 0.3},
        "Chennai": {"sunny": 0.8, "rainy": 0.1, "cloudy": 0.1},
        "KL": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Delhi": {"sunny": 0.7, "rainy": 0.2, "cloudy": 0.1},
        "London": {"sunny": 0.2, "rainy": 0.5, "cloudy": 0.3},
        "Paris": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Tokyo": {"sunny": 0.5, "rainy": 0.3, "cloudy": 0.2},
    }
    
    if city in weather_data:
        conditions = weather_data[city]
        # Simple simulation based on probabilities
        highest_prob = max(conditions, key=conditions.get)
        temp_range = {
            "Singapore": "15-25°C",
            "Chennai": "20-30°C",
            "KL": "10-20°C",
            "Delhi": "25-35°C",
            "London": "10-18°C",
            "Paris": "12-22°C",
            "Tokyo": "15-25°C",
        }
        return f"The weather in {city} on {date} is forecasted to be {highest_prob} with temperatures around {temp_range.get(city, '15-25°C')}."
    else:
        return f"Weather forecast for {city} is not available."



instructions="""
   You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can:
    1. Provide weather information for destinations
    2. Create personalized travel itineraries
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - The weather at the destination
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """

queries = [
        "I'm planning a trip to Singapore for 5 days with a budget of $2000. What should I do there?",
        "I want to visit Chennai for a week with a budget of $3000. What activities do you recommend?"
    ]

async def main():

    travelagent=Agent(name="travelAgent",instructions=instructions,
    model=gemini_model,output_type=TravelPlanner,tools=[getweather_report])

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

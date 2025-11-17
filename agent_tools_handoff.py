
from re import T
from trace import Trace
from typing import Any, List, Optional
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, trace
from openai import AsyncOpenAI
import os
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import json
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
class Flight(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: float
    direct_flight: bool
    reason: str

class Hotel(BaseModel):
    name: str
    location: str
    price_per_night: float
    amenities: List[str]
    reason: str



@function_tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights between two cities on a specific date."""
    # In a real implementation, this would call a flight search API
    flights = []
    # Dummy data for demonstration purposes
    example_flights = [
        {
            "airline": "Air Wonder",
            "departure_time": "09:00",
            "arrival_time": "12:00",
            "price": 300.0,
            "direct_flight": True,
            "reason": f"Non-stop flight for convenience from {origin} to {destination}"
        },
        {
            "airline": "Skyways",
            "departure_time": "15:00",
            "arrival_time": "19:00",
            "price": 250.0,
            "direct_flight": False,
            "reason": f"Best value with short layover from {origin} to {destination}"
        },
    ]

    return json.dumps(flights)

@function_tool
def search_hotels(city: str, check_in: str, check_out: str, max_price: Optional[float] = None) -> str:
 
    hotel_options = [
        {
            "name": "City Center Hotel",
            "location": "Downtown",
            "price_per_night": 199.99,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant"]
        },
        {
            "name": "Riverside Inn",
            "location": "Riverside District",
            "price_per_night": 149.50,
            "amenities": ["WiFi", "Free Breakfast", "Parking"]
        },
        {
            "name": "Luxury Palace",
            "location": "Historic District",
            "price_per_night": 349.99,
            "amenities": ["WiFi", "Pool", "Spa", "Fine Dining", "Concierge"]
        }
    ]
    

    return json.dumps(hotel_options)



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
    3. Hand off to specialists for flights and hotels when needed
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - The weather at the destination
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    
    If the user asks specifically about flights or hotels, hand off to the appropriate specialist agent.
    """
flighinstructions="""
    You are a flight specialist who helps users find the best flights for their trips.
    
    Use the search_flights tool to find flight options, and then provide personalized recommendations
    based on the user's preferences (price, time, direct vs. connecting).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with flight details and prices.
    """,


hotelinstructions="""
    You are a hotel specialist who helps users find the best accommodations for their trips.
    
    Use the search_hotels tool to find hotel options, and then provide personalized recommendations
    based on the user's preferences (location, price, amenities).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with hotel details, amenities, and prices.
    """,



flights_agent=Agent[Any] (name="flight_agent",instructions=flighinstructions,output_type=Flight,
                        model=gemini_model ,tools=[search_flights])
hotel_agent=Agent(name="hotel_agent",instructions=hotelinstructions,
                        model=gemini_model,output_type=Hotel,tools=[search_hotels])


queries = [
         "I need a flight from New York to Chicago tomorrow",
        " Find me a hotel in Paris with a pool for under $300 per night"
    ]

async def main():

    travelagent=Agent(name="travelAgent",
                        instructions=instructions,
                        model=gemini_model,
                        output_type=TravelPlanner,
                        tools=[getweather_report],
                        handoffs=[flights_agent, hotel_agent])

    for query in queries:
                print("\n" + "="*50)
                print(f"QUERY: {query}")
                
                result = await Runner.run(travelagent, query)
                
                print("\nFINAL RESPONSE:")
                travel_plan = result.final_output
                print(travel_plan)


                if hasattr(result.final_output, "airline"):  # Flight recommendation
                        flight = result.final_output
                        print("\n✈️ FLIGHT RECOMMENDATION ✈️")
                        print(f"Airline: {flight.airline}")
                        print(f"Departure: {flight.departure_time}")
                        print(f"Arrival: {flight.arrival_time}")
                        print(f"Price: ${flight.price}")
                        
                        print(f"\nWhy this flight: {flight.reason}")
                
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

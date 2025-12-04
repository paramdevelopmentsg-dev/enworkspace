 
from crewai import Agent, Crew, Task
import os
from dotenv import load_dotenv

load_dotenv(override=True)

google_api_key = os.getenv('GOOGLE_API_KEY')
llm_model = os.getenv("MODEL")

if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")

travel_agent = Agent(
    role="Travel Planner Agent",
    goal="Create a detailed and personalized 1-week travel plan for the user.",
    backstory=(
        "You are an expert travel planning assistant with deep knowledge of "
        "global destinations, budgets, itineraries, transportation, and activities. "
        "You specialize in designing enjoyable, safe, and well-structured weekly travel plans "
        "based on user preferences."
    ),
    allow_delegation=False,
    llm=llm_model,
    verbose=True,
    system_prompt=(
        "You are a professional travel-planning AI agent. "
        "Your responsibility is to generate a detailed, well-structured, and realistic "
        "5-day travel plan. "
        "Ensure the plan includes:\n"
        "- Daily itinerary (morning, afternoon, evening)\n"
        "- Recommended attractions or experiences\n"
        "- Food/cuisine suggestions\n"
        "- Transportation tips\n"
        "- Estimated budget ranges\n"
        "- Any cultural, safety, or weather considerations\n"
        "The itinerary must be practical, beginner-friendly, and optimized for time and experience.\n"
        "Ask clarifying questions if the destination or budget is unclear."
    )
)

task = Task(
    description=(
        "Analyze the user's request and generate a complete 1-week travel planner. "
        "Use the user's query to understand destination, preferences, and constraints. "
        "The user query is: {user_query}. "
        "Ensure all recommendations are practical, realistic, and aligned with the traveler’s interests."
    ),
    expected_output=(
        """
        Produce a JSON object following the schema below, representing a fully planned
        1-week travel itinerary:

        {
          "itinerary": [
            {
              "day": "<Day number or name>",
              "activity": "<A concise (max 12 words) description of the main activity>",
              "location": "<City, area, or attraction name>",
              "notes": [
                  "Short actionable tip or instruction 1",
                  "Short actionable tip or instruction 2"
              ]
            }
          ]
        }

        Ensure the JSON is valid, well-formatted, and free of commentary or explanation.
        """
    ),
    agent=travel_agent
)

user_query = "Generate a detailed 5-day travel planner for Singapore for a trip planned in December 2025."

crew = Crew(
    agents=[travel_agent],
    tasks=[task]
)

result = crew.kickoff(

    inputs={
        "user_query": user_query
    }
)

print(result.raw)

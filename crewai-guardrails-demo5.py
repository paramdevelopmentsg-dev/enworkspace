
from crewai import Agent, Crew, Task
import os
from dotenv import load_dotenv
import re

load_dotenv(override=True)

google_api_key = os.getenv('GOOGLE_API_KEY')
llm_model = os.getenv("MODEL")

if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")


# Custom guardrail function
def limit_to_300_chars_guardrail(output):
    """
    Guardrail that ensures the agent output is no more than 300 characters.
    If longer, it trims the text and returns the first 300 characters.
    """
    try:
        # Extract raw output if it's a TaskOutput object
        text = output if isinstance(output, str) else output.raw
    except Exception as e:
        return (
            False,
            f"Error retrieving the raw output: {str(e)}"
        )

    # Trim to 300 characters
    trimmed = text[:600]

    # Guardrails must return (True/False, output)
    return True, trimmed


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
    verbose=True

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
              "cost": "Cost for the each activity",
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
    agent=travel_agent,
    guardrails=[limit_to_300_chars_guardrail]

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

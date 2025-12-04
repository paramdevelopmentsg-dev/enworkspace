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

travel_agent = Agent(role="YouTube Shorts Micro-History Strategist",
                     goal="Plan a 1-week slate of high-retention YouTube Shorts about surprising origins of everyday "
                          "things.",
                     backstory=(
                         "You specialize in 30–45s micro-history that hooks fast, pays off with a twist, and drives "
                         "comments."
                         "You keep ideas film able by a solo creator at home with minimal props."
                     ),
                     llm=llm_model,
                     verbose=True
                     )

booking_agent = Agent(role="Travel Booking Agent",
                      goal="Take the travel plan and generate booking confirmations with booking IDs.",
                      backstory=(
                          "You specialize in converting itineraries into confirmed bookings. "
                          "You generate unique booking IDs and ensure all itinerary days have an "
                          "associated booking reference."
                      ),
                      allow_delegation=False,
                      llm=llm_model,
                      verbose=True
                      )

task = Task(
    description=(
        "Create a 1-week video posting plan with 5 video blueprints. "
        "Platform: YouTube Shorts (vertical 9:16, 30-45s). "
        "Niche: Micro-History of Everyday Things (e.g., why pencils are yellow, origins of bubble wrap, etc.). "
        "Primary goals: 1) thumb-stop hook in first 1s, 2) crystal-clear narrative with a surprise, "
        "3) strong SEO phrasing in title/caption, 4) comment-bait CTA. "
        "Context: solo creator, home-filmable, no special gear. "
    ),
    expected_output=(
        '''
        Output a JSON array following the schema below, which contains a
        weekly schedule and 5 video blueprints. Each video blueprint should include:
        {
          "videos": [
            {
              "title": "<searchable, curiosity-driven title>",
              "hook_main": "<<=12 words, shows payoff fast>",
              "hook_alt": "<variant hook>",
              "visuals": ["simple prop or b-roll idea 1", "idea 2"],
              "tags": ["#microhistory","#everydaythings","#shorts"],
              "cta": "<question that invites comments>"
            }
          ]
        }
        '''
    ),
    agent=travel_agent
)

task_booking = Task(
    description=(
        "Take the travel plan created by the first agent and generate booking "
        "confirmations. For each itinerary day, create a booking entry with a "
        "unique booking ID. Booking IDs must follow this format: BOOK-<UUID4>."
    ),
    expected_output="""
    A JSON object with the following schema:
    {
      "bookings": [
        {
          "day": "Day 1",
          "activity": "<activity>",
          "booking_id": "BOOK-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        }
      ]
    }
    """,
    agent=booking_agent,
)


crew = Crew(
    agents=[travel_agent,booking_agent],
    tasks=[task,task_booking]
)

user_query = "Generate a detailed 5-day travel planner for Singapore for a trip planned in December 2025."
result = crew.kickoff(

    inputs={
        "user_query": user_query
    }
)


print(result.raw)


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

code_agent = Agent(
    role="Developer",

    goal=(
        "You write Python code to complete the assignment: {user_query}. "
        "First, you outline a clear plan for how the solution will work. "
        "Next, you write clean, efficient, and well-structured Python code. "
        "Then, you execute the code, verify the output, and correct any issues if needed."
    ),

    backstory=(
        "You are a seasoned Python developer known for writing high-quality, modular, "
        "and efficient code. You approach every task with clarity, precision, and "
        "strong problem-solving skills. You follow best practices related to "
        "architecture, error handling, documentation, and testing."
    ),

    allow_delegation=False,
    llm=llm_model,
    verbose=True

)

task = Task(
    description=(
        "Write Python code to accomplish the following assignment: {user_query}. "
        "Your response must strictly follow best practices in Python programming, "
        "including clear structure, readability, and correctness. "
        "Ensure the code is complete, executable, and solves the assignment fully."

    ),
    expected_output=(
        "Produce a text file containing two sections:\n"
        "1. The complete Python code necessary to solve the assignment.\n"
        "2. The output generated after executing the code.\n"
        "Both code and output must be included in the file."
    ),
    agent=code_agent,
    output_file="output/code.txt"
)

user_query = "Please write a FastAPI application that exposes Customer information as a REST API. The API should " \
             "include endpoints for creating, retrieving, updating, and deleting customer records."

crew = Crew(
    agents=[code_agent],
    tasks=[task]
)

result = crew.kickoff(

    inputs={
        "user_query": user_query
    }
)

print(result.raw)


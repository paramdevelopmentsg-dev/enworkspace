from trace import Trace
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from openai import AsyncOpenAI
import os
from pydantic import BaseModel
from datetime import datetime


load_dotenv(override=True)


google_api_key = os.getenv('GOOGLE_API_KEY')
sendgrid_api_key= os.getenv('SENDGRID_API_KEY')


if google_api_key:
    print(f"google API Key exists and begins {google_api_key[:6]}")
else:
    print("Google API Key not set - please head to the troubleshooting guide in the setup folder")


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

@function_tool
def get_current_time():
    """
    Returns the current date and time as a string.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def get_weather_report(city:str):
    " We can integrate with Whether API to get the weather report "
    return "weather is cold" 


@function_tool
def send_email(body:str,to_address:str):
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    from_email = Email("paramesh@***.com")  # Change to your verified sender
    to_email = To(to_address)  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Travel Planner", content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

instruction="What is current Time and weather report for Singapore and also generate the Travel Planner for 3 days trip to Singapore for 3 Pax and starting from 25 dec 25 and budget is low \
   final step,share the travel planner in the email , use send_email as tool to send an email and email address parameshskills@gmail.com  "

support_agent=Agent(name="support_agent",instructions=instruction,tools=[get_current_time,get_weather_report,send_email],model=gemini_model)
with trace("Concierge Agent Trace"):
    response=await Runner.run(support_agent,"what is the current time and weather report for Singapore please you generate the Travel planner also  ")
    print(response.final_output)

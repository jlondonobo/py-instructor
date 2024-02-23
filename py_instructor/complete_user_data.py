"""A script that collects user data and stores it as a JSON object."""

import os

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client = instructor.patch(openai)

# Assume I have the following conversation:

user_message = "I'm 24 years old and I'm from Medellin, Colombia."

class UserData(BaseModel):
    name: str
    age: int
    country: str
    city: str

MaybeUserData = instructor.Maybe(UserData)

# GPT3.5 hallucinates user's name 'Alice'. GPT4 does not.
user = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_model=UserData,
    messages=[
        {"role": "user", "content": user_message},
    ],
)

user._raw_response
"""A script that collects user data and stores it as a JSON object."""

import os

import instructor
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
instructor.patch(openai)
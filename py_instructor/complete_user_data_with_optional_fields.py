"""This script builds on complete_user_data.py by adding optional fields to the UserData model."""
import os
from typing import Optional

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class UserData(BaseModel):
    name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)


def extract_missing_fields(user_data: UserData) -> list[str]:
    missing = [field for field, value in user_data if value is None]
    return missing


def generate_message(openai: OpenAI, system: str, message: str) -> str:
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": message},
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
    )
    res = response.choices[0].message.content
    return res


# For now don't use history
def ask_for_missing_fields(
    client: OpenAI, current_user_data: UserData, missing_fields: list[str]
) -> str:
    current_data = current_user_data.model_dump()
    missing_fields_str = ", ".join(missing_fields)
    message = f"""
    Current data: {current_data}
    Missing fields: {missing_fields_str}
    """
    system = """
    You are a helpful assistant that's currently trying to complete a form for a user's data. Can you casually ask for the user for missing data in your conversation?
    
    For example, if Missing fields: ['age', 'country'], you can ask the user: "Hi, friend can you remind me how old you are and where you are from?"
    """

    query = generate_message(client, system, message)
    return query


def main():
    openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    client = instructor.patch(openai)

    user_message = input("Please provide your name, age, country, and city: ")
    while True:
        print(user_message)
        user = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_model=UserData,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )
        print(user)
        missing_fields = extract_missing_fields(user)
        if not missing_fields:
            break

        asking_message = ask_for_missing_fields(openai, user, missing_fields)
        new_fields = input(asking_message)
        user_message = f"Previous data: {user.model_dump()}\n New data to fill {missing_fields}: {new_fields}"
    
    print("You collected the user's data successfully!")
    print(user.model_dump())


if __name__ == "__main__":
    main()

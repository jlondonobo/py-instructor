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


def main():
    openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    client = instructor.patch(openai)

    user_message = input("Please provide your name, age, country, and city: ")
    while True:
        user = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_model=UserData,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )
        missing_fields = extract_missing_fields(user)
        if not missing_fields:
            break
        print(f"Missing fields: {missing_fields}")

        new_fields = input("Please provide the missing fields: ")
        user_message = f"{user.model_dump()}\n{new_fields}"
    print("You collected the user's data successfully!")
    print(user.model_dump())


if __name__ == "__main__":
    main()

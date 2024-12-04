from random import choice, randint
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # This is the default and can be omitted
)

def get_response(user_input: str) -> str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are roleplaying as Cypher from Valorant"
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content
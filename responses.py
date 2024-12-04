from random import choice, randint

def get_response(user_input: str) -> str:
    lowered = user_input.lower()

    if lowered.startswith("@Cypher"):
        return "Give me a corpse..."
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    """
    Responds to a Discord message with a corresponding response.

    Args:
        message (Message): The message to respond to.
        user_message (str): The content of the message to respond to.

    Returns:
        None
    """
    if not user_message:
        print("Report this error to epicgamerryt (error code: 1)")
        return

    try:
        response = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(f"Error: {e}")


# HANDLE STARTUP
@client.event
async def on_ready() -> None:
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    
    if client.user.mentioned_in(message):
        response = get_response(message)
        await send_message(message, response)

def main():
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
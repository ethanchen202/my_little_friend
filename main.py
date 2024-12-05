import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from responses import get_response, display_lol_info

# Load Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure Intents
intents = Intents.default()
intents.message_content = True

# Initialize Bot
bot = commands.Bot(command_prefix='/', intents=intents)

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
@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')


# BOT FUNCTIONALITIES
@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        message_str = message.content
        await send_message(message, message_str)

    await bot.process_commands(message)

@bot.command(name="lolinfo")
async def lolinfo(ctx, *, riot_id: str):
    """
    Responds with stats for a League of Legends player.
    """
    try:
        if "#" not in riot_id:
            await ctx.send("Invalid format! Use `/lolinfo <name>#<tag>`.")
            return
        
        riot_ign, tag = riot_id.split("#", 1)
        
        result = display_lol_info(riot_ign, tag)
        
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# MAIN
def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
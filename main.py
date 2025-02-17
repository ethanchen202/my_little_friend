import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands, Interaction, Object
from discord.ext import commands
from responses import get_response, display_lol_info, find_biased_balanced_split

# Load Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure Intents
intents = Intents.default()
intents.message_content = True

# Initialize Bot
bot = commands.Bot(command_prefix='/', intents=intents)

# tree = app_commands.CommandTree(bot)

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
        await message.channel.send(response[:2000])
    except Exception as e:
        print(f"Error: {e}")


# HANDLE STARTUP
@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')
    # Sync the slash commands to Discord
    for server in bot.guilds:
        synced = await bot.tree.sync(guild=Object(id=server.id))
        print(f"Synced {len(synced)} command(s) in {server.name}")
    print("Setup Complete.")


# BOT FUNCTIONALITIES
@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        message_str = message.content
        await send_message(message, message_str)

    await bot.process_commands(message)

# @bot.command(name="lolstats")

@bot.tree.command(name="lolstats", description="Get stats for a League of Legends player.")
async def lolstats(interaction: Interaction, riot_id: str):
    """
    Responds with stats for a League of Legends player.
    """
    try:
        if "#" not in riot_id:
            await interaction.response.send_message("Invalid format! Use `/lolstats <name>#<tag>`.", ephemeral=True)
            return
        
        riot_ign, tag = riot_id.split("#", 1)
        
        result = display_lol_info(riot_ign, tag)
        
        await interaction.response.send_message(result)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

@bot.tree.command(name="createteams", description="Creates random balanced 5v5 teams. Enter each player in the format \"<name>:<elo>\".")
async def createteams(interaction: Interaction, std: int, p1: str, p2: str, p3: str, p4: str, p5: str, p6: str, p7: str, p8: str, p9: str, p10: str):
    """
    Responds with stats for a League of Legends player.
    """
    try:
        rank_values = {
            "I4": 0, "I3": 100, "I2": 200, "I1": 300,
            "B4": 400, "B3": 500, "B2": 600, "B1": 700,
            "S4": 800, "S3": 900, "S2": 1000, "S1": 1100,
            "G4": 1200, "G3": 1300, "G2": 1400, "G1": 1500,
            "P4": 1600, "P3": 1700, "P2": 1800, "P1": 1900,
            "E4": 2000, "E3": 2100, "E2": 2200, "E1": 2300,
            "D4": 2400, "D3": 2500, "D2": 2600, "D1": 2700,
            "M4": 2800, "M3": 2900, "M2": 3000, "M1": 3100,
            "GM4": 3200, "GM3": 3300, "GM2": 3400, "GM1": 3500,
            "C4": 3600, "C3": 3700, "C2": 3800, "C1": 3900
        }
        elo_names = {
            0: "I4", 100: "I3", 200: "I2", 300: "I1",
            400: "B4", 500: "B3", 600: "B2", 700: "B1",
            800: "S4", 900: "S3", 1000: "S2", 1100: "S1",
            1200: "G4", 1300: "G3", 1400: "G2", 1500: "G1",
            1600: "P4", 1700: "P3", 1800: "P2", 1900: "P1",
            2000: "E4", 2100: "E3", 2200: "E2", 2300: "E1",
            2400: "D4", 2500: "D3", 2600: "D2", 2700: "D1",
            2800: "M4", 2900: "M3", 3000: "M2", 3100: "M1",
            3200: "GM4", 3300: "GM3", 3400: "GM2", 3500: "GM1",
            3600: "C4", 3700: "C3", 3800: "C2", 3900: "C1"
        }
        elo_symbol_to_name = {
            "I4": "Iron 4", "I3": "Iron 3", "I2": "Iron 2", "I1": "Iron 1",
            "B4": "Bronze 4", "B3": "Bronze 3", "B2": "Bronze 2", "B1": "Bronze 1",
            "S4": "Silver 4", "S3": "Silver 3", "S2": "Silver 2", "S1": "Silver 1",
            "G4": "Gold 4", "G3": "Gold 3", "G2": "Gold 2", "G1": "Gold 1",
            "P4": "Platinum 4", "P3": "Platinum 3", "P2": "Platinum 2", "P1": "Platinum 1",
            "E4": "Emerald 4", "E3": "Emerald 3", "E2": "Emerald 2", "E1": "Emerald 1",
            "D4": "Diamond 4", "D3": "Diamond 3", "D2": "Diamond 2", "D1": "Diamond 1",
            "M4": "Master 4", "M3": "Master 3", "M2": "Master 2", "M1": "Master 1",
            "GM4": "Grandmaster 4", "GM3": "Grandmaster 3", "GM2": "Grandmaster 2", "GM1": "Grandmaster 1",
            "C4": "Challenger 4", "C3": "Challenger 3", "C2": "Challenger 2", "C1": "Challenger 1"
        }
        players = []

        ign1, elo1 = p1.split(":")
        ign2, elo2 = p2.split(":")
        ign3, elo3 = p3.split(":")
        ign4, elo4 = p4.split(":")
        ign5, elo5 = p5.split(":")
        ign6, elo6 = p6.split(":")
        ign7, elo7 = p7.split(":")
        ign8, elo8 = p8.split(":")
        ign9, elo9 = p9.split(":")
        ign10, elo10 = p10.split(":")

        players.append((ign1, int(rank_values[elo1])))
        players.append((ign2, int(rank_values[elo2])))
        players.append((ign3, int(rank_values[elo3])))
        players.append((ign4, int(rank_values[elo4])))
        players.append((ign5, int(rank_values[elo5])))
        players.append((ign6, int(rank_values[elo6])))
        players.append((ign7, int(rank_values[elo7])))
        players.append((ign8, int(rank_values[elo8])))
        players.append((ign9, int(rank_values[elo9])))
        players.append((ign10, int(rank_values[elo10])))
        
        team1, team2 = find_biased_balanced_split(players, std)

        result = "Randomly Selected Teams:\n"

        result += "Team 1:\n"
        for player in team1:
            result += f"**{player[0]}** - Elo: {elo_symbol_to_name[elo_names[player[1]]]}\n"
        result += f"Average elo: {elo_symbol_to_name[elo_names[(sum(p[1] for p in team1) / 5) // 100 * 100]]}\n"

        result += "\nTeam 2:\n"
        for player in team2:
            result += f"**{player[0]}** - Elo: {elo_symbol_to_name[elo_names[player[1]]]}\n"
        result += f"Average elo: {elo_symbol_to_name[elo_names[(sum(p[1] for p in team2) / 5) // 100 * 100]]}\n"

        await interaction.response.send_message(result)
    except KeyError:
        await interaction.response.send_message("Invalid format! Use the format `<name>:<elo>` for players.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)


# MAIN
def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
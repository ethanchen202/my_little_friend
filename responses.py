from dotenv import load_dotenv
import requests
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
RIOT_GAMES_API_KEY = os.getenv("RIOT_GAMES_API_KEY")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def get_acc_info(riot_ign: str, tag: str):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_ign}/{tag}"
    headers = {"X-Riot-Token": RIOT_GAMES_API_KEY}
    response = requests.get(url, headers=headers)
    # print(f'acc info: {response.json()}')
    if response.status_code != 200:
        return None
    return response.json()

def get_summoner_info(puuid: str):
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_GAMES_API_KEY}
    response = requests.get(url, headers=headers)
    # print(f'summoner info: {response.json()}')
    if response.status_code != 200:
        return None
    return response.json()

def get_lol_info(summoner_id: str):
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": RIOT_GAMES_API_KEY}
    response = requests.get(url, headers=headers)
    # print(f'lol info: {response.json()}')
    # print(response.status_code)
    if response.status_code != 200:
        return None
    return response.json()

def display_lol_info(riot_ign: str, tag: str) -> str:
    acc_info = get_acc_info(riot_ign, tag)

    if acc_info == None:
        return "Seems like I don't have access to that data."

    summoner_info = get_summoner_info(acc_info["puuid"])

    if summoner_info == None:
        return "Seems like I don't have access to that data."
    
    lol_info = get_lol_info(summoner_info["id"])

    if lol_info == None:
        return "Seems like I don't have access to that data."

    if lol_info == []:
        return "No data was found"
    
    output = f"Stats for {riot_ign}#{tag}:\n\n" \
            f"Rank: {lol_info[0]['tier']} {lol_info[0]['rank']}\n" \
            f"LP: {lol_info[0]['leaguePoints']}\n" \
            f"Wins: {lol_info[0]['wins']}\n" \
            f"Losses: {lol_info[0]['losses']}\n" \
            f"Winrate: {round(lol_info[0]['wins'] / (lol_info[0]['wins'] + lol_info[0]['losses']), 3) * 100}%"

    return output

def get_response(user_input: str) -> str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are roleplaying as Cypher from Valorant."
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        model="gpt-4o-mini",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print(display_lol_info("devourer of dogs", "asian"))
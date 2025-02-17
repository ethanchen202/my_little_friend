from dotenv import load_dotenv
import requests
import os
import random
import math
from itertools import combinations
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
RIOT_GAMES_API_KEY = os.getenv("RIOT_GAMES_API_KEY")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=os.getenv("OPENROUTER_API_KEY"),
# )

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

def get_live_tft_info(puuid: str):
    url = f"https://na1.api.riotgames.com/lol/spectator/tft/v5/active-games/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_GAMES_API_KEY}
    response = requests.get(url, headers=headers)
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

def live_game_info(riot_ign: str, tag: str):
    acc_info = get_acc_info(riot_ign, tag)

    if acc_info == None:
        return "Seems like I don't have access to that data."
    
    puuid = acc_info["puuid"]

    live_tft_info = get_live_tft_info(puuid)

    if live_tft_info == None:
        return "Seems like I don't have access to that data."
    
    return live_tft_info


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
    # print(f"Asked deepseek: {user_input[22:]}")
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         # {
    #         #     "role": "system",
    #         #     "content": "You are roleplaying as Cypher from Valorant."
    #         # },
    #         {
    #             "role": "user",
    #             "content": user_input,
    #         },
    #     ],
    #     model="deepseek/deepseek-r1:free",
    # )

    return chat_completion.choices[0].message.content

def normal_distribution(x, sigma=100):
    """
    Computes a probability weight based on a normal distribution centered at 0.
    
    :param x: Elo difference.
    :param sigma: Standard deviation of the distribution. Higher sigma allows larger differences more often.
    :return: A probability weight (not normalized).
    """
    return math.exp(- (x ** 2) / (2 * sigma ** 2))

def find_biased_balanced_split(players, sigma=100):
    """
    Finds a random split of 10 players (each with IGN and Elo) into two teams of 5,
    biased towards lower Elo differences.
    
    :param players: A list of tuples (IGN, Elo).
    :param sigma: Standard deviation for the normal distribution controlling bias strength.
    :return: A tuple (team1, team2), where each team is a list of (IGN, Elo) pairs.
    """
    assert len(players) == 10, "There must be exactly 10 players."
    
    team_splits = []
    weights = []
    
    # Generate all possible ways to choose 5 players out of 10
    for team1 in combinations(players, 5):
        team2 = tuple(set(players) - set(team1))  # The other 5 players
        
        # Calculate Elo difference
        weighted_diff = abs(sum(p[1] ** 1.5 for p in team1) - sum(p[1] ** 1.5 for p in team2))
        
        weight = normal_distribution(weighted_diff, sigma)  # Compute probability weight
        team_splits.append((team1, team2))
        weights.append(weight)
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    # Select a team assignment using weighted probabilities
    chosen_index = random.choices(range(len(team_splits)), weights=normalized_weights, k=1)[0]
    
    return team_splits[chosen_index]


if __name__ == "__main__":
    # Example usage
    players = [
        ("Alice", 1200), ("Bob", 1500), ("Charlie", 1600), ("David", 1700), ("Eve", 1800),
        ("Frank", 1900), ("Grace", 2000), ("Hank", 2100), ("Ivy", 2200), ("Jack", 2300)
    ]

    team1, team2 = find_biased_balanced_split(players)

    # Print results
    print("\nRandomly Selected Teams:")
    print("\nTeam 1:")
    for player in team1:
        print(f"{player[0]} - Elo: {player[1]}")
    print(f"Total Elo: {sum(p[1] for p in team1)}")

    print("\nTeam 2:")
    for player in team2:
        print(f"{player[0]} - Elo: {player[1]}")
    print(f"Total Elo: {sum(p[1] for p in team2)}")

    print("\nElo Difference:", abs(sum(p[1] for p in team1) - sum(p[1] for p in team2)))
import pickle
import requests
import time

API_key = "RGAPI-f2a980f9-ea4d-4811-9027-d6d055a2ebfe"
with open ("./puuids/CHALLENGER Players", "rb") as players:
    challengers = pickle.load(players)

with open ("./puuids/GRANDMASTER Players", "rb") as players:
    grandmasters = pickle.load(players)

def matches(puuids): 

    matches=[]

    for puuid in puuids:
        start=0
        print(puuid)
        while True:
            URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime=1623891600&endTime=1636902000&type=ranked&start={start}&count=100&api_key={API_key}"
            match = requests.get(URL)

            if match.status_code == 429:
                print("Rate limit exceeded")
                time.sleep(120)
                print("Wake up")
                match = requests.get(URL)

            if len(match.json()) == 0:
                break

            matches += match.json()
            start +=100
    
    return matches

matches = matches(challengers)

with open(f"./Matches/CHALLENGER", "wb") as matchLists:
        pickle.dump(matches, matchLists)

# matches = matches(grandmasters)

# with open(f"./Matches/GRANDMASTER", "wb") as matchLists:
#         pickle.dump(matches, matchLists)
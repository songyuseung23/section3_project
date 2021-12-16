from os import PathLike
import requests
import json
import pickle
import time

# league of legend API key
# !!! EVERY DAY EXPIRED !!!
API_key = "RGAPI-f2a980f9-ea4d-4811-9027-d6d055a2ebfe"

# request for list of players in specific tier
def GetPlayers1(tier):

    playerList = []
    page = 1
    while True:

        players = requests.get(f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/I?page={page}&api_key={API_key}")
        if not players.json():
            print("stop")
            break

        for player in players.json():
            playerList.append(player["summonerId"])
        
        page+=1

    return playerList

def GetSummonerPuuid2(playerList):
    
    puuids = []
    for summoner_id in playerList:
        URL = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={API_key}"
        
        puuid = requests.get(URL)
        if puuid.status_code == 429:
            print("Rate limit exceeded")
            time.sleep(120)
            print("Wake up")
            puuid = requests.get(URL)
        
        if not puuid:
            print("no such player id")
            continue
        
        puuids.append(puuid.json()["puuid"])
            
    return puuids


    pass

def pickling(tier, playerList, folder):
    
    with open(f"./{folder}/{tier} Players", "wb") as players:
        pickle.dump(playerList, players)

# pickling player list

for tier in ["CHALLENGER", "GRANDMASTER","MASTER"]:
    # get players from API1
    playerList = GetPlayers1(tier)
    pickling(tier, playerList, "Players")

with open ("./Players/CHALLENGER Players", "rb") as players:
    challengers = pickle.load(players)

with open ("./Players/GRANDMASTER Players", "rb") as players:
    grandmasters = pickle.load(players)

with open ("./Players/MASTER Players", "rb") as players:
    masters = pickle.load(players)

# get puuid from player list
challengers = GetSummonerPuuid2(challengers)
pickling("CHALLENGER", challengers, "puuids")
print("challengers done")

grandmasters = GetSummonerPuuid2(grandmasters)
pickling("GRANDMASTER", grandmasters, "puuids")
print("grandmasters done")

# masters = GetSummonerPuuid2(masters)
# pickling("MASTER", masters, "puuids")
# print("masters done")

# pickling puuid list store.











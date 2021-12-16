# for every day matching data 

from pymongo import MongoClient
from bson import json_util
import pickle
import requests
import time

API_key = "RGAPI-da570f6b-0f1e-4476-9433-1dcb624cae50" 

# variables to connect db
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
DB_NAME = "LeagueOfLegend"
COLLECTION_NAME = "matchData"

with open ("./Matches/CHALLENGER", "rb") as players:
    challengers = pickle.load(players)

with open ("./Matches/GRANDMASTER", "rb") as players:
    grandmasters = pickle.load(players)

challengers = list(set(challengers))
grandmasters = list(set(grandmasters))

# db connection
connection = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
collection = connection[DB_NAME][COLLECTION_NAME]

def insertToDB(matches):

    for matchId in matches:

        URL = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={API_key}"
        match = requests.get(URL)

        print(matchId, match.status_code)
        if match.status_code == 429:
            print("Rate limit exceeded")
            time.sleep(120)
            print("Wake up")
            match = requests.get(URL)

        collection.insert_one(match.json())

# 이부분 나눠서 반복 challengers 반 -> grandmaster 시도 예상시간: 챌 : 26 / 그마 : 52시간 총 약 3일
# insertToDB(challengers[77315:])
# print("complete challengers half")




import sqlite3
from pymongo import MongoClient

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
DB_NAME = "LeagueOfLegend"
COLLECTION_NAME = "matchData"

connection = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
collection = connection[DB_NAME][COLLECTION_NAME]

# rdb connection
conn = sqlite3.connect("lolDB.db")
cur = conn.cursor()

def initRdbTable(cur):

    sql = """CREATE TABLE IF NOT EXISTS matchResult(MatchId PRIMARY KEY NOT NULL CHAR, 
    BlueTotalDeal INTEGER, BlueTotalGold INTEGER, BlueTotalVisionScore INTEGER, BlueTotalLevel INTEGER, 
    BlueBaronKills INTEGER, BlueChampionKills INTEGER, BlueDragonKills INTEGER, BlueInhibitorKills INTEGER, 
    BlueRiftHeraldKills INTEGER, BlueTowerKills INTEGER,
    RedTotalDeal INTEGER, RedTotalGold INTEGER, RedTotalTowerDeal INTEGER, RedTotalVisionScore INTEGER, RedTotalLevel INTEGER,
    RedBaronKills INTEGER, RedChampionKills INTEGER, RedDragonKills INTEGER, RedInhibitorKills INTEGER, 
    RedRiftHeraldKills INTEGER, RedTowerKills INTEGER
    """
    cur.execute(sql)

def extract(document, cur, conn):
    
    # team statistics
    for teamData in document["info"]["teams"]:

        baronKills = teamData["objectives"]["baron"]["kills"]
        championKills = teamData["objectives"]["champion"]["kills"]
        dragonKills = teamData["objectives"]["dragon"]["kills"]
        inhibitorKills = teamData["objectives"]["inhibitor"]["kills"]
        riftHeraldKills = teamData["objectives"]["riftHerald"]["kills"]
        towerKills = teamData["objectives"]["tower"]["kills"]

    # indivdual statistics'
    blueTotalDeal = 0
    blueTotalGold = 0
    blueTotalVisionScore = 0
    blueTotalLevel = 0

    for participant in document["info"]["participants"][:5]:

        # blue team id 100
        blueTotalDeal += participant["totalDamageDealtToChampions"]
        blueTotalGold += participant["goldEarned"]
        blueTotalLevel += participant["champLevel"]
        blueTotalVisionScore += participant["visionScore"]

    redTotalDeal = 0
    redTotalGold = 0
    redTotalVisionScore = 0
    redTotalLevel = 0

    for participant in document["info"]["participants"][5:]:

        # red team id 200
        redTotalDeal += participant["totalDamageDealtToChampions"]
        redTotalGold += participant["goldEarned"]
        redTotalLevel += participant["champLevel"]
        redTotalVisionScore += participant["visionScore"]
        
    matchId = document["metadata"]["matchId"]
    cur.execute("INSERT INTO matchResult VALUES ()")

documents = collection.find({"info.gameMode" : 'CLASSIC'})

for document in documents:
    
    extract(document)

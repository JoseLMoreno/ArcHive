import sqlalchemy as sa
import urllib

engine = sa.create_engine("mssql+pyodbc://ArcHive:5413314863@adb-dev.ckbkxdyb9mdd.us-west-2.rds.amazonaws.com:1433/ArcHive?driver=SQL+Server")
# db = engine.raw_connection().connection

def AddGame(*args):
    db = engine.raw_connection().connection 
    cursor = db.cursor()
    print(*args)
    cursor.execute("""INSERT INTO Games (ReplayFile, PlayerOne, PlayerTwo, Victor, Score, GameLength, PlayerOneRace, PlayerTwoRace)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", *args)
    

def PostGame(obs):
    ReplayFile = 'Not Implemented'
    PlayerOne = 1
    PlayerTwo = None
    Victor = None
    if obs.reward == -1:
        Victor = 0
    elif obs.reward ==1:
        Victor = 1
    Score = obs.observation['score_cumulative'][0]
    GameLength = obs.observation['game_loop'][0]
    PlayerOneRace = 'T'
    PlayerTwoRace = 'R'
    AddGame([ReplayFile, PlayerOne, PlayerTwo, Victor, Score, GameLength, PlayerOneRace, PlayerTwoRace])
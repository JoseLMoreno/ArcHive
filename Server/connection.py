import sqlalchemy as sa
import urllib

engine = sa.create_engine("mssql+pyodbc://ArcHive:5413314863@adb-dev.ckbkxdyb9mdd.us-west-2.rds.amazonaws.com:1433/ArcHive?driver=SQL+Server")
# db = engine.raw_connection().connection

def AddGame(*args):
    db = engine.raw_connection().connection 
    cursor = db.cursor()
    print(*args)
    # cursor.execute("""INSERT INTO Games (ReplayFile, PlayerOne, PlayerTwo, Victor, Score, GameLength, PlayerOneRace, PlayerTwoRace)
    # VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", *args)
    cursor.execute("{CALL AddGame (?, ?, ?, ?, ?, ?, ?, ?)}""", *args)
    cursor.commit()

def PostGame(obs, agent):
    ReplayFile = 'Not Implemented'
    PlayerOne = agent
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
    try:
        AddGame([ReplayFile, PlayerOne, PlayerTwo, Victor, int(Score), int(GameLength), PlayerOneRace, PlayerTwoRace])
    finally:
        pass

def GameHistory(name):
    request = """
    SELECT * FROM dbo.Games
    WHERE PlayerOne in (
        SELECT AgentID FROM Agents
        WHERE AgentDescription = ?
    )"""
    db = engine.raw_connection().connection 
    cursor = db.cursor()
    cursor.execute(request, name)
    history = cursor.fetchall()

    return history

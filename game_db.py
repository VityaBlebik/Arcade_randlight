import sqlite3 


db = sqlite3.connect("database/game_db.sqlite")
cur = db.cursor()


def start():
    cur.execute('''CREATE TABLE IF NOT EXISTS levels_statistics (
    id            INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL,
    level_1_time  REAL    NOT NULL
                          DEFAULT (0),
    level_2_time  REAL    NOT NULL
                          DEFAULT (0),
    level_3_time  REAL    NOT NULL
                          DEFAULT (0),
    level_1_score INTEGER NOT NULL
                          DEFAULT (0),
    level_2_score INTEGER NOT NULL
                          DEFAULT (0),
    level_3_score INTEGER DEFAULT (0) 
                          NOT NULL
);''')
    db.commit()

def add_time(time, level):
    if cur.execute(f"SELECT level_{level}_time FROM levels_statistics").fetchone() == None:
        cur.execute(f"INSERT INTO levels_statistics (level_{level}_time) VALUES ({time})")   
        db.commit()
    elif cur.execute(f"SELECT level_{level}_time FROM levels_statistics").fetchone()[0] < time:
        cur.execute(f"UPDATE levels_statistics SET level_{level}_time = {time}")
        db.commit()

    """В будущем для очков"""
    # if cur.execute(f"SELECT level_{level}_score FROM levels_statistics").fetchone()[0] < score:
    #     cur.execute(f"UPDATE levels_statistics SET level_{level}_score = {score}")
    #     db.commit()

def get_time(level):
    return cur.execute(f"SELECT level_{level}_time FROM levels_statistics").fetchone()


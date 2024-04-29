import re
import sqlite3

import chess.pgn

# connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("chess_games.db")

c = conn.cursor()


def parse_pgn(file_path):
    with open(file_path) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # end of file

            # extract headers
            headers = game.headers
            event = headers.get("Event", "")
            site = headers.get("Site", "")
            date = headers.get("Date", "")
            round = headers.get("Round", "")
            white = headers.get("White", "")
            black = headers.get("Black", "")
            result = headers.get("Result", "")
            utc_date = headers.get("UTCDate", "")
            utc_time = headers.get("UTCTime", "")
            white_elo = headers.get("WhiteElo", "")
            black_elo = headers.get("BlackElo", "")
            white_rating_diff = headers.get("WhiteRatingDiff", "")
            black_rating_diff = headers.get("BlackRatingDiff", "")
            white_title = headers.get("WhiteTitle", "")
            eco = headers.get("ECO", "")
            opening = headers.get("Opening", "")
            time_control = headers.get("TimeControl", "")
            termination = headers.get("Termination", "")

            # insert into db
            game_data = (
                event,
                site,
                date,
                round,
                white,
                black,
                result,
                utc_date,
                utc_time,
                white_elo,
                black_elo,
                white_rating_diff,
                black_rating_diff,
                white_title,
                eco,
                opening,
                time_control,
                termination,
            )

            game_id = insert_into_games(c, game_data)
            node = game
            move_number = 1
            while not node.is_end():
                next_node = node.variation(0)
                move = str(next_node.move)

                # rxtract evaluation and clock time from comment
                comment = next_node.comment
                eval_match = re.search(r"\[%eval ([^\]]+)\]", comment)
                clock_match = re.search(r"\[%clk ([^\]]+)\]", comment)
                evaluation = eval_match.group(1) if eval_match else None
                clock = clock_match.group(1) if clock_match else None

                # insert moves into db
                move_data = (game_id, move_number, move, evaluation, clock)
                insert_into_moves(c, move_data)

                node = next_node
                move_number += 1


# create games table
c.execute("""
CREATE TABLE IF NOT EXISTS games (
  id INTEGER PRIMARY KEY,
  event TEXT,
  site TEXT,
  date TEXT,
  round TEXT,
  white TEXT,
  black TEXT,
  result TEXT,
  utc_date TEXT,
  utc_time TEXT,
  white_elo INTEGER,
  black_elo INTEGER,
  white_rating_diff INTEGER,
  black_rating_diff INTEGER,
  white_title TEXT,
  eco TEXT,
  opening TEXT,
  time_control TEXT,
  termination TEXT
)
""")

# create moves table
c.execute("""
CREATE TABLE IF NOT EXISTS moves (
  id INTEGER PRIMARY KEY,
  game_id INTEGER,
  move_number INTEGER,
  move TEXT,
  evaluation REAL,
  clock TEXT,
  FOREIGN KEY(game_id) REFERENCES games(id)
)
""")


def insert_into_games(c, data):
    c.execute(
        """
    INSERT INTO games (event, site, date, round, white, black, result, utc_date, utc_time, white_elo, black_elo, white_rating_diff, black_rating_diff, white_title, eco, opening, time_control, termination) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        data,
    )
    return c.lastrowid


def insert_into_moves(c, data):
    c.execute(
        """
    INSERT INTO moves (game_id, move_number, move, evaluation, clock) 
    VALUES (?, ?, ?, ?, ?)
    """,
        data,
    )


def delete_moves(c, game_id):
    c.execute(
        """
        DELETE FROM moves 
        WHERE game_id = ?
        """,
        (game_id,),
    )


def delete_game(c, game_id):
    # First delete all moves associated with the game
    delete_moves(c, game_id)

    # Then delete the game itself
    c.execute(
        """
        DELETE FROM games 
        WHERE id = ?
        """,
        (game_id,),
    )


def output_tables(c):
    # output games table
    c.execute("SELECT * FROM games")
    print("Games:")
    for row in c.fetchall():
        print(row)

    # output moves table
    c.execute("SELECT * FROM moves")
    print("\nMoves:")
    for row in c.fetchall():
        print(row)


output_tables(c)

# save changes
conn.commit()

# close db connection
conn.close()

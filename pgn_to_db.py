import re
import sqlite3
from multiprocessing import Pool

import chess.pgn
from alive_progress import alive_bar

from split_file import split_file

# connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("chess_games.db")

c = conn.cursor()


def process_game(game):
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

    moves_data = []
    node = game
    move_number = 1
    while not node.is_end():
        next_node = node.variation(0)
        move = str(next_node.move)

        # extract evaluation and clock time from comment
        comment = next_node.comment
        eval_match = re.search(r"\[%eval ([^\]]+)\]", comment)
        clock_match = re.search(r"\[%clk ([^\]]+)\]", comment)
        evaluation = eval_match.group(1) if eval_match else None
        clock = clock_match.group(1) if clock_match else None

        move_data = (move_number, move, evaluation, clock)
        moves_data.append(move_data)

        node = next_node
        move_number += 1

    return game_data, moves_data


def parse_pgn(file_path):
    count = 0
    with alive_bar(4000000) as bar:
        with Pool() as pool, open(file_path) as pgn:
            game = chess.pgn.read_game(pgn)
            while game is not None:
                count += 1
                pool.apply_async(process_and_insert_game, (game,))
                game = chess.pgn.read_game(pgn)
                bar()
                if count % 25 == 0:  # save every 25 games
                    conn.commit()


def process_and_insert_game(game):
    game_data, moves_data = process_game(game)
    with conn:
        game_id = insert_into_games(c, game_data)
        for move_data in moves_data:
            move_data = (game_id,) + move_data
            insert_into_moves(c, move_data)


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


def output_tables(c, table):
    if table == 0:
        # output games table
        c.execute("SELECT * FROM games")
        print("Games:")
        for row in c.fetchall():
            print(row)
    elif table == 1:
        # output moves table
        c.execute("SELECT * FROM moves")
        print("\nMoves:")
        for row in c.fetchall():
            print(row)


if __name__ == "__main__":
    # load and find number of lines in the file
    file = "lichess/lichess_db_standard_rated_2014-09.pgn"
    with open(file) as f:
        num_lines = sum(1 for line in f)

    if num_lines > 4000000:
        print("The file is too large to be processed splitting it into parts.")
        num_lines = num_lines // 4000000
        split_file(file, num_lines)  # split the file into parts
    for i in range(num_lines):
        print(f"Parsing part: {i+1}")
        parse_pgn(f"lichess/lichess_db_standard_rated_2014-09.pgn_part{i+1}")

    # close db connection
    conn.close()

import sqlite3


class DBConnector:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)

    def _connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def _disconnect(self):
        if self.connection:
            self.connection.close()

    def create_games_table(self):
        c = self.conn.cursor()
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
            termination TEXT,
            moves TEXT
        )
        """)
        self.conn.commit()

    def create_moves_table(self):
        c = self.conn.cursor()
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
        self.conn.commit()

    def insert_move(self, game_id, move_number, move, evaluation, clock):
        query = f"INSERT INTO moves (game_id, move_number, move, evaluation, clock) VALUES ({game_id}, {move_number}, '{move}', {evaluation}, '{clock}')"
        self.execute_query(query)

    def fetch_moves(self, game_id):
        query = f"SELECT * FROM moves WHERE game_id = {game_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def display_all_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def display_previous_games(self):
        query = "SELECT * FROM games"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def fetch_move_history(self, game_id):
        query = f"SELECT * FROM moves WHERE game_id = {game_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def delete_game(self, game_id):
        query = f"DELETE FROM games WHERE id = {game_id}"
        self.execute_query(query)

    def find_game_rating(self, game_id):
        query = f"SELECT white_elo, black_elo FROM games WHERE id = {game_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def insert_game(
        self,
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
        moves,
    ):
        query = f"INSERT INTO games (event, site, date, round, white, black, result, utc_date, utc_time, white_elo, black_elo, white_rating_diff, black_rating_diff, white_title, eco, opening, time_control, termination, moves) VALUES ('{event}', '{site}', '{date}', '{round}', '{white}', '{black}', '{result}', '{utc_date}', '{utc_time}', {white_elo}, {black_elo}, {white_rating_diff}, {black_rating_diff}, '{white_title}', '{eco}', '{opening}', '{time_control}', '{termination}', '{moves}')"
        self.execute_query(query)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

import sqlite3


class DBConnector:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(database)

    def connect(self):
        """
        Connects to the database.
        """
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connection.commit()

    def disconnect(self):
        """
        Disconnects from the database.
        """
        if self.connection:
            self.connection.close()

    # * NEA methods

    def display_all_tables(self):
        """
        Retrieves and returns all tables from the database.

        Returns:
            list: A list of tuples representing the tables.
        """
        query = "SELECT * FROM sqlite_master WHERE name='players' "

        cursor = self.cursor.execute(query)
        return cursor.fetchall()

    def create_table(self, table_name, columns):
        c = self.conn.cursor()

        # Create a string that defines the column names for the SQL command
        cols = ", ".join(columns)

        # Create the table
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")

        self.conn.commit()

    def display_previous_games(self):
        """
        Retrieves and returns all previous games from the database.

        Returns:
            list: A list of tuples representing the previous games.
        """
        query = "SELECT * FROM games"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def fetch_move_history(self, game_id):
        """
        Retrieves and returns the move history for a specific game from the database.

        Args:
            game_id (int): The ID of the game.

        Returns:
            list: A list of tuples representing the move history.
        """
        query = f"SELECT * FROM moves WHERE game_id = {game_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def delete_game(self, game_id):
        """
        Deletes a game from the database.

        Args:
            game_id (int): The ID of the game.
        """
        query = f"DELETE FROM games WHERE game_id = {game_id}"
        self.execute_query(query)

    def find_game_rating(self, game_id):
        """
        Retrieves and returns the rating of a specific game from the database.

        Args:
            game_id (int): The ID of the game.

        Returns:
            list: A list of tuples representing the game rating.
        """
        query = f"SELECT rating FROM games WHERE game_id = {game_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def find_player_rating(self, player_id):
        """
        Retrieves and returns the rating of a specific player from the database.

        Args:
            player_id (int): The ID of the player.

        Returns:
            list: A list of tuples representing the player rating.
        """
        query = f"SELECT rating FROM players WHERE player_id = {player_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def insert_game(self, game_id, player_1_id, player_2_id, winner_id, rating):
        """
        Inserts a new game into the database.

        Args:
            game_id (int): The ID of the game.
            player_1_id (int): The ID of player 1.
            player_2_id (int): The ID of player 2.
            winner_id (int): The ID of the winner.
            rating (int): The rating of the game.
        """
        query = f"INSERT INTO games (game_id, player_1_id, player_2_id, winner_id, rating) VALUES ({game_id}, {player_1_id}, {player_2_id}, {winner_id}, {rating})"
        self.execute_query(query)

    def count_games(self, player_1_id, player_2_id):
        """
        Counts the number of games between two players in the database.

        Args:
            player_1_id (int): The ID of player 1.
            player_2_id (int): The ID of player 2.

        Returns:
            list: A list of tuples representing the count of games.
        """
        query = f"SELECT COUNT(*) FROM Games WHERE player_1_id = {player_2_id} OR player_2_id = {player_1_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def calc_winrate(self, player_1_id):
        """
        Calculates and returns the win rate of a specific player from the database.

        Args:
            player_1_id (int): The ID of the player.

        Returns:
            list: A list of tuples representing the win rate.
        """
        query = f"SELECT COUNT(*) FROM games WHERE winner_id = {player_1_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def longest_moves(self, player_id):
        """
        Retrieves and returns the maximum move number for a specific player from the database.

        Args:
            player_id (int): The ID of the player.

        Returns:
            list: A list of tuples representing the maximum move number.
        """
        query = f"SELECT MAX(move_number) FROM moves WHERE player_id = {player_id}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def insertGame(self, game_id, player_1_id, player_2_id, winner_id, rating):
        query = f"INSERT INTO Games (game_id, player_1_id, player_2_id, winner_id, rating) VALUES ({game_id}, {player_1_id}, {player_2_id}, {winner_id}, {rating})"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


if __name__ == "__main__":
    db = DBConnector("chess.db")
    db.connect()
    # create games table
    db.create_table("games", ["column1", "column2", "column3"])
    db.insert_game(1, 1, 2, 1, 1)
    print(db.display_all_tables())

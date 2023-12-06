import sqlite3


class DBConnector:
    """
    A class that represents a database connector.

    Attributes:
        host (str): The host of the database.
        user (str): The username for the database.
        password (str): The password for the database.
        database (str): The name of the database.

    Methods:
        connect(): Connects to the database.
        disconnect(): Disconnects from the database.
        create_table(): Creates the necessary tables for the project.
        display_previous_games(): Retrieves and returns all previous games from the database.
        fetch_move_history(game_id): Retrieves and returns the move history for a specific game from the database.
        delete_game(game_id): Deletes a game from the database.
        find_game_rating(game_id): Retrieves and returns the rating of a specific game from the database.
        find_player_rating(player_id): Retrieves and returns the rating of a specific player from the database.
        insert_game(game_id, player_1_id, player_2_id, winner_id, rating): Inserts a new game into the database.
        count_games(player_1_id, player_2_id): Counts the number of games between two players in the database.
        calc_winrate(player_1_id): Calculates and returns the win rate of a specific player from the database.
        longest_moves(player_id): Retrieves and returns the maximum move number for a specific player from the database.
    """

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        Connects to the database.
        """
        self.connection = sqlite3.connect(self.database)

    def disconnect(self):
        """
        Disconnects from the database.
        """
        if self.connection:
            self.connection.close()

    # * NEA methods

    def create_table(self):
        """
        Creates the necessary tables for the project.
        """
        self.create_table(
            "Players",
            "player_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, rating INTEGER",
        )
        self.create_table(
            "Games",
            "game_id INTEGER PRIMARY KEY AUTOINCREMENT, date_played TEXT, result INTEGER, player_1_id INTEGER, player_2_id INTEGER, rating INTEGER, player_1_rating INTEGER",
        )
        self.create_table(
            "Moves",
            "move_id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, player_id INTEGER, move_number INTEGER, move TEXT",
        )

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

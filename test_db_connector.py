import unittest
from unittest.mock import patch

from db_connector import DBConnector


class TestDBConnector(unittest.TestCase):
    def setUp(self):
        self.db = DBConnector(":memory:")
        self.db.create_users_table()

    def tearDown(self):
        self.db._disconnect()

    def test_insert_user(self):
        self.db.insert_user("test_user", "password")
        result = self.db.verify_user("test_user", "password")
        self.assertTrue(result)

    def test_verify_user_invalid(self):
        result = self.db.verify_user("test_user", "password")
        self.assertFalse(result)

    @patch("db_connector.DBConnector.execute_query")
    def test_insert_game(self, mock_execute_query):
        self.db.insert_game(
            "Event",
            "Site",
            "2022-01-01",
            "Round 1",
            "White",
            "Black",
            "1-0",
            "2022-01-01",
            "12:00:00",
            2000,
            1800,
            200,
            -200,
            "GM",
            "A01",
            "Nimzo-Larsen",
            "Standard",
            "Time forfeit",
            "1. e4 e5 2. Nf3 Nc6",
        )
        mock_execute_query.assert_called_with(
            "INSERT INTO games (event, site, date, round, white, black, result, utc_date, utc_time, white_elo, black_elo, white_rating_diff, black_rating_diff, white_title, eco, opening, time_control, termination, moves) VALUES ('Event', 'Site', '2022-01-01', 'Round 1', 'White', 'Black', '1-0', '2022-01-01', '12:00:00', 2000, 1800, 200, -200, 'GM', 'A01', 'Nimzo-Larsen', 'Standard', 'Time forfeit', '1. e4 e5 2. Nf3 Nc6')"
        )

    @patch("db_connector.DBConnector.execute_query")
    def test_insert_move(self, mock_execute_query):
        self.db.insert_move(1, 1, "e4", 0.5, "10:00")
        mock_execute_query.assert_called_with(
            "INSERT INTO moves (game_id, move_number, move, evaluation, clock) VALUES (1, 1, 'e4', 0.5, '10:00')"
        )

    @patch("db_connector.DBConnector.execute_query")
    def test_fetch_moves(self, mock_execute_query):
        self.db.fetch_moves(1)
        mock_execute_query.assert_called_with("SELECT * FROM moves WHERE game_id = 1")

    @patch("db_connector.DBConnector.execute_query")
    def test_display_all_tables(self, mock_execute_query):
        self.db.display_all_tables()
        mock_execute_query.assert_called_with(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

    @patch("db_connector.DBConnector.execute_query")
    def test_display_previous_games(self, mock_execute_query):
        self.db.display_previous_games()
        mock_execute_query.assert_called_with("SELECT * FROM games")

    @patch("db_connector.DBConnector.execute_query")
    def test_fetch_move_history(self, mock_execute_query):
        self.db.fetch_move_history(1)
        mock_execute_query.assert_called_with("SELECT * FROM moves WHERE game_id = 1")

    @patch("db_connector.DBConnector.execute_query")
    def test_delete_game(self, mock_execute_query):
        self.db.delete_game(1)
        mock_execute_query.assert_called_with("DELETE FROM games WHERE id = 1")


if __name__ == "__main__":
    unittest.main()

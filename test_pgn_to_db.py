import sqlite3
import unittest
from unittest.mock import patch

import pandas as pd

import pgn_to_db
from db_connector import DBConnector


class TestPgnToDb(unittest.TestCase):
    def setUp(self):
        self.db = DBConnector(":memory:")
        self.db.create_games_table()
        self.db.create_moves_table()

    def tearDown(self):
        self.db._disconnect()

    @patch("pgn_to_db.count_games_in_pgn")
    def test_count_games_in_pgn(self, mock_count_games_in_pgn):
        mock_count_games_in_pgn.return_value = 10
        result = pgn_to_db.count_games_in_pgn("test.pgn")
        self.assertEqual(result, 10)

    @patch("pgn_to_db.add_game_to_db")
    def test_add_game_to_db(self, mock_add_game_to_db):
        mock_game = unittest.mock.Mock()
        mock_game.headers = {"Event": "Test Event"}
        mock_add_game_to_db.return_value = {"event": "Test Event"}
        result = pgn_to_db.add_game_to_db(mock_game, "test.pgn")
        self.assertEqual(result, {"event": "Test Event"})

    @patch("pgn_to_db.process_game")
    def test_process_game(self, mock_process_game):
        mock_process_game.return_value = {"event": "Test Event"}
        result = pgn_to_db.process_game("test.pgn", 1)
        self.assertEqual(result, {"event": "Test Event"})

    @patch("pgn_to_db.process_file")
    def test_process_file(self, mock_process_file):
        mock_process_file.return_value = None
        result = pgn_to_db.process_file("test.pgn")
        self.assertEqual(result, None)

    @patch("pgn_to_db.process_files")
    def test_process_files(self, mock_process_files):
        mock_process_files.return_value = None
        result = pgn_to_db.process_files()
        self.assertEqual(result, None)

    @patch("os.path.basename")
    def test_process_game_file_id(self, mock_basename):
        mock_basename.return_value = "test.pgn"
        result = pgn_to_db.process_game("test.pgn", 1)
        self.assertEqual(result["file_id"], "test.pgn")

    @patch("sqlite3.connect")
    def test_sqlite3_connect(self, mock_connect):
        mock_connect.return_value = sqlite3.connect(":memory:")
        result = pgn_to_db.conn
        self.assertIsInstance(result, sqlite3.Connection)

    @patch("pandas.DataFrame.to_sql")
    def test_to_sql(self, mock_to_sql):
        mock_to_sql.return_value = None
        df = pd.DataFrame([{"event": "Test Event"}])
        result = df.to_sql("games", pgn_to_db.conn, if_exists="append", index=False)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()

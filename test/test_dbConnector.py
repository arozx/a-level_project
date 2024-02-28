import unittest
from dbConnector import DBConnector


class TestDBConnector(unittest.TestCase):
    def setUp(self):
        # Set up a test database connection
        self.db = DBConnector(
            host="localhost",
            user="testuser",
            password="testpassword",
            database="testdb",
        )
        self.db.connect()

    def tearDown(self):
        # Disconnect from the test database
        self.db.disconnect()

    def test_create_table(self):
        # Test creating a new table
        table_name = "test_table"
        columns = "id INT PRIMARY KEY, name VARCHAR(255), age INT"
        self.db.create_table(table_name, columns)

        # Check if the table exists
        tables = self.db.execute_query("SHOW TABLES")
        table_names = [table[0] for table in tables]
        self.assertIn(table_name, table_names)

    def test_insert_data(self):
        # Test inserting data into a table
        table_name = "test_table"
        data = {"id": 1, "name": "John Doe", "age": 25}
        self.db.insert_data(table_name, data)

        # Check if the data was inserted correctly
        result = self.db.select_data(table_name)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], data["id"])
        self.assertEqual(result[0][1], data["name"])
        self.assertEqual(result[0][2], data["age"])

    def test_select_data(self):
        # Test selecting data from a table
        table_name = "test_table"
        condition = "age > 20"
        result = self.db.select_data(table_name, condition)

        # Check if the selected data meets the condition
        for row in result:
            self.assertGreater(row[2], 20)

    def test_update_data(self):
        # Test updating data in a table
        table_name = "test_table"
        condition = "id = 1"
        data = {"name": "Jane Doe", "age": 30}
        self.db.update_data(table_name, data, condition)

        # Check if the data was updated correctly
        result = self.db.select_data(table_name, condition)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], data["name"])
        self.assertEqual(result[0][2], data["age"])

    def test_delete_data(self):
        # Test deleting data from a table
        table_name = "test_table"
        condition = "id = 1"
        self.db.delete_data(table_name, condition)

        # Check if the data was deleted
        result = self.db.select_data(table_name, condition)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
import unittest
from dbConnector import DBConnector


class TestDBConnector(unittest.TestCase):
    def setUp(self):
        # Set up a test database connection
        self.db = DBConnector(
            host="localhost",
            user="testuser",
            password="testpassword",
            database="testdb",
        )
        self.db.connect()

    def tearDown(self):
        # Disconnect from the test database
        self.db.disconnect()

    def test_create_table(self):
        # Test creating a new table
        table_name = "test_table"
        columns = "id INT PRIMARY KEY, name VARCHAR(255), age INT"
        self.db.create_table(table_name, columns)

        # Check if the table exists
        tables = self.db.execute_query("SHOW TABLES")
        table_names = [table[0] for table in tables]
        self.assertIn(table_name, table_names)

    def test_insert_data(self):
        # Test inserting data into a table
        table_name = "test_table"
        data = {"id": 1, "name": "John Doe", "age": 25}
        self.db.insert_data(table_name, data)

        # Check if the data was inserted correctly
        result = self.db.select_data(table_name)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], data["id"])
        self.assertEqual(result[0][1], data["name"])
        self.assertEqual(result[0][2], data["age"])

    def test_select_data(self):
        # Test selecting data from a table
        table_name = "test_table"
        condition = "age > 20"
        result = self.db.select_data(table_name, condition)

        # Check if the selected data meets the condition
        for row in result:
            self.assertGreater(row[2], 20)

    def test_update_data(self):
        # Test updating data in a table
        table_name = "test_table"
        condition = "id = 1"
        data = {"name": "Jane Doe", "age": 30}
        self.db.update_data(table_name, data, condition)

        # Check if the data was updated correctly
        result = self.db.select_data(table_name, condition)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], data["name"])
        self.assertEqual(result[0][2], data["age"])

    def test_delete_data(self):
        # Test deleting data from a table
        table_name = "test_table"
        condition = "id = 1"
        self.db.delete_data(table_name, condition)

        # Check if the data was deleted
        result = self.db.select_data(table_name, condition)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()

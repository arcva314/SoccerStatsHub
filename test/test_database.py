import unittest
import sqlite3
import os
from src import Database  # Replace with the actual import statement

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_database.db'
        self.db_handler = Database.Database(self.test_db)
        self.db_handler.connect()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS players (
            id integer PRIMARY KEY,
            name text NOT NULL,
            goals integer
        );
        """
        self.db_handler.create_table(create_table_sql)

    def tearDown(self):
        self.db_handler.close()
        os.remove(self.test_db)

    def test_insert_data(self):
        player_data = {'name': 'Lionel Messi', 'goals': 50}
        self.db_handler.insert_data('players', player_data)

        query = "SELECT name, goals FROM players WHERE name='Lionel Messi'"
        result = self.db_handler.query_data(query)
        self.assertEqual(result, [('Lionel Messi', 50)])

    def test_query_data(self):
        player_data_1 = {'name': 'Lionel Messi', 'goals': 50}
        player_data_2 = {'name': 'Cristiano Ronaldo', 'goals': 45}
        self.db_handler.insert_data('players', player_data_1)
        self.db_handler.insert_data('players', player_data_2)

        query = "SELECT name, goals FROM players"
        result = self.db_handler.query_data(query)
        self.assertEqual(len(result), 2)
        self.assertIn(('Lionel Messi', 50), result)
        self.assertIn(('Cristiano Ronaldo', 45), result)

if __name__ == '__main__':
    unittest.main()

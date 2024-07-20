import unittest
import sqlite3
from src import Database, Info
import pandas as pd
class TestInfoClass(unittest.TestCase):
    def setUp(self):
        self.db = Database.Database(":memory:")
        self.db.connect()
        create_table_sql = """
        CREATE TABLE player_season (
            name TEXT,
            season TEXT,
            competition TEXT,
            goals INTEGER,
            assists INTEGER
        )
        """
        self.db.create_table(create_table_sql)

        # Insert some test data
        self.db.insert_data('player_season', {'name': 'Lionel Messi', 'season': '2019', 'competition': 'La Liga', 'goals': 30, 'assists': 10})
        self.db.insert_data('player_season', {'name': 'Lionel Messi', 'season': '2020', 'competition': 'La Liga', 'goals': 25, 'assists': 15})

    def tearDown(self):
        self.db.close()

    def test_get_player_data(self):
        info = Info.Info(name='Lionel Messi', seasons=['2019', '2020'], competitions=['La Liga'], key_stats=['goals', 'assists'])
        df = info.get_player_data(self.db)

        # Check if result is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Check DataFrame contents
        expected_data = {
            'name': ['Lionel Messi', 'Lionel Messi'],
            'season': ['2019', '2020'],
            'competition': ['La Liga', 'La Liga'],
            'goals': [30, 25],
            'assists': [10, 15]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(df, expected_df)

if __name__ == '__main__':
    unittest.main()
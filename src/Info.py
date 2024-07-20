import pandas as pd
class Info:
    def __init__(self, name, seasons, competitions, key_stats):
        self.name = name
        self.seasons = seasons
        self.competitions = competitions
        self.key_stats = key_stats

    def get_player_data(self, db_handler):
        query = f"""
        SELECT name, season, competition, {', '.join(self.key_stats)} 
        FROM player_season 
        WHERE name = '{self.name}' 
        AND season IN ({', '.join([f"'{season}'" for season in self.seasons])})
        AND competition IN ({', '.join([f"'{competition}'" for competition in self.competitions])})
        """
        results = db_handler.query_data(query)
        columns = ['name', 'season', 'competition'] + self.key_stats
        return pd.DataFrame(results, columns=columns)
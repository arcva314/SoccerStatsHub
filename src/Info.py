import pandas as pd
class Info:
    def __init__(self, name, seasons, competitions, key_stats):
        self.name = name
        self.seasons = seasons
        self.competitions = competitions
        self.key_stats = key_stats

    def get_player_data(self, db_handler):
        key_stats_str = ', '.join([f'"{stat}"' for stat in self.key_stats])
        competitions_str = ', '.join([f"'{competition}'" for competition in self.competitions])
        seasons_str = ', '.join([f"'{season}'" for season in self.seasons])
        query = 'SELECT "Player Name" as name, "Season" as season, "Tournament" as competition, ' + key_stats_str + ' FROM player_seasons_data WHERE name = "' + self.name + '" AND season IN (' + seasons_str + ') AND competition IN (' + competitions_str + ')'
        results = db_handler.execute(query)
        columns = ['name', 'season', 'competition'] + self.key_stats
        return pd.DataFrame(results, columns=columns)
    def get_manager_data(self, db_handler):
        key_stats_str = ', '.join([f'"{stat}"' for stat in self.key_stats])
        seasons_str = ', '.join([f"'{season}'" for season in self.seasons])
        query = 'SELECT "Name" as name, "Season" as season, ' + key_stats_str + ' FROM manager_seasons_data WHERE name = "' + self.name + '" AND season IN (' + seasons_str + ')'
        results = db_handler.execute(query)
        columns = ['name', 'season'] + self.key_stats
        return pd.DataFrame(results, columns=columns)
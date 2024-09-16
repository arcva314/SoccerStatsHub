from src import Visualization, Info, Database, Compare
import sqlite3
db_handler = Database.Database('../SoccerStatsHub.db')
player = Info.Info('Lionel Messi', ['2011/2012', '2018/2019', '2014/2015', '2010/2011', '2016/2017'], ['UCL', 'SLL'], ['Goals', 'Assists', 'MotM', 'Rating'])
result = player.get_player_data(db_handler)
print(result)
import pandas as pd
import sqlite3

# Define the CSV file path and the SQLite database file path
csv_file_path = 'manager_seasons.csv'
sqlite_db_path = 'SoccerStatsHub.db'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Create a connection to the SQLite database
conn = sqlite3.connect(sqlite_db_path)

# Define the table name where the data will be inserted
table_name = 'manager_seasons_data'

# Write the data to the SQLite database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

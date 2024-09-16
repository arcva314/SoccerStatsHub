import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, create_table_sql):
        self.cursor.execute(create_table_sql)

    def insert_data(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()

    def query_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

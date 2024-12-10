import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        column_definitions = ', '.join([f'{column_name} {column_type}' for column_name, column_type in columns.items()])
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})')
        self.conn.commit()

    def insert_data(self, table_name, data):
        column_names = ', '.join(data[0].keys())
        values = ', '.join(['?'] * len(data[0]))
        self.cursor.executemany(f'INSERT OR REPLACE INTO {table_name} ({column_names}) VALUES ({values})', [tuple(row.values()) for row in data])
        self.conn.commit()
    def insert_data(self, table_name, keys, values):
        # Create the INSERT query
        query = f"INSERT INTO {table_name} ({', '.join(keys)}) VALUES ({', '.join(['?'] * len(keys))})"
        # Execute the query with the given values
        self.cursor.executemany(query, values)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
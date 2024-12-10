from main import Main
from config import Config
import sqlite3
import threading

class DynamicInsightsService:
    def __init__(self):
        self.main = Main()
        self.config = Config('sqlite')
        self.thread_local = threading.local()

    def get_db_connection(self):
        if not hasattr(self.thread_local, 'conn'):
            self.thread_local.conn = sqlite3.connect(self.config.database_name, check_same_thread=False)
        return self.thread_local.conn

    def get_emp_details(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM EMPLOYEE')
        data = cursor.fetchall()
        cursor.close()
        return data

    def generate_sql_query(self, natural_language_input):
        return self.main.generate_sql_query(natural_language_input)

    def execute_query(self, sql_query):
        self.main.execute_query(sql_query)

    def get_query_results(self):
        return self.main.results

    def get_query_columns(self):
        return self.main.columns

    def export_to_csv(self, filename):
        self.main.export_to_csv(filename)
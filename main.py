import sqlite3
import json
import csv
from data_creator import DataCreator
from sql_generator import SQLGenerator
from datetime import datetime
from config import Config
import io



class Main:
    def __init__(self):
        config = Config('sqlite')
        self.database_name = config.database_name
        self.api_key = config.api_key
        self.data_creator = DataCreator(self.database_name)
        self.sql_generator = SQLGenerator(self.api_key, self.database_name)
        self.results = None
        self.columns = None

    def create_and_insert_data(self):
        self.data_creator.create_tables()
        self.data_creator.insert_data()

    def generate_sql_query(self, natural_language_input):
        return self.sql_generator.generate_query(natural_language_input)

    def execute_query(self, sql_query):
        try:
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            print('excute query')
            print(sql_query)
            cursor.execute(sql_query)
            self.results = cursor.fetchall()
            self.columns = [description[0] for description in cursor.description]
            conn.close()
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            print("Message: Table or table structure not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def display_query_results(self):
        if self.results is not None:
            print("Query Results:")
            for row in self.results:
                print(row)
        else:
            print("No results found.")

    def export_to_csv(self, filename):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"query_results_{timestamp}.csv"
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        if self.columns and self.results:
            writer.writerow(self.columns)  # Write the column headers
            writer.writerows(self.results)  # Write the results
            #print('csv_data.getvalue:')
            #print(csv_data.getvalue)
            return csv_data.getvalue()
        else:
            return "No data available"

if __name__ == '__main__':
    main = Main()
    main.create_and_insert_data()
    natural_language_input = "Show the names of employees who have an issue code."
    sql_query = main.generate_sql_query(natural_language_input)
    print("Generated SQL Query:")
    print(sql_query)
    main.execute_query(sql_query)
    main.display_query_results()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"query_results_{timestamp}.csv"
    main.export_to_csv(filename)
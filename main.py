import sqlite3
import json
import csv
from data_creator import DataCreator
from sql_generator import SQLGenerator
from datetime import datetime

class Main:
    def __init__(self):
        self.data_creator = DataCreator('DynamicInsights.db')
        self.sql_generator = SQLGenerator('AIzaSyBHXFCxfatXH_4EOZBWaIDWnbBWcw0Y0bQ', 'DynamicInsights.db')
        self.results = None
        self.columns = None

    def create_and_insert_data(self):
        self.data_creator.create_tables()
        self.data_creator.insert_data()

    def generate_sql_query(self, natural_language_input):
        return self.sql_generator.generate_query(natural_language_input)

    def execute_query(self, sql_query):
        try:
            conn = sqlite3.connect('DynamicInsights.db')
            cursor = conn.cursor()
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
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.columns)  # Write the column headers
            writer.writerows(self.results)  # Write the results
        print(f"Results exported to {filename}")

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
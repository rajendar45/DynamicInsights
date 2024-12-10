import os
import sqlite3
import google.generativeai as genai
import json
import logging

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.basicConfig(level=logging.ERROR)

# Configure the API key
genai.configure(api_key="AIzaSyBHXFCxfatXH_4EOZBWaIDWnbBWcw0Y0bQ")

# Load the Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a SQLite database and tables
conn = sqlite3.connect('empdata.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS empdata
    (guid TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, middlename TEXT, age INTEGER)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS empissues
    (guid TEXT PRIMARY KEY, issuecode TEXT)
''')

# Insert sample data into the tables
sample_data_empdata = [
    ('guid1', 'John', 'Doe', 'M', 30),
    ('guid2', 'Jane', 'Smith', 'E', 25),
    ('guid3', 'Bob', 'Johnson', 'A', 40),
    ('guid4', 'Alice', 'Williams', 'L', 35),
    ('guid5', 'Mike', 'Davis', 'T', 20),
]

sample_data_empissues = [
    ('guid1', 'issue1'),
    ('guid2', 'issue2'),
    ('guid3', 'issue3'),
    ('guid4', 'issue4'),
    ('guid5', 'issue5'),
]

cursor.executemany('INSERT OR REPLACE INTO empdata VALUES (?,?,?,?,?)', sample_data_empdata)
cursor.executemany('INSERT OR REPLACE INTO empissues VALUES (?,?)', sample_data_empissues)
conn.commit()

# Define a function to generate SQL queries from natural language inputs
def generate_sql_query(natural_language_input):
    response = model.generate_content(f"translate English to SQL: {natural_language_input}. Give SQL query in JSON response")
    candidates = response.candidates
    if candidates:
        sql_query = json.loads(candidates[0].content.parts[0].text.strip("```json\n"))["sql"]
        return sql_query
    else:
        return "No candidates found in the response."

# Test the function with a sample natural language input that joins the two tables
natural_language_input = "Show the names of employees who have an issue code and are older than 30."
print(generate_sql_query(natural_language_input))

# Close the SQLite database connection
conn.close()
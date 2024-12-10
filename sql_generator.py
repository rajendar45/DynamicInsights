import google.generativeai as genai
import json
import sqlite3


class SQLGenerator:
    def __init__(self, api_key, db_name):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.db_name = db_name
        self.db_schema = self.get_db_schema()

    def get_db_schema(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        schema = {}
        for row in cursor.fetchall():
            table_name = row[0]
            table_schema = row[1]
            schema[table_name] = table_schema
        conn.close()
        return schema

    def generate_query(self, natural_language_input):
        try:
            db_schema_json = json.dumps(self.db_schema)
            response = self.model.generate_content(f"translate English to SQL: {natural_language_input}. Give SQL query in JSON response. Database schema: {db_schema_json}")
            candidates = response.candidates
            if candidates:
                json_response = json.loads(candidates[0].content.parts[0].text.strip("```json\n"))
                sql_query = json_response["sql"]
                return sql_query
            else:
                return "No candidates found in the response."
        except Exception as e:
            return str(e)
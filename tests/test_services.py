import unittest
from ..services import DynamicInsightsService

class TestDynamicInsightsService(unittest.TestCase):
    def setUp(self):
        self.service = DynamicInsightsService()

    def test_get_db_connection(self):
        conn = self.service.get_db_connection()
        self.assertIsInstance(conn, sqlite3.Connection)

    def test_generate_sql_query(self):
        natural_language_input = "Show me the names of employees who have an issue code"
        sql_query = self.service.generate_sql_query(natural_language_input)
        self.assertIsInstance(sql_query, str)

    def test_execute_query(self):
        sql_query = "SELECT * FROM employees"
        self.service.execute_query(sql_query)

    def test_get_query_results(self):
        results = self.service.get_query_results()
        self.assertIsInstance(results, list)

    def test_get_query_columns(self):
        columns = self.service.get_query_columns()
        self.assertIsInstance(columns, list)

    def test_export_to_csv(self):
        filename = "test.csv"
        self.service.export_to_csv(filename)

if __name__ == "__main__":
    unittest.main()
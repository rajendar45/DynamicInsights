import unittest
from ..dynamic_insights_controller import DynamicInsightsController
from ..services import DynamicInsightsService

class TestDynamicInsightsController(unittest.TestCase):
    def setUp(self):
        self.controller = DynamicInsightsController()
        self.service = DynamicInsightsService()

    def test_health(self):
        response = self.controller.health()
        self.assertEqual(response, "Welcome to Dynamic Insights!")

    def test_get_emp_details(self):
        response = self.controller.get_emp_details()
        self.assertIsInstance(response, dict)
        self.assertIn("message", response)

    def test_generate_sql_query(self):
        natural_language_input = "Show me the names of employees who have an issue code"
        response = self.controller.generate_sql_query()
        self.assertIsInstance(response, dict)
        self.assertIn("sql_query", response)

    def test_execute_query(self):
        sql_query = "SELECT * FROM employees"
        response = self.controller.execute_query()
        self.assertIsInstance(response, dict)
        self.assertIn("sql_query", response)

    def test_display_query_results(self):
        response = self.controller.display_query_results()
        self.assertIsInstance(response, dict)
        self.assertIn("results", response)

    def test_export_to_csv(self):
        filename = "test.csv"
        response = self.controller.export_to_csv()
        self.assertIsInstance(response, dict)
        self.assertIn("message", response)

if __name__ == "__main__":
    unittest.main()
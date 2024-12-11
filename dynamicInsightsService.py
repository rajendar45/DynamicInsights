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
    
    def get_chart_data(self,nlpquery):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            if nlpquery is not None and nlpquery.strip() != '':
                cursor.execute(nlpquery)
            else:
                cursor.execute('SELECT TAX_YR, FEIN_ID, SUM(PENALTY_A_AMT) AS TOTAL_PENALTY_A_AMT, SUM(PENALTY_B_AMT) AS TOTAL_PENALTY_B_AMT FROM FEIN_PENALTY_INFO GROUP BY TAX_YR, FEIN_ID HAVING SUM(PENALTY_A_AMT) > 0 ORDER BY TAX_YR, FEIN_ID')
            rows = cursor.fetchall()
            if not rows:
                chart_data = []
            else:
                print(rows)
                columns = [description[0] for description in cursor.description]
                chart_data = [
                    {
                        'x': row[0]+'_'+row[1],
                        'y': row[2],
                        'h': columns[0]+'_'+columns[1]
                    }
                    for row in rows
                ]
            print(chart_data)
            return {"chartData": chart_data}
        except Exception as e:
            return {"error": str(e)}


    def generate_sql_query(self, natural_language_input):
        return self.main.generate_sql_query(natural_language_input)

    def execute_query(self, sql_query):
        self.main.execute_query(sql_query)

    def get_query_results(self):
        return self.main.results

    def get_query_columns(self):
        return self.main.columns

    def export_to_csv(self, filename):
        return self.main.export_to_csv(filename)
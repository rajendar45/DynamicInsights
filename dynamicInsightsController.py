from flask import request, jsonify
from flask import Response
from dynamicInsightsService import DynamicInsightsService

class DynamicInsightsController:
    def __init__(self):
        self.service = DynamicInsightsService()

    def health(self):
        return 'Welcome to my Dynamic Insights app!'

    def get_emp_details(self):
        data = self.service.get_emp_details()
        return jsonify({'message': 'Query executed successfully :'+str(data)}), 200

    def generate_sql_query(self):
        self.natural_language_input = request.json['natural_language_input']
        sql_query = self.service.generate_sql_query(self.natural_language_input)
        print(sql_query)
        return jsonify({'sql_query': sql_query})

    def execute_query(self):
        sql_query = request.json['sql_query']
        self.nlpquery = sql_query
        self.service.execute_query(sql_query)
        return {'sql_query': sql_query}

    def display_query_results(self):
        results = self.service.get_query_results()
        columns = self.service.get_query_columns()
        if results is not None:
            return jsonify({'results': results, 'columns': columns}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'message': 'No results found'}), 200, {'Content-Type': 'application/json'}

    def export_to_csv(self):
        filename = request.json['filename']
        csv_data = self.service.export_to_csv(filename)
        print('csv_data: ')
        print(csv_data)
        if csv_data is None:
            return []
        return csv_data
    
    def get_chart_data(self):
        return self.service.get_chart_data(self.nlpquery)
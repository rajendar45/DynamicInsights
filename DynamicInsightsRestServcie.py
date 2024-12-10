from flask import Flask
from flask import request
from flask import render_template


from dynamicInsightsController import DynamicInsightsController

dynamic_insights_rest_service = Flask(__name__)

controller = DynamicInsightsController()

@dynamic_insights_rest_service.route('/')
def index():
    return render_template('index.html')

@dynamic_insights_rest_service.route('/health', methods=['GET'])
def health():
    return controller.health()

@dynamic_insights_rest_service.route('/getEMP', methods=['GET'])
def get_emp_details():
    return controller.get_emp_details()

@dynamic_insights_rest_service.route('/generate_sql_query', methods=['POST'])
def generate_sql_query():
    return controller.generate_sql_query()

@dynamic_insights_rest_service.route('/execute_query', methods=['POST'])
def execute_query():
    return controller.execute_query()

@dynamic_insights_rest_service.route('/display_query_results', methods=['GET'])
def display_query_results():
    return controller.display_query_results()

@dynamic_insights_rest_service.route('/export_to_csv', methods=['POST'])
def export_to_csv():
    return controller.export_to_csv()

if __name__ == '__main__':
    dynamic_insights_rest_service.run(debug=True, host="0.0.0.0", port=8080)
from flask import Flask, request, jsonify
from main import Main
import json
import threading
import sqlite3
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from config import Config


dynamic_insights_rest_service = Flask(__name__)
CORS(dynamic_insights_rest_service)
thread_local = threading.local()

main = Main()
#config = Config('sqlite')

def get_db_connection():
    if not hasattr(thread_local, 'conn'):
        config = Config('sqlite')
        thread_local.conn = sqlite3.connect(config.database_name, check_same_thread=False)
    return thread_local.conn

def insert_data_into_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    main.create_and_insert_data()
    conn.commit()
    cursor.close()

@dynamic_insights_rest_service.route('/health', methods=['GET'])
def health():
    return 'Welcome to my Dynamic Insights app!'

@dynamic_insights_rest_service.route('/getEMP', methods=['GET'])
def getEmpDetils():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM EMPLOYEE')
    data = cursor.fetchall()
    cursor.close()
    return jsonify({'message': 'Query executed successfully :'+str(data)}), 200

@dynamic_insights_rest_service.route('/grid')
def grid():
    return render_template('grid.html')

@dynamic_insights_rest_service.route('/')
def index():
    return render_template('index.html')

from flask import json

@dynamic_insights_rest_service.route('/generate_sql_query', methods=['POST'])
def generate_sql_query():
    try:
        natural_language_input = request.json['natural_language_input']
        print("Received natural language input:", natural_language_input)
        sql_query = main.generate_sql_query(natural_language_input)
        print("Generated SQL query:", sql_query)
        print(jsonify({'sql_query': sql_query}))
        return jsonify({'sql_query': sql_query})
    except Exception as e:
        print("Error generating SQL query:", e)
        return jsonify({'error': str(e)}), 500
    
@dynamic_insights_rest_service.route('/execute_query', methods=['POST'])
def execute_query():
    print('inside execute_query')
    sql_query = request.json['sql_query']
    print('execute query:')
    print(sql_query)
    main.execute_query(sql_query)
    return {'sql_query': sql_query}



@dynamic_insights_rest_service.route('/display_query_results', methods=['GET'])
def display_query_results():
    results = main.results
    columns = main.columns
    if results is not None:
        return jsonify({'results': results, 'columns': columns}), 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'No results found'}), 200, {'Content-Type': 'application/json'}

@dynamic_insights_rest_service.route('/export_to_csv', methods=['POST'])
def export_to_csv():
    filename = request.json['filename']
    main.export_to_csv(filename)
    return jsonify({'message': f'Results exported to {filename}'}), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    dynamic_insights_rest_service.run(debug=True,host="0.0.0.0", port=8080)

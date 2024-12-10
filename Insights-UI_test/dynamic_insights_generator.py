from insights_dao import execute_query
from nlp_parser import convert_to_query
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
def get_faq_questions():
    print("Enter frequently asked questions (type 'done' to finish):")
    faq_questions = []
    while True:
        question = input()
        if question == "done":
            break
        faq_questions.append(question)
    return faq_questions

def launch_insights():
    app = Flask(__name__)
    CORS(app)
    @app.route('/generate_insights', methods=['GET'])
    def generate_insights_endpoint():
        question = request.args.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        try:
            print("Understanding your question ..." + question)
            query = convert_to_query(question)
            print("Running interpreted query.."+query)
            results = execute_query(query)
            # Check if the results contain any date columns and format them
            for column in results.columns:
                if pd.api.types.is_datetime64_any_dtype(results[column]):
                    results[column] = results[column].dt.strftime('%Y-%m-%d %H:%M:%S')
            print(results)
            record =results.to_json(orient='records')
            print(record)
            return record
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    if __name__ == '__main__':
        app.run(debug=True,port=8080)
#Main program Starts here
print("Dynamic Insights Generator")
launch_insights()


// script.js

const executeQueryBtn = document.getElementById('execute-query-btn');
const displayResultsBtn = document.getElementById('display-results-btn');
const exportToCsvBtn = document.getElementById('export-to-csv-btn');

const generateSqlForm = document.getElementById('generate-sql-form');
const executeQueryForm = document.getElementById('execute-query-form');
const exportToCsvForm = document.getElementById('export-to-csv-form');

const resultsContainer = document.getElementById('results-container');

const generateSqlBtn = document.getElementById('generate-sql-submit-btn');
const sqlQueryContainer = document.getElementById('sql-query-container');


generateSqlBtn.addEventListener('click', () => {
    console.log('Generate SQL button clicked!');
    const naturalLanguageInput = document.getElementById('natural-language-input').value;
    console.log('Natural language input:', naturalLanguageInput);


    fetch('/generate_sql_query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ natural_language_input: naturalLanguageInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })    
    .then(data => {
        console.log('Received SQL query:', data.sql_query);
        sqlQueryContainer.innerText = data.sql_query;
    })
    .catch(error => console.error('Error:', error));
    });

executeQueryBtn.addEventListener('click', () => {
    const sqlQuery = document.getElementById('sql-query-input').value;
    console.log('sqlQuery:', sqlQuery);
    fetch('/execute_query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sql_query: sqlQuery })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});

displayResultsBtn.addEventListener('click', () => {
    fetch('/display_query_results', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});

exportToCsvBtn.addEventListener('click', () => {
    const filename = document.getElementById('filename-input').value;
    fetch('/export_to_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
});
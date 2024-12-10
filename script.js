// script.js

const generateSqlBtn = document.getElementById('generate-sql-btn');
const executeQueryBtn = document.getElementById('execute-query-btn');
const displayResultsBtn = document.getElementById('display-results-btn');
const exportToCsvBtn = document.getElementById('export-to-csv-btn');

const generateSqlForm = document.getElementById('generate-sql-form');
const executeQueryForm = document.getElementById('execute-query-form');
const exportToCsvForm = document.getElementById('export-to-csv-form');

const resultsContainer = document.getElementById('results-container');
const sqlQueryContainer = document.getElementById('sql-query-container');

generateSqlBtn.addEventListener('click', () => {
    console.log('Generate SQL button clicked!');
    const naturalLanguageInput = document.getElementById('natural-language-input').value;
    console.log('Natural language input:', naturalLanguageInput);
    fetch(' http://127.0.0.1:5000/getdata', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ natural_language_input: naturalLanguageInput })
    })
    .then(response => {
        console.log('Response received:');
        console.log(response);
        return response.json();
    })
    .then(data => {
        console.log('Data received:');
        console.log(data);
        const sqlQuery = data.sql_query;
        sqlQueryContainer.innerText = sqlQuery;
    })
    .catch(error => console.error('Error:', error));
});


executeQueryBtn.addEventListener('click', () => {
    const sqlQuery = document.getElementById('sql-query-input').value;
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
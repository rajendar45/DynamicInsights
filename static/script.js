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
const viewChartDataBtn  = document.getElementById('view-chart-data-btn');



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
        document.getElementById('sql-query-input').value = data.sql_query;
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
  .then(data => {
    const container = document.getElementById('results-container');
    container.innerHTML = ''; // Clear existing content

    if (data.results.length === 0) {
      container.innerHTML = '<p>No results available.</p>';
    } else {
      // Create table
      const table = document.createElement('table');
      table.style.width = '100%'; // Set table width to 100%

      // Create table header row
      const headerRow = document.createElement('tr');
      data.columns.forEach(column => {
        const headerCell = document.createElement('th');
        headerCell.textContent = column;
        headerCell.style.background = '#f0f0f0'; // Style column headers
        headerCell.style.padding = '8px';
        headerRow.appendChild(headerCell);
      });
      table.appendChild(headerRow);

      // Create table body
      const tableBody = document.createElement('tbody');
      table.appendChild(tableBody);

      // Append the table to the results container
      container.appendChild(table);

      // Function to render table data
      function renderTableData(results) {
        tableBody.innerHTML = '';

        const currentPageResults = results;
        currentPageResults.forEach(result => {
          const row = document.createElement('tr');
          result.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            cell.style.padding = '8px';
            row.appendChild(cell);
          });
          tableBody.appendChild(row);
        });
      }

      // Function to handle pagination
      function handlePagination() {
        const recordsPerPage = 10;
        const totalPages = Math.ceil(data.results.length / recordsPerPage);
        let currentPage = 1;

        // Render table data for current page
        const startIndex = (currentPage - 1) * recordsPerPage;
        const endIndex = startIndex + recordsPerPage;
        const currentPageResults = data.results.slice(startIndex, endIndex);
        renderTableData(currentPageResults);

        // Create pagination buttons
        const paginationContainer = document.createElement('div');
        paginationContainer.style.textAlign = 'center'; // Center pagination buttons

        const prevPageBtn = document.createElement('button');
        prevPageBtn.textContent = 'Previous';
        prevPageBtn.addEventListener('click', () => {
          if (currentPage > 1) {
            currentPage--;
            handlePagination();
          }
        });

        const nextPageBtn = document.createElement('button');
        nextPageBtn.textContent = 'Next';
        nextPageBtn.addEventListener('click', () => {
          if (currentPage < totalPages) {
            currentPage++;
            handlePagination();
          }
        });

        const pageNumDisplay = document.createElement('span');
        pageNumDisplay.textContent = `Page ${currentPage} of ${totalPages}`;

        paginationContainer.appendChild(prevPageBtn);
        paginationContainer.appendChild(pageNumDisplay);
        paginationContainer.appendChild(nextPageBtn);

        // Append the pagination container to the results container
        container.appendChild(paginationContainer);
      }

      handlePagination(); // Call handlePagination() when results are available
    }
  })
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
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  })
  .catch(error => console.error(error));
});

document.getElementById('view-chart-data-btn').addEventListener('click', function() {
    // Make an AJAX request to retrieve the chart data
    fetch('/chart-data', {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      const chartDataArray = data.chartData.chartData; // Access the chartData array property
      // Render the chart using Highcharts
      Highcharts.chart('chart-container', {
        chart: {
          type: 'column'
        },
        title: {
          text: 'Penalty Data'
        },
        xAxis: {
          type: 'category',
          categories: chartDataArray.map(function(item) {
            return item.name;
          })
        },
        yAxis: {
          title: {
            text: 'Values'
          }
        },
        series: [{
          name: 'Penalty A',
          data: chartDataArray.map(function(item) {
            return item.data[0].y;
          })
        }, {
          name: 'Penalty B',
          data: chartDataArray.map(function(item) {
            return item.data[1].y;
          })
        }]
      });
    })
    .catch((error) => {
      console.error(error);
    })
  });
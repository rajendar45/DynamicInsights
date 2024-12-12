const generateSqlBtn = document.getElementById('generate-sql-submit-btn');
const displayResultsBtn = document.getElementById('display-results-btn');
const refreshBtn = document.getElementById('reset-btn');

// Add event listener to refresh button
if (refreshBtn) {
  refreshBtn.addEventListener('click', () => {
    // Reset query input field
    const queryInputField = document.getElementById('sql-query-input');
    queryInputField.value = '';

    // Refresh the page
    location.reload();
  });
}

function populateHintText(hintText) {
  document.getElementById("natural-language-input").value = hintText;
}

if (generateSqlBtn) {
  generateSqlBtn.addEventListener('click', () => {
      console.log('Generate SQL button clicked!');
      const naturalLanguageInput = document.getElementById('natural-language-input').value;
      console.log('Natural language input:', naturalLanguageInput);
      document.getElementById('hourglass-container').style.display = 'block';
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
          document.getElementById('hourglass-container').style.display = 'none';
      })
      .catch(error => console.error('Error:', error));
  });
}
displayResultsBtn.addEventListener('click', async () => {
  const sqlQuery = document.getElementById('sql-query-input').value;
  console.log('sqlQuery:', sqlQuery);
  try {
    const response = await fetch('/execute_query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sql_query: sqlQuery })
    });
    const data = await response.json();
    console.log(data);
    // Now display the results
    fetch('/display_query_results', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      const resultsContainer = document.getElementById('results-container');
      resultsContainer.innerHTML = ''; // Clear existing content

      if (data.results.length === 0) {
        resultsContainer.innerHTML = '<p>No results available.</p>';
      } else {
        //create table
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
        resultsContainer.appendChild(table);
        //end table
        //CSV Export logic 
        const exportButton = document.createElement('button');
        exportButton.id = 'export-to-csv-btn';
        exportButton.addEventListener('click', () => {
          const filename = 'Tempdata';
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
     
        exportButton.textContent = 'Export to CSV';
        resultsContainer.appendChild(exportButton);
        //Penalty display if query contains penalty 
        if (sqlQuery.toLowerCase().includes('penalty')) {
          const viewPenaltyDataBtn = document.createElement('button');
          viewPenaltyDataBtn.id = 'view-chart-data-btn';
          viewPenaltyDataBtn.textContent = 'View Penalty Data';
          viewPenaltyDataBtn.addEventListener('click', () => {
            fetch('/chart-data', {
              method: 'GET'
            })
            .then(response => response.json())
            .then(data => {
              const chartDataArray = data.chartData.chartData; // Access the chartData array property
              //Render the chart using Highcharts
              Highcharts.chart('bar-chart-container', {
                chart: {
                  type: 'column'
                },
                title: {
                  text: 'Penalty Data'
                },
                xAxis: {
                  type: 'category',
                  categories: chartDataArray.map(function(item) {
                    return item.x;
                  })
                },
                yAxis: {
                  title: {
                    text: 'Penalty'
                  }
                },
                series: [{
                  name: 'Fein Tax Year',
                  data: chartDataArray.map(function(item) {
                    return item.y;
                  })
                }]
              });
              Highcharts.chart('pie-chart-container', {
                chart: {
                  type: 'pie'
                },
                title: {
                  text: 'Penalty Data'
                },
                series: [{
                  name: 'Penalty',
                  colorByPoint: true,
                  data: chartDataArray.map(function(item) {
                    return {
                      name: item.x,
                      y: item.y
                    };
                  })
                }]
              });
            })
            .catch(error => console.error('Error fetching penalty data:', error));
          });
          resultsContainer.appendChild(viewPenaltyDataBtn);
        }
        
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
        renderTableData(data.results);
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
          resultsContainer.appendChild(paginationContainer);
        }

        handlePagination(); // Call handlePagination() when results are available
      }
    })
    .catch(error => console.error(error));
  } catch (error) {
    console.error(error);
  }
});

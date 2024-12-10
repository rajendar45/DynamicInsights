const fetchDataBtn = document.getElementById('fetch-data-btn');
const dataContainer = document.getElementById('data-container');

fetchDataBtn.addEventListener('click', fetchData);

function fetchData() {
    fetch('/getEMP')
        .then(response => response.json())
        .then(data => {
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');

            table.appendChild(thead);
            table.appendChild(tbody);

            dataContainer.innerHTML = '';
            dataContainer.appendChild(table);

            const row = document.createElement('tr');
            thead.appendChild(row);

            const headers = ['Employee ID', 'Name', 'Department', 'Designation'];
            headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                row.appendChild(th);
            });

            data.message.split(':')[1].slice(1, -1).split('), (').forEach(employee => {
                const row = document.createElement('tr');
                tbody.appendChild(row);

                const [employeeId, name, department, designation] = employee.split(', ');
                [employeeId, name, department, designation].forEach(value => {
                    const td = document.createElement('td');
                    td.textContent = value.replace(/'/g, '');
                    row.appendChild(td);
                });
            });
        })
        .catch(error => console.error(error));
}
function filterEmployeesTable() {
  const input = document.getElementById('employee-search');
  const filter = input.value.toLowerCase();
  const tbody = document.getElementById('employees-table-body');
  const trs = tbody.getElementsByTagName('tr');
  for (let i = 0; i < trs.length; i++) {
    const td = trs[i].getElementsByTagName('td')[1]; // Employee ID column
    if (td) {
      const txtValue = td.textContent || td.innerText;
      trs[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('employee-search');
  if (searchInput) {
    searchInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        filterEmployeesTable();
      }
    });
  }
});
function filterTableRows(inputId, tableBodyId, columnIndex = 1) {
  const input = document.getElementById(inputId);
  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableBodyId);
  const trs = table.getElementsByTagName('tr');
  for (let i = 0; i < trs.length; i++) {
    const td = trs[i].getElementsByTagName('td')[columnIndex];
    if (td) {
      const txtValue = td.textContent || td.innerText;
      trs[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Universal table search configuration: [inputId, tableBodyId, columnIndex]  
  const searches = window.TABLE_SEARCHES || [];
  searches.forEach(([inputId, tableBodyId, columnIndex]) => {
    const input = document.getElementById(inputId);
    if (input) {
      input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
          event.preventDefault();
          filterTableRows(inputId, tableBodyId, columnIndex);
        }
      });
    }
  });
});
function filterWorksTable() {
  const input = document.getElementById('work-search');
  const filter = input.value.toLowerCase();
  const table = document.getElementById('works-table');
  const trs = table.getElementsByTagName('tr');
  for (let i = 1; i < trs.length; i++) { // skip header row
    const td = trs[i].getElementsByTagName('td')[1];
    if (td) {
      const txtValue = td.textContent || td.innerText;
      trs[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('work-search');
  if (searchInput) {
    searchInput.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        filterWorksTable();
      }
    });
  }
});
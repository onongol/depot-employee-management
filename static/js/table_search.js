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

// Универсальная фильтрация таблицы по select (например, по должности)
function filterTableBySelect(selectId, tableBodyId, columnIndex = 1) {
  const select = document.getElementById(selectId);
  const table = document.getElementById(tableBodyId);
  if (!select || !table) return;

  select.addEventListener('change', function() {
    const value = select.value;
    const trs = table.getElementsByTagName('tr');
    for (let i = 0; i < trs.length; i++) {
      const td = trs[i].getElementsByTagName('td')[columnIndex];
      if (!td) continue;
      if (!value || td.textContent.trim() === value) {
        trs[i].style.display = '';
      } else {
        trs[i].style.display = 'none';
      }
    }
  });
}

// Автоматически инициализировать фильтрацию для всех select-фильтров
document.addEventListener('DOMContentLoaded', function() {
  if (window.TABLE_SELECT_FILTERS) {
    window.TABLE_SELECT_FILTERS.forEach(([selectId, tableBodyId, columnIndex]) => {
      filterTableBySelect(selectId, tableBodyId, columnIndex);
    });
  }
});
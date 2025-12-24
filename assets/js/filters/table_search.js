// Provides client-side table search and select filters: filters rows by text input or select dropdown, and initializes per-page configs via window.TABLE_SEARCHES and window.TABLE_SELECT_FILTERS.

function filterTableRows(inputId, tableBodyId, columnIndex = 1) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const filter = input.value.toLowerCase();
  const table = document.getElementById(tableBodyId);
  if (!table) return;
  const trs = table.getElementsByTagName('tr');
  for (let i = 0; i < trs.length; i++) {
    const td = trs[i].getElementsByTagName('td')[columnIndex];
    if (td) {
      const txtValue = td.textContent || td.innerText;
      trs[i].style.display = txtValue.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
    }
  }
}

// existing DOM init (kept for compatibility)
document.addEventListener('DOMContentLoaded', function() {
  // 1) Backwards-compatible config via window.TABLE_SEARCHES
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

  // 2) New: auto-init from data-attributes on inputs/selects
  document.querySelectorAll('input[data-table][data-column], input[data-table]').forEach(input => {
    const table = input.dataset.table;
    const col = input.dataset.column ? Number(input.dataset.column) : 1;
    input.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        filterTableRows(input.id, table, col);
      }
    });
  });

  // For selects with data-table
  document.querySelectorAll('select[data-table][data-column], select[data-table]').forEach(select => {
    const table = select.dataset.table;
    const col = select.dataset.column ? Number(select.dataset.column) : 1;
    // attach change handler
    select.addEventListener('change', function() {
      // reuse helper logic from filterTableBySelect
      const value = select.value;
      const tableEl = document.getElementById(table);
      if (!tableEl) return;
      const trs = tableEl.getElementsByTagName('tr');
      for (let i = 0; i < trs.length; i++) {
        const td = trs[i].getElementsByTagName('td')[col];
        if (!td) continue;
        trs[i].style.display = (!value || td.textContent.trim() === value) ? '' : 'none';
      }
    });
  });

  // Also auto-init select filters declared via window.TABLE_SELECT_FILTERS (compat)
  if (window.TABLE_SELECT_FILTERS) {
    window.TABLE_SELECT_FILTERS.forEach(([selectId, tableBodyId, columnIndex]) => {
      const sel = document.getElementById(selectId);
      if (!sel) return;
      sel.addEventListener('change', function() {
        const value = sel.value;
        const table = document.getElementById(tableBodyId);
        if (!table) return;
        const trs = table.getElementsByTagName('tr');
        for (let i = 0; i < trs.length; i++) {
          const td = trs[i].getElementsByTagName('td')[columnIndex];
          if (!td) continue;
          trs[i].style.display = (!value || td.textContent.trim() === value) ? '' : 'none';
        }
      });
    });
  }
});

// Optional helpers kept globally (compat)
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
      trs[i].style.display = (!value || td.textContent.trim() === value) ? '' : 'none';
    }
  });
}

window.filterTableRows = filterTableRows;
window.filterTableBySelect = filterTableBySelect;
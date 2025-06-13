function updateSelectedEmployeesSummary() {
  const empCheckboxes = document.querySelectorAll('input[name="employee_ids"]');
  const empChecked = document.querySelectorAll('input[name="employee_ids"]:checked');
  const selectAllEmp = document.getElementById('select-all-employees');
  let empSummary = 'None';
  if (selectAllEmp && selectAllEmp.checked && empChecked.length === empCheckboxes.length && empChecked.length > 0) {
    empSummary = 'Selected all';
  } else {
    const empNames = Array.from(empChecked).map(cb => {
      const row = cb.closest('tr');
      if (row) {
        // Get only the text node after the label (employee_id)
        const empIdCell = row.querySelector('td:nth-child(2)');
        let empId = '';
        if (empIdCell) {
          // Find the text node that is not the label
          empId = Array.from(empIdCell.childNodes)
            .filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim())
            .map(n => n.textContent.trim())[0] || '';
        }
        const empName = row.querySelector('td:nth-child(3)')?.textContent.trim() || '';
        return empId && empName ? `${empId}/${empName}` : '';
      }
      return '';
    }).filter(Boolean);
    if (empNames.length) empSummary = empNames.join(', ');
  }
  document.getElementById('selected-employees-list').textContent = empSummary;
  // Show or hide the summary box (works handled in works script)
  const workChecked = document.querySelectorAll('input[name="work_ids"]:checked');
  document.getElementById('selected-summary').style.display = (empChecked.length || workChecked.length) ? '' : 'none';
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[name="employee_ids"]').forEach(cb => {
    cb.addEventListener('change', updateSelectedEmployeesSummary);
  });
  const selectAllEmp = document.getElementById('select-all-employees');
  if (selectAllEmp) selectAllEmp.addEventListener('change', updateSelectedEmployeesSummary);
  updateSelectedEmployeesSummary();
});
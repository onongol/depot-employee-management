// Update the selected employees summary display
function updateSelectedEmployeesSummary() {
  const empCheckboxes = document.querySelectorAll('input[name="employee_ids"]');
  const empChecked = document.querySelectorAll('input[name="employee_ids"]:checked');
  const selectAllEmp = document.getElementById('select-all-employees');
  
  // Let user know if no employees are selected
  let empSummary = gettext('No employees selected');
  if (selectAllEmp && selectAllEmp.checked && empChecked.length === empCheckboxes.length && empChecked.length > 0) {
    empSummary = gettext('Selected all');

  // If not all selected, list selected employees by employee_id/name
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
        // Get only the text node after the label (employee name)
        const empName = row.querySelector('td:nth-child(3)')?.textContent.trim() || '';
        // Format as id/name
        return empId && empName ? `${empId}/${empName}` : '';
      }
      return '';
    }).filter(Boolean);
    if (empNames.length) empSummary = empNames.join(', ');
  }

  // Update the summary display
  document.getElementById('selected-employees-list').textContent = empSummary;
  // Show or hide the summary box (works handled in works script)
  const workChecked = document.querySelectorAll('input[name="work_ids"]:checked');
  document.getElementById('selected-summary').style.display = (empChecked.length || workChecked.length) ? '' : 'none';
}

// Helper: safely get employee id and name from checkbox row
function getEmployeeIdAndName(cb) {
  if (!cb) return { id: '', name: '' };
  const row = cb.closest('tr');
  if (!row) return { id: '', name: '' };
  // Retrieve employee id from the second cell
  const empIdCell = row.querySelector('td:nth-child(2)');
  let empId = '';
  if (empIdCell) {
    empId = Array.from(empIdCell.childNodes)
      .filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim())
      .map(n => n.textContent.trim())[0] || '';
  }
  // Retrieve employee name from the third cell
  const empNameCell = row.querySelector('td:nth-child(3)');
  const empName = empNameCell ? empNameCell.textContent.trim() : '';
  return { id: empId, name: empName };
}

// Initialize event listeners on DOM load
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[name="employee_ids"]').forEach(cb => {
    cb.addEventListener('change', updateSelectedEmployeesSummary);
  });
  const selectAllEmp = document.getElementById('select-all-employees');
  if (selectAllEmp) selectAllEmp.addEventListener('change', updateSelectedEmployeesSummary);
  updateSelectedEmployeesSummary();
});
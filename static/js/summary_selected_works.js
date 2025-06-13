function updateSelectedWorksSummary() {
  const workCheckboxes = document.querySelectorAll('input[name="work_ids"]');
  const workChecked = document.querySelectorAll('input[name="work_ids"]:checked');
  const selectAllWork = document.getElementById('select-all-works');
  let workSummary = 'None';
  if (selectAllWork && selectAllWork.checked && workChecked.length === workCheckboxes.length && workChecked.length > 0) {
    workSummary = 'Selected all';
  } else {
    const workNames = Array.from(workChecked).map(cb => {
      const row = cb.closest('tr');
      if (row) {
        // Get only the text node after the label (work name)
        const workNameCell = row.querySelector('td:nth-child(2)');
        let workName = '';
        if (workNameCell) {
          workName = Array.from(workNameCell.childNodes)
            .filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim())
            .map(n => n.textContent.trim())[0] || '';
        }
        return workName;
      }
      return '';
    }).filter(Boolean);
    if (workNames.length) workSummary = workNames.join(', ');
  }
  document.getElementById('selected-works-list').textContent = workSummary;
  // Show or hide the summary box (employees handled in employees script)
  const empChecked = document.querySelectorAll('input[name="employee_ids"]:checked');
  document.getElementById('selected-summary').style.display = (empChecked.length || workChecked.length) ? '' : 'none';
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[name="work_ids"]').forEach(cb => {
    cb.addEventListener('change', updateSelectedWorksSummary);
  });
  const selectAllWork = document.getElementById('select-all-works');
  if (selectAllWork) selectAllWork.addEventListener('change', updateSelectedWorksSummary);
  updateSelectedWorksSummary();
});
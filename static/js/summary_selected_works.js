// Update the summary of selected works

// Helper: safely get work name from checkbox row
function getWorkName(cb) {
  if (!cb) return '';
  const row = cb.closest('tr');
  if (!row) return '';
  const workNameCell = row.querySelector('td:nth-child(2)');
  if (!workNameCell) return '';
  const workName = Array.from(workNameCell.childNodes)
    .filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim())
    .map(n => n.textContent.trim())[0] || '';
  return workName;
}

// Main function to update the summary box
function updateSelectedWorksSummary() {
  const workCheckboxes = document.querySelectorAll('input[name="work_ids"]');
  const workChecked = document.querySelectorAll('input[name="work_ids"]:checked');
  const selectAllWork = document.getElementById('select-all-works');
  const worksListDiv = document.getElementById('selected-works-list');
  const summaryBox = document.getElementById('selected-summary');
  // Check elements before using
  if (!worksListDiv || !summaryBox) return;
  // Build the summary text
  let workSummary = 'No works selected';
  if (
    selectAllWork &&
    selectAllWork.checked &&
    workChecked.length === workCheckboxes.length &&
    workChecked.length > 0
  ) {
    workSummary = 'Selected all';
  } else {
    const workNames = Array.from(workChecked).map(getWorkName).filter(Boolean);
    if (workNames.length) {
      workSummary = workNames.slice(0, 5).join(', ') + (workNames.length > 5 ? ', ...' : '');
    }
  }
  worksListDiv.textContent = workSummary;

  // Show or hide the summary box (employees handled in employees script)
  const empChecked = document.querySelectorAll('input[name="employee_ids"]:checked');
  summaryBox.style.display = (empChecked.length || workChecked.length) ? '' : 'none';
}

// Initialize event listeners on DOM load
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[name="work_ids"]').forEach(cb => {
    cb.addEventListener('change', updateSelectedWorksSummary);
  });
  const selectAllWork = document.getElementById('select-all-works');
  if (selectAllWork) selectAllWork.addEventListener('change', updateSelectedWorksSummary);
  updateSelectedWorksSummary();
});
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
  if (!worksListDiv || !summaryBox) return;
  // Build the summary text
  let workSummary = 'No works selected';
  let workNames = Array.from(workChecked).map(getWorkName).filter(Boolean);

  // If all checkboxes are checked and there is at least one, show 'Selected all'
  if (
    selectAllWork &&
    selectAllWork.checked &&
    workChecked.length === workCheckboxes.length &&
    workChecked.length > 0
  ) {
    workSummary = 'Selected all';
    worksListDiv.textContent = workSummary;
    // Remove full summary if open
    const fullSummary = document.getElementById('works-full-summary');
    if (fullSummary) fullSummary.remove();
  } else if (workNames.length) {
    workSummary = workNames.slice(0, 5).join(', ');
    if (workNames.length > 5) {
      workSummary += ', ';
      let moreSpan = worksListDiv.querySelector('.works-summary-more');
      if (moreSpan) moreSpan.remove();
      moreSpan = document.createElement('span');
      moreSpan.textContent = '...';
      moreSpan.className = 'works-summary-more cursor-pointer text-blue-500 underline';
      moreSpan.onclick = function() {
        toggleWorksFullSummary(workNames);
      };
      worksListDiv.textContent = workSummary;
      worksListDiv.appendChild(moreSpan);
    } else {
      worksListDiv.textContent = workSummary;
      const fullSummary = document.getElementById('works-full-summary');
      if (fullSummary) fullSummary.remove();
    }
  } else {
    worksListDiv.textContent = workSummary;
    const fullSummary = document.getElementById('works-full-summary');
    if (fullSummary) fullSummary.remove();
  }

  // Show or hide the summary box
  const empChecked = document.querySelectorAll('input[name="employee_ids"]:checked');
  summaryBox.style.display = (empChecked.length || workChecked.length) ? '' : 'none';
}

// Toggle dropdown summary below the list
function toggleWorksFullSummary(workNames) {
  let fullSummary = document.getElementById('works-full-summary');
  if (fullSummary) {
    fullSummary.remove();
    return;
  }
  const worksListDiv = document.getElementById('selected-works-list');
  fullSummary = document.createElement('div');
  fullSummary.id = 'works-full-summary';
  fullSummary.className = 'mt-2 p-2 text-sm';
  fullSummary.textContent = workNames.join(', ');
  worksListDiv.parentNode.insertBefore(fullSummary, worksListDiv.nextSibling);
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
// Universal checkbox selection validation for tables.
function setupCheckboxValidation(formId, checkboxName, tableSelector, errorMessage) {
  const form = document.getElementById(formId);
  if (!form) return;
  const tableDiv = document.querySelector(tableSelector);
  if (!tableDiv) return;
  // Show error: add red border and error message
  function showError() {
    tableDiv.classList.add('border-red-500');
    let errorDiv = document.getElementById(`${checkboxName}-selection-error`);
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.id = `${checkboxName}-selection-error`;
      errorDiv.className = 'text-red-500 text-sm';
      errorDiv.textContent = errorMessage;
      tableDiv.parentNode.insertBefore(errorDiv, tableDiv.nextSibling);
    }
  }
  // Hide error: remove red border and error message
  function hideError() {
    if (!document.getElementById('amount-error')) {
      tableDiv.classList.remove('border-red-500');
    }
    const errorDiv = document.getElementById(`${checkboxName}-selection-error`);
    if (errorDiv) errorDiv.remove();
  }
  // On form submission
  form.addEventListener('submit', function (e) {
    const checked = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
    if (checked.length === 0) {
      e.preventDefault();
      showError();
    } else {
      hideError();
    }
  });
  // Add change event listener to checkboxes
  document.querySelectorAll(`input[name="${checkboxName}"]`).forEach(cb => {
    cb.addEventListener('change', function () {
      const checked = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
      if (checked.length > 0) hideError();
    });
  });
}
// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
  // Example usage:
  // setupCheckboxValidation('myForm', 'employee_ids', '.employee-table-container', 'Select at least one employee');
});
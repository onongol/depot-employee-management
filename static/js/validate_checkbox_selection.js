// Universal checkbox selection validation for tables.
// Usage: setupCheckboxValidation(formId, checkboxName, tableSelector, errorMessage);

function setupCheckboxValidation(formId, checkboxName, tableSelector, errorMessage) {
  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener('submit', function (e) {
      const checked = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
      let errorDiv = document.getElementById(`${checkboxName}-selection-error`);
      const tableDiv = document.querySelector(tableSelector);
      if (checked.length === 0) {
        e.preventDefault();
        // Add red border to the table container
        tableDiv.classList.add('border-red-500');
        if (!errorDiv) {
          errorDiv = document.createElement('div');
          errorDiv.id = `${checkboxName}-selection-error`;
          errorDiv.className = 'text-red-500 text-sm';
          errorDiv.textContent = errorMessage;
          tableDiv.parentNode.insertBefore(errorDiv, tableDiv.nextSibling);
        }
      } else {
        // Remove red border and error message if present
        tableDiv.classList.remove('border-red-500');
        if (errorDiv) {
          errorDiv.remove();
        }
      }
    });
  });
}
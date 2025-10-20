// Universal checkbox selection validation for tables.

// Utility: show error message and add red border
function showSelectionError(tableDiv, errorId, errorMessage) {
  if (!tableDiv) return;
  tableDiv.classList.add('border-red-500', 'dark:border-red-500'); // добавлено
  let errorDiv = document.getElementById(errorId);
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.id = errorId;
    errorDiv.className = 'text-red-500 text-sm';
    errorDiv.textContent = errorMessage;
    tableDiv.parentNode.insertBefore(errorDiv, tableDiv.nextSibling);
  }
}

// Utility: hide error message and remove red border
function hideSelectionError(tableDiv, errorId) {
  if (!tableDiv) return;
  if (!document.getElementById('amount-error')) {
    tableDiv.classList.remove('border-red-500', 'dark:border-red-500'); // добавлено
  }
  const errorDiv = document.getElementById(errorId);
  if (errorDiv) errorDiv.remove();
}

// Main function to set up validation
function setupCheckboxValidation(formId, checkboxName, tableSelector, errorMessage) {
  const form = document.getElementById(formId);
  if (!form) return;
  const tableDiv = document.querySelector(tableSelector);
  if (!tableDiv) return;
  const errorId = `${checkboxName}-selection-error`;

  // On form submission
  form.addEventListener('submit', function (e) {
    const checked = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
    if (checked.length === 0) {
      e.preventDefault();
      showSelectionError(tableDiv, errorId, errorMessage);
    } else {
      hideSelectionError(tableDiv, errorId);
    }
  });

  // Add change event listener to checkboxes
  document.querySelectorAll(`input[name="${checkboxName}"]`).forEach(cb => {
    cb.addEventListener('change', function () {
      const checked = document.querySelectorAll(`input[name="${checkboxName}"]:checked`);
      if (checked.length > 0) hideSelectionError(tableDiv, errorId);
    });
  });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
  // Example usage:
  // setupCheckboxValidation('myForm', 'employee_ids', '.employee-table-container', 'Select at least one employee');
});
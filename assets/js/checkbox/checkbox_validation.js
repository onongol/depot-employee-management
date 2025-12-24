// Validates checkbox selection in tables: shows/removes error messages and red border on submit/change, preventing form submission when no checkboxes are checked; exposes setupCheckboxValidation for per-form setup.

// Utility: show error message and add red border
function showSelectionError(tableDiv, errorId, errorMessage) {
  if (!tableDiv) return;
  tableDiv.classList.add('border-red-500', 'dark:border-red-500');
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
    tableDiv.classList.remove('border-red-500', 'dark:border-red-500');
  }
  const errorDiv = document.getElementById(errorId);
  if (errorDiv) errorDiv.remove();
}

// Main function to set up validation
function setupCheckboxValidation(formId, checkboxName, tableSelector, errorMessage) {
  const form = document.getElementById(formId);
  if (!form) return;
  // prefer table inside the form, fallback to global
  const tableDiv = form.querySelector(tableSelector) || document.querySelector(tableSelector);
  if (!tableDiv) return;
  const errorId = `${checkboxName}-selection-error`;

  // submit handler scoped to form
  form.addEventListener('submit', function (e) {
    const checked = form.querySelectorAll(`input[name="${checkboxName}"]:checked`);
    if (checked.length === 0) {
      e.preventDefault();
      showSelectionError(tableDiv, errorId, errorMessage);
    } else {
      hideSelectionError(tableDiv, errorId);
    }
  });

  // delegate change events inside the form (works for dynamic inputs)
  form.addEventListener('change', function (e) {
    if (!e.target) return;
    if (e.target.name === checkboxName) {
      const checked = form.querySelectorAll(`input[name="${checkboxName}"]:checked`);
      if (checked.length > 0) hideSelectionError(tableDiv, errorId);
    }
  });

  // also hide error when a "select-all" checkbox inside the table is toggled
  const selectAll = tableDiv.querySelector('input[type="checkbox"][id^="select-all"]');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      const checked = form.querySelectorAll(`input[name="${checkboxName}"]:checked`);
      if (checked.length > 0) hideSelectionError(tableDiv, errorId);
    });
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function () {
  // Example usage:
  // setupCheckboxValidation('myForm', 'employee_ids', '.employee-table-container', 'Select at least one employee');
});

if (typeof window !== 'undefined') {
  window.setupCheckboxValidation = setupCheckboxValidation;
}
(function () {
  // UI helpers
  // Add or remove red border classes for invalid inputs
  function addRedBorder(input) {
    if (input) input.classList.add(
      'border-red-500', 'focus:border-red-500', 'focus:ring-red-500',
      'dark:border-red-500', 'dark:focus:border-red-500', 'dark:focus:ring-red-500'
    );
  }
  function removeRedBorder(input) {
    if (input) input.classList.remove(
      'border-red-500', 'focus:border-red-500', 'focus:ring-red-500',
      'dark:border-red-500', 'dark:focus:border-red-500', 'dark:focus:ring-red-500'
    );
  }
  
  // Show or clear error message below the container
  function showAmountError(message, container) {
    if (!container) return;
    let errorDiv = document.getElementById('amount-error');
    if (errorDiv) errorDiv.remove();
    errorDiv = document.createElement('div');
    errorDiv.id = 'amount-error';
    errorDiv.className = 'text-red-500 text-sm mb-2';
    errorDiv.textContent = message;
    container.parentNode.insertBefore(errorDiv, container.nextSibling);
    container.classList.add('border-red-500', 'dark:border-red-500');
  }

  // Clear error message and red border from container
  function clearAmountError(container) {
    if (!container) return;
    const errorDiv = document.getElementById('amount-error');
    if (errorDiv) errorDiv.remove();
    if (!document.getElementById('work_ids-selection-error')) {
      container.classList.remove('border-red-500', 'dark:border-red-500');
    }
  }

  // Core validation logic
  function validateSelectedWorkAmounts(checkboxName, containerSelector, message) {
    const container = document.querySelector(containerSelector);
    // Reset any previous invalid state across all amount inputs.
    document.querySelectorAll('input[id^="amount_"]').forEach(removeRedBorder);

    // Collect all checked work checkboxes.
    const selected = Array.from(document.querySelectorAll(`input[name="${checkboxName}"]:checked`));
    if (selected.length === 0) {
      clearAmountError(container);
      return true;
    }

    // Validate each selected work's amount input.
    let invalid = false;
    selected.forEach(cb => {
      const input = document.getElementById(`amount_${cb.value}`);
      const val = input ? String(input.value).trim() : '';
      if (!input || val === '' || isNaN(val) || Number(val) <= 0) {
        invalid = true;
        addRedBorder(input);
      }
    });

    // If any invalid input found, show message and stop form submission.
    if (invalid) {
      if (container) container.scrollIntoView({ behavior: 'smooth', block: 'start' });
      showAmountError(message, container);
      return false;
    }

    // All good: cleanup UI state.
    clearAmountError(container);
    return true;
  }

  // Public initializer function
  window.setupAmountValidation = function (formId, checkboxName, containerSelector, message) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Validate on form submit
    form.addEventListener('submit', function (e) {
      if (!validateSelectedWorkAmounts(checkboxName, containerSelector, message)) {
        e.preventDefault();
      }
    });
  };
})();
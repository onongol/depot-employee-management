// Validate that amount inputs are filled for selected works
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('createForm');
  if (!form) return;

  // Helper: add red border to input
  function addRedBorder(input) {
    if (input) {
      input.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    }
  }

  // Helper: remove red border from input
  function removeRedBorder(input) {
    if (input) {
      input.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    }
  }

  // Helper: show error message below works table
  function showAmountError(message, worksTable) {
    if (!worksTable) return;
    let errorDiv = document.getElementById('amount-error');
    if (errorDiv) errorDiv.remove();
    errorDiv = document.createElement('div');
    errorDiv.id = 'amount-error';
    errorDiv.className = 'text-red-500 text-sm mb-2';
    errorDiv.textContent = message;
    worksTable.parentNode.insertBefore(errorDiv, worksTable.nextSibling);
    worksTable.classList.add('border-red-500');
  }

  // Helper: remove error message and red border from table
  function clearAmountError(worksTable) {
    if (!worksTable) return;
    const errorDiv = document.getElementById('amount-error');
    if (errorDiv) errorDiv.remove();
    if (!document.getElementById('work_ids-selection-error')) {
      worksTable.classList.remove('border-red-500');
    }
  }

  // On form submission
  form.addEventListener('submit', function (e) {
    const checkedWorks = Array.from(document.querySelectorAll('input[name="work_ids"]:checked'));
    let missing = [];
    // Remove red borders from all amount inputs
    document.querySelectorAll('input[name^="amount_"]').forEach(removeRedBorder);

    // Check each checked work for corresponding amount input
    checkedWorks.forEach(workCheckbox => {
      const workId = workCheckbox.value;
      const amountInput = document.querySelector(`input[name="amount_${workId}"]`);
      if (!amountInput || !amountInput.value) {
        const workName =
          workCheckbox.dataset.workName ||
          (workCheckbox.closest('tr') && workCheckbox.closest('tr').querySelector('.work-name') ?
            workCheckbox.closest('tr').querySelector('.work-name').textContent.trim() : workId);
        missing.push(workName);
        addRedBorder(amountInput);
      }
    });

    const worksTable = document.querySelector('.works-table-container');
    if (missing.length > 0) {
      e.preventDefault();
      showAmountError('Please fill in the amount for selected work(s)', worksTable);
    } else {
      clearAmountError(worksTable);
    }
  });
});
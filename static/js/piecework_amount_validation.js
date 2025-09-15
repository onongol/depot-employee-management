// Validate that amount inputs are filled for selected works
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('createForm');
  if (!form) return;
  // On form submission
  form.addEventListener('submit', function (e) {
    const checkedWorks = Array.from(document.querySelectorAll('input[name="work_ids"]:checked'));
    let missing = [];
    // First, remove red borders from all amount inputs
    document.querySelectorAll('input[name^="amount_"]').forEach(input => {
      input.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    });
    // Check each checked work for corresponding amount input
    checkedWorks.forEach(workCheckbox => {
      const workId = workCheckbox.value;
      const amountInput = document.querySelector(`input[name="amount_${workId}"]`);
      if (!amountInput || !amountInput.value) {
        const workName = workCheckbox.dataset.workName || workCheckbox.closest('tr').querySelector('.work-name').textContent.trim();
        missing.push(workName);
        // Add red border to this field
        if (amountInput) {
          amountInput.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        }
      }
    });
    // Delete previous error message if exists
    let errorDiv = document.getElementById('amount-error');
    if (errorDiv) errorDiv.remove();
    // Remove red border from table if no error
    const worksTable = document.querySelector('.works-table-container');
    if (missing.length > 0) {
      e.preventDefault();
      // Add error message below the works table
      errorDiv = document.createElement('div');
      errorDiv.id = 'amount-error';
      errorDiv.className = 'text-red-500 text-sm mb-2';
      errorDiv.textContent = 'Please fill in the amount for selected work(s)';
      worksTable.parentNode.insertBefore(errorDiv, worksTable.nextSibling);
      // Add red border to table
      worksTable.classList.add('border-red-500');
    } else {
      // Remove red border only if no error
      if (!document.getElementById('work_ids-selection-error')) {
        worksTable.classList.remove('border-red-500');
      }
    }
  });
});
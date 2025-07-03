// This script manages the enabling and disabling of amount inputs based on work checkbox selections.
document.addEventListener('DOMContentLoaded', function () {
  function updateAmountInput(checkbox) {
    const amountInput = document.getElementById('amount_' + checkbox.value);
    if (amountInput) {
      amountInput.disabled = !checkbox.checked;
      if (!checkbox.checked) {
        amountInput.value = '';
      }
    }
  }

  // Enable/disable amount input based on work checkbox
  document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
    updateAmountInput(checkbox);
    checkbox.addEventListener('change', function () {
      updateAmountInput(checkbox);
    });
  });

  // Handle "Select all works" checkbox
  const selectAllWorks = document.getElementById('select-all-works');
  if (selectAllWorks) {
    selectAllWorks.addEventListener('change', function () {
      document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
        updateAmountInput(checkbox);
      });
    });
  }

  // Prevent form submission on Enter key in amount inputs
  document.querySelectorAll('.amount-input').forEach(function(input) {
    input.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.keyCode === 13) {
        event.preventDefault();
      }
    });
  });
});
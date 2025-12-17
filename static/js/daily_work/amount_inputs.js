// Manages enabling/disabling amount inputs tied to work checkboxes: toggles input disabled state on checkbox changes, handles "select all", prevents Enter from submitting amount fields, and initializes input states on page load.

document.addEventListener('DOMContentLoaded', function () {
  // Update amount input state for a single checkbox
  function updateAmountInput(checkbox) {
    if (!checkbox) return;
    const amountInput = document.getElementById('amount_' + checkbox.value);
    if (amountInput) {
      amountInput.disabled = !checkbox.checked;
      if (!checkbox.checked) {
        amountInput.value = '';
      }
    }
  }

  // Update all work checkboxes and their amount inputs
  function updateAllWorkCheckboxes() {
    document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
      updateAmountInput(checkbox);
    });
  }

  // Explicitly check/uncheck all work checkboxes
  function setAllWorkCheckboxes(checked) {
    document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
      checkbox.checked = checked;
      updateAmountInput(checkbox);
    });
  }

  // Initial setup for all work checkboxes
  updateAllWorkCheckboxes();
  document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
      updateAmountInput(checkbox);
    });
  });

  // Handle "Select all works" checkbox
  const selectAllWorks = document.getElementById('select-all-works');
  if (selectAllWorks) {
    selectAllWorks.addEventListener('change', function () {
      // Toggle all checkboxes based on the "Select all works" checkbox
      window.toggleAllVisible(selectAllWorks, 'work_ids');
      // After that, update amount fields only for visible checkboxes
      document.querySelectorAll('.work-checkbox').forEach(function (checkbox) {
        if (checkbox.offsetParent !== null) {
          updateAmountInput(checkbox);
        }
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
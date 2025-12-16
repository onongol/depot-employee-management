// This script handles the duplicate check for piecework entries in a form.
document.addEventListener('DOMContentLoaded', function () {
  // Read server data injected via json_script
  const existingPieceworksEl = document.getElementById('existing-pieceworks');
  const existingPieceworks = existingPieceworksEl ? JSON.parse(existingPieceworksEl.textContent) : [];

  // Get form by ID
  const form = document.getElementById('createForm');
  if (!form) return;
  // Get elements for modal and buttons
  const modalDiv = document.getElementById('saveDuplicateModal');
  const confirmBtn = document.getElementById('confirmSaveBtn');
  const cancelBtn = document.querySelector('#saveDuplicateModal [data-modal-cancel]');
  let allowSubmit = false; // Flag to control form submission

  // Open the modal
  function openModal() {
    modalDiv.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  // Close the modal
  function closeModal() {
    modalDiv.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  // Form submission handler
  form.addEventListener('submit', function (e) {
    if (allowSubmit) {
      allowSubmit = false;  // Reset flag
      return;
    }

    // No duplicate modal if there's an amount error
    if (document.getElementById('amount-error')) {
      // Error is already shown, no duplicate modal needed
      return;
    }

    // Collect selected employee and work IDs
    const selectedEmployeeIds = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => cb.value);
    const selectedWorkIds = Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.value);
    // Get values type work, work date, and wagon number
    const typeWork = document.getElementById('type_work').value;
    const workDate = document.getElementById('work_date').value;
    const wagonNumberInput = document.getElementById('wagon_number');
    let wagonNumber = wagonNumberInput && wagonNumberInput.value ? wagonNumberInput.value.trim() : '';
    wagonNumber = wagonNumber === '' ? null : wagonNumber; // Normalize empty to null

    // Helper function to normalize wagon number for comparison
    function normalizeWagon(val) {
      if (val === null || val === undefined) return null;
      return String(val).trim();
    }

    let isDuplicate = false;  // Flag to track duplicates
    // Iterate through selected employees and works to check for duplicates
    for (const empId of selectedEmployeeIds) {
      for (const workId of selectedWorkIds) {
        // Check against existing pieceworks
        if (existingPieceworks.some(pw =>
          String(pw.employee_id) === String(empId) &&
          String(pw.work_id) === String(workId) &&
          pw.type_work === typeWork &&
          pw.work_date === workDate &&
          normalizeWagon(pw.wagon_number) === normalizeWagon(wagonNumber)
        )) {
          isDuplicate = true;
        }
      }
    }
    if (isDuplicate) {
      e.preventDefault(); // Stop form submission

      // Collect selected employee names and work names for modal display
      const selectedEmployees = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => {
        const tr = cb.closest('tr');
        const id = cb.value;
        const name = tr.children[2].textContent.trim();
        return `${id}/${name}`;
      });
      // Collect selected work names, ensuring uniqueness
      const selectedWorks = Array.from(new Set(
        Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.dataset.workName)
      ));
      // Fill modal content with collected data
      document.getElementById('modal-employee').textContent = selectedEmployees.join(', ');
      document.getElementById('modal-work').textContent = selectedWorks.join(', ');
      document.getElementById('modal-type-work').textContent = typeWork;
      document.getElementById('modal-wagon-number').textContent = wagonNumber || '-';
      document.getElementById('modal-work-date').textContent = workDate;
      openModal(); // Show the modal
    }
    // else, allow form to submit
  });

  // Confirm button allows submission and closes modal
  confirmBtn.addEventListener('click', function () {
    allowSubmit = true;
    closeModal();
    form.requestSubmit();
  });

  // Cancel button closes modal and restores scroll
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function () {
      closeModal();
    });
  }

  // Esc closes modal and restores scroll
  document.addEventListener('keydown', function (e) {
    if (!modalDiv.classList.contains('hidden') && e.key === 'Escape') {
      closeModal();
    }
  });
});
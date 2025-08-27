// This script handles the duplicate check for piecework entries in a form.
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('createForm');
  if (!form) return;
  const modalDiv = document.getElementById('saveDuplicateModal');
  const confirmBtn = document.getElementById('confirmSaveBtn');
  const cancelBtn = document.querySelector('#saveDuplicateModal [data-modal-cancel]');
  let allowSubmit = false;

  function openModal() {
    modalDiv.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }
  function closeModal() {
    modalDiv.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  form.addEventListener('submit', function (e) {
    if (allowSubmit) {
      allowSubmit = false;
      return;
    }
    // Gather selected IDs
    const selectedEmployeeIds = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => cb.value);
    const selectedWorkIds = Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.value);
    const typeWork = document.getElementById('type_work').value;
    const workDate = document.getElementById('work_date').value;
    const wagonNumberInput = document.getElementById('wagon_number');
    let wagonNumber = wagonNumberInput && wagonNumberInput.value ? wagonNumberInput.value.trim() : '';
    wagonNumber = wagonNumber === '' ? null : wagonNumber;

    function normalizeWagon(val) {
      if (val === null || val === undefined) return null;
      return String(val).trim();
    }

    let isDuplicate = false;
    for (const empId of selectedEmployeeIds) {
      for (const workId of selectedWorkIds) {
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
      e.preventDefault();
      // Fill modal fields with IDs and names for user clarity
      const selectedEmployees = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => {
        const tr = cb.closest('tr');
        const id = cb.value;
        const name = tr.children[2].textContent.trim();
        return `${id}/${name}`;
      });
      const selectedWorks = Array.from(new Set(
        Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.dataset.workName)
      ));
      document.getElementById('modal-employee').textContent = selectedEmployees.join(', ');
      document.getElementById('modal-work').textContent = selectedWorks.join(', ');
      document.getElementById('modal-type-work').textContent = typeWork;
      document.getElementById('modal-wagon-number').textContent = wagonNumber || '-';
      document.getElementById('modal-work-date').textContent = workDate;
      openModal();
    }
    // else, allow form to submit
  });

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
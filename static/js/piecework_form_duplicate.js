// This script handles the duplicate check for piecework entries in a form.
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('createForm');
  if (!form) return;
  const modalDiv = document.getElementById('saveDuplicateModal');
  const confirmBtn = document.getElementById('confirmSaveBtn');
  const cancelBtn = document.querySelector('#saveDuplicateModal [data-modal-cancel]');
  let allowSubmit = false;

  // Helper: safely set modal field text
  function setModalField(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  // Fill modal fields with selected data
  function fillDuplicateModal(selectedEmployees, selectedWorks, typeWork, wagonNumber, workDate) {
    setModalField('modal-employee', selectedEmployees.join(', '));
    setModalField('modal-work', selectedWorks.join(', '));
    setModalField('modal-type-work', typeWork);
    setModalField('modal-wagon-number', wagonNumber || '-');
    setModalField('modal-work-date', workDate);
  }

  function openModal() {
    if (!modalDiv) return;
    modalDiv.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }
  function closeModal() {
    if (!modalDiv) return;
    modalDiv.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  // Optimize duplicate check using Set
  function getPieceworkKey(pw) {
    return [
      pw.employee_id,
      pw.work_id,
      pw.type_work,
      pw.work_date,
      pw.wagon_number ? String(pw.wagon_number).trim() : ''
    ].join('|');
  }
  // Build a Set of existing piecework keys for fast lookup
  const existingKeys = new Set(
    (window.existingPieceworks || []).map(getPieceworkKey)
  );

  form.addEventListener('submit', function (e) {
    if (allowSubmit) {
      allowSubmit = false;
      return;
    }
    const selectedEmployeeIds = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => cb.value);
    const selectedWorkIds = Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.value);
    const typeWork = document.getElementById('type_work')?.value || '';
    const workDate = document.getElementById('work_date')?.value || '';
    const wagonNumberInput = document.getElementById('wagon_number');
    let wagonNumber = wagonNumberInput && wagonNumberInput.value ? wagonNumberInput.value.trim() : '';
    wagonNumber = wagonNumber === '' ? null : wagonNumber;

    // Check for duplicates using Set
    let isDuplicate = false;
    for (const empId of selectedEmployeeIds) {
      for (const workId of selectedWorkIds) {
        const key = [
          empId,
          workId,
          typeWork,
          workDate,
          wagonNumber ? String(wagonNumber).trim() : ''
        ].join('|');
        if (existingKeys.has(key)) {
          isDuplicate = true;
        }
      }
    }

    if (isDuplicate) {
      e.preventDefault();
      // Prepare modal data
      const selectedEmployees = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => {
        const tr = cb.closest('tr');
        const id = cb.value;
        const name = tr?.children[2]?.textContent.trim() || '';
        return `${id}/${name}`;
      });
      const selectedWorks = Array.from(new Set(
        Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.dataset.workName)
      ));
      fillDuplicateModal(selectedEmployees, selectedWorks, typeWork, wagonNumber, workDate);
      openModal();
    }
    // else, allow form to submit
  });

  if (confirmBtn) {
    confirmBtn.addEventListener('click', function () {
      allowSubmit = true;
      closeModal();
      form.requestSubmit();
    });
  }
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function () {
      closeModal();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (!modalDiv?.classList.contains('hidden') && e.key === 'Escape') {
      closeModal();
    }
  });
});
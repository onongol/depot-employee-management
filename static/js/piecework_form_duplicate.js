// This script handles the duplicate check for piecework entries in a form.
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('createForm');
  if (!form) return;
  const modalDiv = document.getElementById('saveDuplicateModal');
  const confirmBtn = document.getElementById('confirmSaveBtn');
  let allowSubmit = false;
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
    let isDuplicate = false;
    for (const empId of selectedEmployeeIds) {
      for (const workId of selectedWorkIds) {
        if (existingPieceworks.some(pw =>
          String(pw.employee_id) === String(empId) &&
          String(pw.work_id) === String(workId) &&
          pw.type_work === typeWork &&
          pw.work_date === workDate
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
      document.getElementById('modal-work-date').textContent = workDate;
      document.getElementById('saveDuplicateModal').classList.remove('hidden');
    }
    // else, allow form to submit
  });
  confirmBtn.addEventListener('click', function () {
    allowSubmit = true;
    modalDiv.classList.add('hidden');
    form.requestSubmit();
  });
});
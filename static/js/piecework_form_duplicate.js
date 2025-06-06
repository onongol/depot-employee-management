// This script handles the duplicate check for piecework entries in a form.
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('create_form');
  if (!form) return;
  const modal = new bootstrap.Modal(document.getElementById('saveDuplicateModal'));
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
      // Fill modal fields with names for user clarity
      const selectedEmployees = Array.from(document.querySelectorAll('input[name="employee_ids"]:checked')).map(cb => cb.closest('tr').children[2].textContent.trim());
      const selectedWorks = Array.from(document.querySelectorAll('input[name="work_ids"]:checked')).map(cb => cb.closest('tr').children[1].textContent.trim());
      document.getElementById('modal-employee').textContent = selectedEmployees.join(', ');
      document.getElementById('modal-work').textContent = selectedWorks.join(', ');
      document.getElementById('modal-type-work').textContent = typeWork;
      document.getElementById('modal-work-date').textContent = workDate;
      modal.show();
    }
    // else, allow form to submit
  });
  confirmBtn.addEventListener('click', function () {
    allowSubmit = true;
    modal.hide();
    form.requestSubmit(); // re-submit the form
  });
});
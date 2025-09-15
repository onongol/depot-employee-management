// Get elements
const saveBtn = document.getElementById('saveButton');
const saveModal = document.getElementById('saveModal');
const confirmBtn = document.getElementById('confirmSaveButton');
const updateForm = document.getElementById('updateForm');
// Open modal and stop scroll
if (saveBtn && saveModal) {
  saveBtn.addEventListener('click', function() {
    saveModal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  });
}
// Submit form on confirm
if (confirmBtn && updateForm) {
  confirmBtn.addEventListener('click', function() {
    updateForm.submit();
  });
}
// Close modal on Esc
if (saveModal) {
  document.addEventListener('keydown', function(e) {
    if (!saveModal.classList.contains('hidden') && e.key === 'Escape') {
      saveModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }
  });
}
// Close modal on Cancel
if (saveModal) {
  document.querySelectorAll('[data-modal-cancel]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      saveModal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    });
  });
}
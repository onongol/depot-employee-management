// Shows a confirmation modal before saving: opens modal on Save click, prevents page scroll, submits the form on confirm, and closes modal on Escape or Cancel.

(function () {
  const saveBtn = document.getElementById('saveButton');
  const saveModal = document.getElementById('saveModal');
  const confirmBtn = document.getElementById('confirmSaveButton');
  const updateForm = document.getElementById('updateForm');

  // Reusable closer
  function closeSaveModal() {
    if (!saveModal) return;
    saveModal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  // Open modal and stop scroll
  if (saveBtn && saveModal) {
    saveBtn.addEventListener('click', function (e) {
      e.preventDefault();
      saveModal.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    });
  }

  // Submit form on confirm
  if (confirmBtn && updateForm) {
    confirmBtn.addEventListener('click', function (e) {
      e.preventDefault();
      updateForm.submit();
    });
  }

  // Close modal on Esc
  if (saveModal) {
    document.addEventListener('keydown', function (e) {
      if (!saveModal.classList.contains('hidden') && e.key === 'Escape') {
        closeSaveModal();
      }
    });

    // Close modal on Cancel
    document.querySelectorAll('[data-modal-cancel]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        closeSaveModal();
      });
    });
  }
})();
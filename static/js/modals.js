// Modal management: open/close modals, populate dynamic content, focus management
document.addEventListener("DOMContentLoaded", function () {
  // Focus first input in modal
  function openModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    focusFirst(modalId);
  }
  // Close all modals and restore scroll
  function closeAllModals() {
    document.querySelectorAll('.fixed.inset-0').forEach(function (modal) {
      modal.classList.add('hidden');
    });
    document.body.classList.remove('overflow-hidden');
  }
  // Edit
  document.querySelectorAll('button[aria-label^="Edit"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const updateUrl = button.getAttribute("data-url");
      document.getElementById("updateLink").href = updateUrl;
      document.getElementById("updateDetails").textContent = `${itemId}/${itemName}`;
      openModal('updateModal');
    });
  });
  // Delete
  document.querySelectorAll('button[aria-label^="Delete"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const itemUrl = button.getAttribute("data-url");
      document.getElementById("deleteForm").action = itemUrl;
      document.getElementById("deleteDetails").textContent = `${itemId}/${itemName}`;
      openModal('deleteModal');
    });
  });
  // Close modals with Esc
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });
  // Close modals on Cancel button
  document.querySelectorAll('[data-modal-cancel]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      closeAllModals();
    });
  });
});
// Modal functionality for editing, deleting, activating, and deactivating employees
document.addEventListener("DOMContentLoaded", function () {
  // Focus first button in modal
  function openModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    focusFirst(modalId);
  }
  // Focus first button in the modal
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
  // Deactivate
  document.querySelectorAll('a[aria-label^="Deactivate"]').forEach(function (button) {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const deactivateUrl = button.getAttribute("href");
      document.getElementById("deactivateLink").href = deactivateUrl;
      document.getElementById("deactivateDetails").textContent = `${itemId}/${itemName}`;
      openModal('deactivateModal');
    });
  });
  // Activate
  document.querySelectorAll('a[aria-label^="Activate"]').forEach(function (button) {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const activateUrl = button.getAttribute("href");
      document.getElementById("activateLink").href = activateUrl;
      document.getElementById("activateDetails").textContent = `${itemId}/${itemName}`;
      openModal('activateModal');
    });
  });
  // Close modals with Esc
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });
  // Close modals when clicking outside content
  document.querySelectorAll('[data-modal-cancel]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      closeAllModals();
    });
  });
});
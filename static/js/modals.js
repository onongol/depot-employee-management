// Modal management: open/close modals, populate dynamic content, focus management
document.addEventListener("DOMContentLoaded", function () {
  // Focus first input in modal
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.warn(`Modal with id "${modalId}" not found`);
      return;
    }
    modal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    if (typeof focusFirst === 'function') focusFirst(modalId);
  }

  // Close all modals and restore scroll
  function closeAllModals() {
    document.querySelectorAll('.fixed.inset-0').forEach(function (modal) {
      modal.classList.add('hidden');
    });
    document.body.classList.remove('overflow-hidden');
  }

  // Safe setters with error handling
  function safeSetText(id, value) {
    const el = document.getElementById(id);
    if (!el) {
      console.warn(`Element with id "${id}" not found`);
      return;
    }
    el.textContent = value;
  }
  function safeSetHref(id, value) {
    const el = document.getElementById(id);
    if (!el) {
      console.warn(`Element with id "${id}" not found`);
      return;
    }
    el.href = value;
  }
  function safeSetAction(id, value) {
    const el = document.getElementById(id);
    if (!el) {
      console.warn(`Element with id "${id}" not found`);
      return;
    }
    el.action = value;
  }

  // Fill modal details based on type
  function fillModalDetails(modalType, itemId, itemName, url) {
    if (modalType === 'edit') {
      safeSetHref('updateLink', url);
      safeSetText('updateDetails', `${itemId}/${itemName}`);
    } else if (modalType === 'delete') {
      safeSetAction('deleteForm', url);
      safeSetText('deleteDetails', `${itemId}/${itemName}`);
    }
  }

  // Edit
  document.querySelectorAll('button[aria-label^="Edit"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const updateUrl = button.getAttribute("data-url");
      fillModalDetails('edit', itemId, itemName, updateUrl);
      openModal('updateModal');
    });
  });

  // Delete
  document.querySelectorAll('button[aria-label^="Delete"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const itemUrl = button.getAttribute("data-url");
      fillModalDetails('delete', itemId, itemName, itemUrl);
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
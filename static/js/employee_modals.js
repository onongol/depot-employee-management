// Modal functionality for editing, deleting, activating, and deactivating employees
document.addEventListener("DOMContentLoaded", function () {
  // Focus first button in modal
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('hidden');
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

  // Deactivate
  document.querySelectorAll('a[aria-label^="Deactivate"]').forEach(function (button) {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const deactivateUrl = button.getAttribute("href");
      fillModalDetails('deactivate', itemId, itemName, deactivateUrl);
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
      fillModalDetails('activate', itemId, itemName, activateUrl);
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
function fillModalDetails(type, id, name, url) {
  if (type === 'edit') {
    safeSetHref('updateLink', url);
    safeSetText('updateDetails', `${id}/${name}`);
  } else if (type === 'delete') {
    safeSetAction('deleteForm', url);
    safeSetText('deleteDetails', `${id}/${name}`);
  } else if (type === 'deactivate') {
    safeSetHref('deactivateLink', url);
    safeSetText('deactivateDetails', `${id}/${name}`);
  } else if (type === 'activate') {
    safeSetHref('activateLink', url);
    safeSetText('activateDetails', `${id}/${name}`);
  }
}
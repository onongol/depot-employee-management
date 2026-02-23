// Manages modal dialogs for edit/delete/activate/deactivate actions: opens/closes modals, populates modal content and targets (links/forms), traps page scrolling, and binds keyboard/overlay close handlers.

type ModalType = 'edit' | 'delete' | 'deactivate' | 'activate';

const getEl = <T extends HTMLElement = HTMLElement>(id: string): T | null =>
  document.getElementById(id) as T | null;

document.addEventListener('DOMContentLoaded', () => {
  // Show modal and trap scroll
  function openModal(modalId: string): void {
    const modal = getEl<HTMLElement>(modalId);
    if (!modal) return;
    modal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  // Hide all modals and restore scroll
  function closeAllModals(): void {
    document.querySelectorAll<HTMLElement>('[role="dialog"]').forEach((modal) => {
      modal.classList.add('hidden');
    });
    document.body.classList.remove('overflow-hidden');
  }

  // Attach generic click handler for element lists
  function forEachButton(selector: string, cb: (el: HTMLElement) => void): void {
    document.querySelectorAll<HTMLElement>(selector).forEach(cb);
  }

  // Edit buttons
  forEachButton('button[aria-label^="Edit"]', (button) => {
    button.addEventListener('click', () => {
      const itemId = button.getAttribute('data-id') ?? '';
      const itemName = button.getAttribute('data-name') ?? '';
      const updateUrl = button.getAttribute('data-url') ?? '';
      fillModalDetails('edit', itemId, itemName, updateUrl);
      openModal('updateModal');
    });
  });

  // Delete buttons
  forEachButton('button[aria-label^="Delete"]', (button) => {
    button.addEventListener('click', () => {
      const itemId = button.getAttribute('data-id') ?? '';
      const itemName = button.getAttribute('data-name') ?? '';
      const itemUrl = button.getAttribute('data-url') ?? '';
      fillModalDetails('delete', itemId, itemName, itemUrl);
      openModal('deleteModal');
    });
  });

  // Deactivate links (anchors)
  forEachButton('a[aria-label^="Deactivate"]', (anchor) => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const itemId = anchor.getAttribute('data-id') ?? '';
      const itemName = anchor.getAttribute('data-name') ?? '';
      const deactivateUrl = (anchor as HTMLAnchorElement).href ?? '';
      fillModalDetails('deactivate', itemId, itemName, deactivateUrl);
      openModal('deactivateModal');
    });
  });

  // Activate links (anchors)
  forEachButton('a[aria-label^="Activate"]', (anchor) => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const itemId = anchor.getAttribute('data-id') ?? '';
      const itemName = anchor.getAttribute('data-name') ?? '';
      const activateUrl = (anchor as HTMLAnchorElement).href ?? '';
      fillModalDetails('activate', itemId, itemName, activateUrl);
      openModal('activateModal');
    });
  });

  // Close with Escape
  document.addEventListener('keydown', (e: KeyboardEvent) => {
    if (e.key === 'Escape') closeAllModals();
  });

  // Close when clicking elements marked as cancel
  forEachButton('[data-modal-cancel]', () => {
    // attach below: iterate again to bind handler
  });
  document.querySelectorAll<HTMLElement>('[data-modal-cancel]').forEach((btn) => {
    btn.addEventListener('click', () => closeAllModals());
  });
});

// Safe setters with strict typing
function safeSetText(id: string, value: string): void {
  const el = getEl<HTMLElement>(id);
  if (!el) {
    console.warn(`Element with id "${id}" not found`);
    return;
  }
  el.textContent = value;
}

function safeSetHref(id: string, value: string): void {
  const el = getEl<HTMLAnchorElement>(id);
  if (!el) {
    console.warn(`Element with id "${id}" not found`);
    return;
  }
  el.href = value;
}

function safeSetAction(id: string, value: string): void {
  const el = getEl<HTMLFormElement>(id);
  if (!el) {
    console.warn(`Element with id "${id}" not found`);
    return;
  }
  el.action = value;
}

// Fill modal details based on type
function fillModalDetails(type: ModalType, id: string, name: string, url: string): void {
  const details = name || id;
  switch (type) {
    case 'edit':
      safeSetHref('updateLink', url);
      safeSetText('updateDetails', details);
      break;
    case 'delete':
      safeSetAction('deleteForm', url);
      safeSetText('deleteDetails', details);
      break;
    case 'deactivate':
      safeSetHref('deactivateLink', url);
      safeSetText('deactivateDetails', details);
      break;
    case 'activate':
      safeSetHref('activateLink', url);
      safeSetText('activateDetails', details);
      break;
  }
}
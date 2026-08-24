/**
 * Modal Management System:
 * Handles CRUD-related modal dialogs (edit, delete, activate, etc.) using Event Delegation.
 * It manages content population, URL/Form action updates, and body scroll locking.
 */
type ModalType =
  "edit" | "delete" | "deactivate" | "activate" | "bulkDelete" | "confirmSave";

/**
 * Interface for modal triggers to ensure type safety when accessing dataset.
 */
interface ModalTrigger extends HTMLElement {
  dataset: DOMStringMap & {
    modalOpen?: ModalType;
    id?: string;
    name?: string;
    url?: string;
  };
}

/**
 * Type Guard to validate if a string matches the ModalType union.
 */
function isModalType(value: string | undefined): value is ModalType {
  return (
    value === "edit" ||
    value === "delete" ||
    value === "deactivate" ||
    value === "activate" ||
    value === "bulkDelete" ||
    value === "confirmSave"
  );
}

// Attribute used to prevent double initialization
const MODAL_INIT = {
  attr: "data-modals-init",
} as const;

// Prevents background scrolling when modal is open
const MODAL_SELECTORS = {
  dialogs: '[role="dialog"]',
  openTrigger: "[data-modal-open]",
  cancel: "[data-modal-cancel]",
} as const;

const MODAL_CLASSES = {
  hidden: "hidden",
  lockScroll: "overflow-hidden",
} as const;

const MODAL_KEYS = {
  escape: "Escape",
} as const;

/**
 * Mapping of Modal IDs and their internal child elements (links/forms/text).
 */
const MODAL_IDS = {
  updateModal: "updateModal",
  deleteModal: "deleteModal",
  deactivateModal: "deactivateModal",
  activateModal: "activateModal",
  bulkDeleteModal: "bulkDeleteModal",
  updateLink: "updateLink",
  updateDetails: "updateDetails",
  deleteForm: "deleteForm",
  deleteDetails: "deleteDetails",
  deactivateLink: "deactivateLink",
  deactivateDetails: "deactivateDetails",
  activateLink: "activateLink",
  activateDetails: "activateDetails",
  confirmSaveModal: "confirmSaveModal",
  confirmSaveObjectDetails: "confirmSaveObjectDetails",
} as const;

const MODAL_TYPE_TO_ID: Record<ModalType, string> = {
  edit: MODAL_IDS.updateModal,
  delete: MODAL_IDS.deleteModal,
  deactivate: MODAL_IDS.deactivateModal,
  activate: MODAL_IDS.activateModal,
  bulkDelete: MODAL_IDS.bulkDeleteModal,
  confirmSave: MODAL_IDS.confirmSaveModal,
};

/**
 * DOM Utility: safely get element by ID.
 */
const getById = (id: string): HTMLElement | null => document.getElementById(id);

/**
 * Opens a specific modal and locks the page scroll.
 */
function openModal(modalId: string): void {
  const modal = getById(modalId);
  if (!modal) return;
  modal.classList.remove(MODAL_CLASSES.hidden);
  document.body.classList.add(MODAL_CLASSES.lockScroll);
}

/**
 * Closes all elements with role="dialog" and restores page scroll.
 */
function closeAllModals(): void {
  document
    .querySelectorAll<HTMLElement>(MODAL_SELECTORS.dialogs)
    .forEach((modal) => {
      modal.classList.add(MODAL_CLASSES.hidden);
    });
  document.body.classList.remove(MODAL_CLASSES.lockScroll);
}

/**
 * Updates text content of a target element.
 */
function setText(id: string, value: string): void {
  const el = getById(id);
  if (!el) return;
  el.textContent = value;
}

/**
 * Safely updates href for anchor elements.
 */
function setHref(id: string, value: string): void {
  const el = getById(id);
  if (!(el instanceof HTMLAnchorElement)) return;
  el.href = value;
}

/**
 * Safely updates action attribute for form elements.
 */
function setAction(id: string, value: string): void {
  const el = getById(id);
  if (!(el instanceof HTMLFormElement)) return;
  el.action = value;
}

/**
 * Populates modal content (links, forms, text) based on the triggered action type.
 */
function fillModalDetails(
  type: ModalType,
  id: string,
  name: string,
  url: string,
): void {
  const details = name || id; // Fallback to ID if name is missing
  switch (type) {
    case "edit":
      setHref(MODAL_IDS.updateLink, url);
      setText(MODAL_IDS.updateDetails, details);
      break;
    case "delete":
      setAction(MODAL_IDS.deleteForm, url);
      setText(MODAL_IDS.deleteDetails, details);
      break;
    case "deactivate":
      setHref(MODAL_IDS.deactivateLink, url);
      setText(MODAL_IDS.deactivateDetails, details);
      break;
    case "activate":
      setHref(MODAL_IDS.activateLink, url);
      setText(MODAL_IDS.activateDetails, details);
      break;
    case "bulkDelete":
      break;
    case "confirmSave":
      setText(MODAL_IDS.confirmSaveObjectDetails, details);
      break;
  }
}

/**
 * Global Event Delegation:
 * Ensures the script runs only once and handles clicks for all modal triggers.
 */
if (!document.documentElement.hasAttribute(MODAL_INIT.attr)) {
  document.documentElement.setAttribute(MODAL_INIT.attr, "true");

  document.addEventListener("click", (event: Event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;

    // Handle Close/Cancel buttons
    const cancelBtn = target.closest<HTMLElement>(MODAL_SELECTORS.cancel);
    if (cancelBtn) {
      event.preventDefault();
      closeAllModals();
      return;
    }

    // Handle Modal Open triggers
    const triggerEl = target.closest<HTMLElement>(MODAL_SELECTORS.openTrigger);
    if (!triggerEl) return;

    const type = triggerEl.dataset.modalOpen;
    if (!isModalType(type)) return;
    event.preventDefault();

    const modalId = MODAL_TYPE_TO_ID[type];
    if (!modalId) return;

    // Extract data attributes for population
    const itemId = triggerEl.dataset.id ?? "";
    const itemName = triggerEl.dataset.name ?? "";

    // Use data-url attribute or fallback to anchor's href
    const targetUrl =
      triggerEl.dataset.url ??
      (triggerEl instanceof HTMLAnchorElement ? triggerEl.href : "");

    fillModalDetails(type, itemId, itemName, targetUrl);
    openModal(modalId);
  });

  /**
   * Accessibility: Close modals on Escape key press.
   */
  document.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key === MODAL_KEYS.escape) closeAllModals();
  });
}

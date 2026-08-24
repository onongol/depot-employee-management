/**
 * Checkbox validation logic (TypeScript, strict, modular).
 * Shows/removes error messages and red border on submit/change,
 * preventing form submission when no checkboxes are checked.
 */

import { readJsonScript } from "../utils/read_json";

const CHECKBOX_VALIDATION_SELECTORS = {
  groupCheckbox: 'input[type="checkbox"][data-row-checkbox-name]',
  selectAll: 'input[type="checkbox"][data-checkbox-name]',
} as const;

const CHECKBOX_VALIDATION_DATA = {
  validation: "data-checkbox-validation",
} as const;

const CHECKBOX_VALIDATION_CLASSES = {
  errorBorder: "border-red-500",
  errorBorderDark: "dark:border-red-500",
  errorText: "text-red-500",
  errorTextSize: "text-sm",
  errorTextCombined: "text-red-500 text-sm",
} as const;

const CHECKBOX_VALIDATION_ELEMENTS = {
  errorParagraph: "p",
} as const;

const CHECKBOX_VALIDATION_ATTRS = {
  errorRole: "role",
  errorRoleAlert: "alert",
} as const;

/** Selector used to identify existing error messages in the container */
const errorSelector = `.${CHECKBOX_VALIDATION_CLASSES.errorText}` as const;

/** Attribute selector for elements that opt-in for auto-initialization */
const validationSelector = `[${CHECKBOX_VALIDATION_DATA.validation}]` as const;

/**
 * Checks if the container still holds any validation error messages.
 * Prevents premature removal of the red border if other errors are present.
 */
function hasValidationErrors(container: ParentNode | null): boolean {
  if (!(container instanceof HTMLElement)) return false;
  return container.querySelector(errorSelector) !== null;
}

/** Generates CSS selector for checked row checkboxes in a specific group */
function getCheckedGroupSelector(groupName: string): string {
  return `${CHECKBOX_VALIDATION_SELECTORS.groupCheckbox}[data-row-checkbox-name="${groupName}"]:checked`;
}

/** Generates a unique ID for the error message element */
function getErrorId(groupName: string): string {
  return `${groupName}-selection-error`;
}

/**
 * Highlights the table/container and injects an error message into the DOM.
 */
function showSelectionError(
  tableDiv: HTMLElement | null,
  errorId: string,
  errorMessage: string,
): void {
  if (!tableDiv) return;

  // Apply error styling to the container
  tableDiv.classList.add(
    CHECKBOX_VALIDATION_CLASSES.errorBorder,
    CHECKBOX_VALIDATION_CLASSES.errorBorderDark,
  );

  let errorEl = document.getElementById(errorId);
  if (!errorEl) {
    errorEl = document.createElement(
      CHECKBOX_VALIDATION_ELEMENTS.errorParagraph,
    );
    errorEl.id = errorId;
    errorEl.className = CHECKBOX_VALIDATION_CLASSES.errorTextCombined;
    errorEl.textContent = errorMessage;

    // A11y: Ensure screen readers announce the error immediately
    errorEl.setAttribute(
      CHECKBOX_VALIDATION_ATTRS.errorRole,
      CHECKBOX_VALIDATION_ATTRS.errorRoleAlert,
    );

    tableDiv.after(errorEl);
  }
}

/**
 * Removes the specific error message and clears container highlighting
 * only if no other validation errors remain in the parent scope.
 */
function hideSelectionError(
  tableDiv: HTMLElement | null,
  errorId: string,
): void {
  if (!tableDiv) return;

  const errorEl = document.getElementById(errorId);
  if (errorEl) errorEl.remove();

  const parent = tableDiv.parentNode;
  if (!hasValidationErrors(parent)) {
    tableDiv.classList.remove(
      CHECKBOX_VALIDATION_CLASSES.errorBorder,
      CHECKBOX_VALIDATION_CLASSES.errorBorderDark,
    );
  }
}

/** Queries the form for checked checkboxes belonging to the specified group */
function resolveCheckedCheckboxes(
  form: HTMLFormElement,
  groupName: string,
): HTMLInputElement[] {
  return Array.from(
    form.querySelectorAll<HTMLInputElement>(getCheckedGroupSelector(groupName)),
  );
}

/**
 * Core setup function. Binds submit and change listeners to the form.
 */
export function setupCheckboxValidation(
  formId: string,
  groupName: string,
  tableSelector: string,
  errorMessage: string,
): void {
  const form = document.getElementById(formId);
  if (!(form instanceof HTMLFormElement)) return;

  // Resolve table/container either within the form or globally
  const tableDiv =
    form.querySelector(tableSelector) ?? document.querySelector(tableSelector);
  if (!(tableDiv instanceof HTMLElement)) return;

  const errorId = getErrorId(groupName);

  // Block submission if selection is empty
  form.addEventListener("submit", (event: Event) => {
    const checked = resolveCheckedCheckboxes(form, groupName);
    if (checked.length === 0) {
      event.preventDefault();
      showSelectionError(tableDiv, errorId, errorMessage);
    } else {
      hideSelectionError(tableDiv, errorId);
    }
  });

  // Real-time error clearing when user interacts with checkboxes
  form.addEventListener("change", (event: Event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) return;

    // Check if the interacted element belongs to the current validation group
    if (
      target.dataset.rowCheckboxName === groupName ||
      target.dataset.checkboxName === groupName
    ) {
      const checked = resolveCheckedCheckboxes(form, groupName);
      if (checked.length > 0) hideSelectionError(tableDiv, errorId);
    }
  });
}

/**
 * Global initialization. Finds all elements with the validation data-attribute
 * and sets up their respective form listeners.
 */
document.addEventListener("DOMContentLoaded", () => {
  const validationEls =
    document.querySelectorAll<HTMLElement>(validationSelector);
  for (const el of validationEls) {
    const formId = el.dataset.formId;
    const groupName = el.dataset.checkboxName;
    const tableSelector = el.dataset.tableSelector;
    const errorMsgId = el.dataset.errorMessageId ?? "";
    const errorMessage = readJsonScript(errorMsgId);
    if (formId && groupName && tableSelector && errorMessage) {
      setupCheckboxValidation(formId, groupName, tableSelector, errorMessage);
    }
  }
});

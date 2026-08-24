/**
 * Amount Validation Logic (TypeScript, strict, modular).
 * Specifically designed for piecework items where each selected (checked) row
 * must have a valid positive numeric amount before the form can be submitted.
 */

import { readJsonScript } from "../utils/read_json";

type Nullable<T> = T | null;

const AMOUNT_VALIDATION_SELECTORS = {
  amountInput: "input[data-amount-input]",
} as const;

const AMOUNT_VALIDATION_DATA = {
  validation: "data-amount-validation",
  amountInputAttr: "data-amount-input",
} as const;

const AMOUNT_VALIDATION_CLASSES = {
  errorBorder: "border-red-500",
  errorBorderDark: "dark:border-red-500",
  errorBorderFocus: "focus:border-red-500",
  errorRingFocus: "focus:ring-red-500",
  errorBorderFocusDark: "dark:focus:border-red-500",
  errorRingFocusDark: "dark:focus:ring-red-500",
  errorText: "text-red-500",
  errorTextSize: "text-sm",
  errorTextCombined: "text-red-500 text-sm mb-2",
} as const;

const AMOUNT_VALIDATION_ELEMENTS = {
  errorParagraph: "p",
} as const;

const AMOUNT_VALIDATION_ATTRS = {
  errorRole: "role",
  errorRoleAlert: "alert",
} as const;

const AMOUNT_ERROR_ID = "amount-error" as const;

/** Attribute selector for auto-initialization */
const validationSelector = `[${AMOUNT_VALIDATION_DATA.validation}]` as const;

/** Class selector to identify existing error text elements */
const errorSelector = `.${AMOUNT_VALIDATION_CLASSES.errorText}` as const;

/** Helper: Returns selector for checked checkboxes in a specific group */
function getCheckedCheckboxSelector(name: string): string {
  return `input[data-row-checkbox-name="${name}"]:checked`;
}

/** Helper: Returns selector for an amount input linked to a specific row value */
function getAmountSelector(value: string): string {
  return `${AMOUNT_VALIDATION_SELECTORS.amountInput}[data-amount-for="${value}"]`;
}

/** Helper: Returns selector for a checkbox that is currently checked for a specific value */
function getCheckedRowSelector(checkboxName: string, value: string): string {
  return `input[data-row-checkbox-name="${checkboxName}"][value="${value}"]:checked`;
}

/**
 * Checks if the container's parent has any existing validation error messages.
 * This prevents the removal of shared borders if other validation scripts still have errors.
 */
function hasValidationErrors(container: Nullable<HTMLElement>): boolean {
  if (!container) return false;
  const parent = container.parentNode;
  return (
    parent instanceof HTMLElement &&
    parent.querySelector(errorSelector) !== null
  );
}

/** Applies red error styling to a specific input field */
function addRedBorder(input: Nullable<HTMLInputElement>): void {
  if (!input) return;
  input.classList.add(
    AMOUNT_VALIDATION_CLASSES.errorBorder,
    AMOUNT_VALIDATION_CLASSES.errorBorderFocus,
    AMOUNT_VALIDATION_CLASSES.errorRingFocus,
    AMOUNT_VALIDATION_CLASSES.errorBorderDark,
    AMOUNT_VALIDATION_CLASSES.errorBorderFocusDark,
    AMOUNT_VALIDATION_CLASSES.errorRingFocusDark,
  );
}

/** Removes red error styling from a specific input field */
function removeRedBorder(input: Nullable<HTMLInputElement>): void {
  if (!input) return;
  input.classList.remove(
    AMOUNT_VALIDATION_CLASSES.errorBorder,
    AMOUNT_VALIDATION_CLASSES.errorBorderFocus,
    AMOUNT_VALIDATION_CLASSES.errorRingFocus,
    AMOUNT_VALIDATION_CLASSES.errorBorderDark,
    AMOUNT_VALIDATION_CLASSES.errorBorderFocusDark,
    AMOUNT_VALIDATION_CLASSES.errorRingFocusDark,
  );
}

/**
 * Displays a global amount error errorAmountMessage and highlights the table container.
 * It removes any existing error before injecting the new one.
 */
function showAmountError(
  errorAmountMessage: string,
  tableSelector: Nullable<HTMLElement>,
): void {
  if (!tableSelector) return;
  const errorId = AMOUNT_ERROR_ID;
  const existing = document.getElementById(errorId);
  if (existing) existing.remove();

  const errorEl = document.createElement(
    AMOUNT_VALIDATION_ELEMENTS.errorParagraph,
  );
  errorEl.id = errorId;
  errorEl.className = AMOUNT_VALIDATION_CLASSES.errorTextCombined;
  errorEl.textContent = errorAmountMessage;
  errorEl.setAttribute(
    AMOUNT_VALIDATION_ATTRS.errorRole,
    AMOUNT_VALIDATION_ATTRS.errorRoleAlert,
  );

  tableSelector.after(errorEl);
  tableSelector.classList.add(
    AMOUNT_VALIDATION_CLASSES.errorBorder,
    AMOUNT_VALIDATION_CLASSES.errorBorderDark,
  );
}

/** Clears the global amount error and removes the highlight from the container */
function clearAmountError(tableSelector: Nullable<HTMLElement>): void {
  if (!tableSelector) return;
  const errorId = AMOUNT_ERROR_ID;
  const err = document.getElementById(errorId);
  if (err) err.remove();

  // Clean up container borders only if no other errors exist in this scope
  if (!hasValidationErrors(tableSelector)) {
    tableSelector.classList.remove(
      AMOUNT_VALIDATION_CLASSES.errorBorder,
      AMOUNT_VALIDATION_CLASSES.errorBorderDark,
    );
  }
}

/** Checks if a string represents a valid finite number greater than zero. */
function isPositiveNumberString(valueInput: string): boolean {
  if (valueInput.trim() === "") return false;
  const numInput = Number(valueInput);
  return Number.isFinite(numInput) && numInput > 0;
}

/**
 * Validates the amounts for all selected rows.
 * Used during form submission to prevent sending invalid data.
 */
function validateSelectedWorkAmounts(
  checkboxName: string,
  tableSelector: string,
  errorAmountMessage: string,
): boolean {
  const container = document.querySelector(
    tableSelector,
  ) as Nullable<HTMLElement>;
  const amountInputs = document.querySelectorAll<HTMLInputElement>(
    AMOUNT_VALIDATION_SELECTORS.amountInput,
  );

  // Clear all individual field highlights before re-checking
  for (const input of amountInputs) {
    removeRedBorder(input);
  }

  const selected = Array.from(
    document.querySelectorAll<HTMLInputElement>(
      getCheckedCheckboxSelector(checkboxName),
    ),
  );

  // If no rows are selected, validation implicitly passes
  if (selected.length === 0) {
    clearAmountError(container);
    return true;
  }

  let invalid = false;
  for (const checkbox of selected) {
    const input = document.querySelector<HTMLInputElement>(
      getAmountSelector(checkbox.value),
    );
    const val = input ? String(input.value).trim() : "";

    // Highlight individual field if it belongs to a checked row but has invalid value
    if (!input || !isPositiveNumberString(val)) {
      invalid = true;
      addRedBorder(input);
    }
  }

  if (invalid) {
    // Scroll to the table to ensure the user sees the error notification
    if (container)
      container.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    showAmountError(errorAmountMessage, container);
    return false;
  }

  clearAmountError(container);
  return true;
}

/**
 * Main setup function to initialize event listeners for a specific form and row group.
 */
export function setupAmountValidation(
  formId: string,
  checkboxName: string,
  tableSelector: string,
  errorAmountMessage: string,
): void {
  const maybeForm = document.getElementById(formId);
  if (!(maybeForm instanceof HTMLFormElement)) return;
  const form: HTMLFormElement = maybeForm;

  /** Internal check to see if all checked rows have valid inputs */
  function allSelectedAmountsValid(): boolean {
    const selected = Array.from(
      document.querySelectorAll<HTMLInputElement>(
        getCheckedCheckboxSelector(checkboxName),
      ),
    );
    if (selected.length === 0) return true;
    for (const checkbox of selected) {
      const input = document.querySelector<HTMLInputElement>(
        getAmountSelector(checkbox.value),
      );
      const val = input ? String(input.value).trim() : "";
      if (!input || !isPositiveNumberString(val)) return false;
    }
    return true;
  }

  /**
   * Binds listeners that clear errors as the user types or toggles checkboxes.
   */
  function attachLiveClearHandlers(): void {
    form.addEventListener("input", (event: Event) => {
      const target = event.target;
      if (!(target instanceof HTMLInputElement)) return;
      if (!target.hasAttribute(AMOUNT_VALIDATION_DATA.amountInputAttr)) return;

      removeRedBorder(target);
      const container = document.querySelector(
        tableSelector,
      ) as Nullable<HTMLElement>;

      // Optimization: Only check logic if the input belongs to a checked row
      const amountFor = target.dataset.amountFor ?? "";
      const checkbox = document.querySelector<HTMLInputElement>(
        getCheckedRowSelector(checkboxName, amountFor),
      );

      if (!checkbox) return;

      const val = target.value.trim();
      if (isPositiveNumberString(val)) {
        // If the current input is fixed, check if we can remove the global error
        if (allSelectedAmountsValid()) clearAmountError(container);
      }
    });

    form.addEventListener("change", (event: Event) => {
      const target = event.target;
      if (!(target instanceof HTMLInputElement)) return;

      // If a checkbox is unchecked, we remove its individual error highlight
      if (target.name === checkboxName) {
        const container = document.querySelector(
          tableSelector,
        ) as Nullable<HTMLElement>;
        if (!target.checked) {
          const input = document.querySelector<HTMLInputElement>(
            getAmountSelector(target.value),
          );
          removeRedBorder(input);
        }
        // Recalculate global error state on checkbox changes
        if (allSelectedAmountsValid()) clearAmountError(container);
      }
    });
  }

  attachLiveClearHandlers();

  // Final validation barrier on form submission
  form.addEventListener("submit", (event: Event) => {
    if (
      !validateSelectedWorkAmounts(
        checkboxName,
        tableSelector,
        errorAmountMessage,
      )
    ) {
      event.preventDefault();
    }
  });
}

/**
 * Initialization logic on page load.
 * Discovers containers with the 'data-amount-validation' attribute and attaches logic.
 */
document.addEventListener("DOMContentLoaded", () => {
  const containerEls =
    document.querySelectorAll<HTMLElement>(validationSelector);
  for (const el of containerEls) {
    const formId = el.dataset.formId;
    const checkboxName = el.dataset.checkboxName;
    const tableSelector = el.dataset.tableSelector;
    const amountErrorMessageId = el.dataset.amountErrorMessageId ?? "";
    const errorAmountMessage = readJsonScript(amountErrorMessageId);
    if (!formId || !checkboxName || !tableSelector) continue;
    setupAmountValidation(
      formId,
      checkboxName,
      tableSelector,
      errorAmountMessage,
    );
  }
});

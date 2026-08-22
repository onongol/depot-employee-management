/**
 * Amount Input Sync Logic (TypeScript, strict, modular).
 * Synchronizes the state of amount inputs with their corresponding checkboxes.
 * Supports multiple independent groups on a single page using data-attributes.
 */

type Nullable<T> = T | null;

const AMOUNT_INPUT_SELECTORS = {
  amountInput: "input[data-amount-input]",
  workCheckbox: "input[data-row-checkbox-name]",
  selectAllWorks: "input[data-checkbox-name]",
  syncGroupContainer: "[data-amount-sync-group]",
} as const;

const AMOUNT_INPUT_KEYS = {
  enter: "Enter",
} as const;

/** Helper: Returns a selector for checkboxes belonging to a specific row group */
function getWorkCheckboxSelector(groupName: string): string {
  return `input[data-row-checkbox-name="${groupName}"]`;
}

/** Finds an amount input associated with a specific checkbox value */
function getAmountInputByValue(value: string): Nullable<HTMLInputElement> {
  return document.querySelector<HTMLInputElement>(
    `${AMOUNT_INPUT_SELECTORS.amountInput}[data-amount-for="${value}"]`,
  );
}

/**
 * Focuses the corresponding amount input for a checkbox, if enabled.
 */
function focusAmountInput(checkbox: Nullable<HTMLInputElement>): void {
  if (!checkbox) return;

  const amountInput = getAmountInputByValue(checkbox.value);
  if (amountInput && !amountInput.disabled) amountInput.focus();
}

/**
 * Syncs the state of an individual amount input.
 * Disables and clears the input if the checkbox is unchecked.
 */
function updateAmountInput(checkbox: Nullable<HTMLInputElement>): void {
  if (!checkbox) return;
  const amountInput = getAmountInputByValue(checkbox.value);
  if (!amountInput) return;

  amountInput.disabled = !checkbox.checked;

  // Clear value to ensure no "ghost data" is submitted if the row is deselected
  if (!checkbox.checked) amountInput.value = "";
}

/** Performs an initial synchronization for all checkboxes in a group */
function updateAllWorkCheckboxes(groupName: string): void {
  const checkboxes = document.querySelectorAll<HTMLInputElement>(
    getWorkCheckboxSelector(groupName),
  );
  for (const checkbox of checkboxes) {
    updateAmountInput(checkbox);
  }
}

/**
 * Prevents Enter key submit for amount inputs within a specific container only (delegated).
 */
function preventEnterSubmit(container: HTMLElement): void {
  container.addEventListener("keydown", (event: KeyboardEvent) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) return;
    if (!target.matches(AMOUNT_INPUT_SELECTORS.amountInput)) return;
    if (event.key === AMOUNT_INPUT_KEYS.enter) event.preventDefault();
  });
}

/**
 * Delegated handler for both row and select-all checkboxes on the container.
 */
function attachDelegatedHandlers(
  groupName: string,
  container: HTMLElement,
): void {
  container.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement)) return;

    // Row checkbox changed
    if (target.dataset.rowCheckboxName === groupName) {
      updateAmountInput(target);
      if (target.checked) focusAmountInput(target);
      return;
    }

    // Select-all checkbox changed
    if (target.dataset.checkboxName === groupName) {
      for (const checkbox of document.querySelectorAll<HTMLInputElement>(
        getWorkCheckboxSelector(groupName),
      )) {
        if (checkbox.offsetParent !== null) updateAmountInput(checkbox);
      }
    }
  });
}

/**
 * Main Entry Point: Discovers all sync containers and initializes their logic.
 */
document.addEventListener("DOMContentLoaded", () => {
  for (const container of document.querySelectorAll<HTMLElement>(
    AMOUNT_INPUT_SELECTORS.syncGroupContainer,
  )) {
    const groupName = container.dataset.amountSyncGroup;
    if (!groupName) continue;

    updateAllWorkCheckboxes(groupName);
    attachDelegatedHandlers(groupName, container);
    preventEnterSubmit(container);
  }
});

/**
 * Select-all logic (TypeScript, strict).
 * Manages master-slave checkbox relationships with indeterminate state support.
 * Integrates with table filtering by only affecting visible rows.
 */

/** Extended interface to safely track state without 'any' */
interface MasterCheckbox extends HTMLInputElement {
  _preClickIndeterminate?: boolean;
}
const SELECT_ALL_TYPES = {
  checkboxType: "checkbox",
} as const;

const SELECT_ALL_SELECTORS = {
  selectAll: 'input[type="checkbox"][data-checkbox-name]',
  groupCheckbox: 'input[type="checkbox"][data-row-checkbox-name]',
} as const;

/** Helper to find row checkboxes by group name */
function getGroupCheckboxSelector(name: string): string {
  return `${SELECT_ALL_SELECTORS.groupCheckbox}[data-row-checkbox-name="${name}"]`;
}

/** Finds the master checkbox by its group name */
function getSelectAllCheckboxSelector(name: string): string {
  return `${SELECT_ALL_SELECTORS.selectAll}[data-checkbox-name="${name}"]`;
}

/** Resolves all row checkboxes into an array */
function resolveCheckboxesByData(name: string): HTMLInputElement[] {
  return Array.from(
    document.querySelectorAll<HTMLInputElement>(getGroupCheckboxSelector(name)),
  );
}

/**
 * Toggles visible row checkboxes.
 * Implements "Click-to-Reset" logic for indeterminate state.
 */
export function toggleAllVisible(source: MasterCheckbox, name: string): void {
  const checkboxList = resolveCheckboxesByData(name);
  if (checkboxList.length === 0) return;

  // Logic: If the master checkbox was in 'indeterminate' (minus) state before the click,
  // we force a reset (uncheck everything) instead of checking the remaining items.
  const wasIndeterminate = source._preClickIndeterminate ?? false;
  const shouldCheck = wasIndeterminate ? false : source.checked;

  if (wasIndeterminate) {
    source.checked = false;
    source.indeterminate = false;
  }

  for (const checkbox of checkboxList) {
    // Only toggle checkboxes that are currently visible (respects active table filters)
    if (checkbox.offsetParent !== null) {
      if (checkbox.checked !== shouldCheck) {
        checkbox.checked = shouldCheck;
        checkbox.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }
  }
}

/** Updates master checkbox visual state */
function refreshAllCheckbox(selectAll: HTMLInputElement): void {
  const name = selectAll.dataset.checkboxName;
  if (!name) return;

  const visible = resolveCheckboxesByData(name).filter(
    (cb) => cb.offsetParent !== null,
  );

  // If there are no visible checkboxes, reset master checkbox to unchecked and not indeterminate
  if (visible.length === 0) {
    selectAll.checked = false;
    selectAll.indeterminate = false;
    return;
  }

  const checked = visible.filter((cb) => cb.checked);

  if (checked.length === 0) {
    selectAll.checked = false;
    selectAll.indeterminate = false;
  } else if (checked.length === visible.length) {
    selectAll.checked = true;
    selectAll.indeterminate = false;
  } else {
    selectAll.checked = false;
    selectAll.indeterminate = true;
  }
}

/**
 * Orchestrates initialization and event delegation.
 */
function initSelectAll(): void {
  /**
   * 1. Capture the indeterminate state BEFORE the 'change' event fires.
   * Browser native behavior switches indeterminate to checked on click,
   * so we must store the previous state during pointerdown.
   */
  document.addEventListener("pointerdown", (event) => {
    const target = event.target as MasterCheckbox;
    if (target?.dataset?.checkboxName) {
      target._preClickIndeterminate = target.indeterminate;
    }
  });

  /** 2. Initial synchronization of all master checkboxes on page load */
  for (const cb of document.querySelectorAll<HTMLInputElement>(
    SELECT_ALL_SELECTORS.selectAll,
  )) {
    refreshAllCheckbox(cb);
  }

  /** 3. Event delegation for all checkbox interactions */
  document.addEventListener("change", (event) => {
    const target = event.target as HTMLInputElement | null;
    if (!target || target.type !== SELECT_ALL_TYPES.checkboxType) return;

    // Case: Master checkbox interaction
    const groupName = target.dataset.checkboxName;
    if (groupName) {
      toggleAllVisible(target as MasterCheckbox, groupName);
      refreshAllCheckbox(target);
      return;
    }

    // Case: Individual row checkbox interaction
    const rowGroupName = target.dataset.rowCheckboxName;
    if (rowGroupName) {
      const selectAll = document.querySelector<HTMLInputElement>(
        getSelectAllCheckboxSelector(rowGroupName),
      );
      if (selectAll) refreshAllCheckbox(selectAll);
    }
  });
}

/**
 * Initialize on DOMContentLoaded or immediately if already loaded
 */
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSelectAll);
} else {
  initSelectAll();
}

/**
 * HTMX Integration.
 * Re-evaluates master checkbox states after a table body is swapped/updated via AJAX.
 */
document.addEventListener("htmx:afterSwap", () => {
  for (const cb of document.querySelectorAll<HTMLInputElement>(
    SELECT_ALL_SELECTORS.selectAll,
  )) {
    refreshAllCheckbox(cb);
  }
});

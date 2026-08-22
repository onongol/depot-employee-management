/**
 * Work Date Filter:
 * Synchronizes the date input with URL search parameters.
 * Resets pagination when the date is updated to ensure the user starts from page 1.
 */
const WORK_DATE_IDS = {
  input: "work_date",
} as const;

const WORK_DATE_PARAMS = {
  workDate: "work_date",
  page: "page",
} as const;

const WORK_DATE_KEYS = {
  enter: "Enter",
} as const;

document.addEventListener("DOMContentLoaded", () => {
  // Acquire the input element and ensure it is the correct HTML type
  const inputEl = document.getElementById(WORK_DATE_IDS.input);
  if (!(inputEl instanceof HTMLInputElement)) return;
  const input = inputEl;

  /**
   * Updates the browser URL with the selected date value.
   * Clears the 'page' parameter to prevent out-of-bounds pagination.
   */
  const applyWorkDate = (value: string): void => {
    const val = value.trim();

    try {
      // Use the URL API for safe search parameter manipulation
      const url = new URL(window.location.href);
      const params = url.searchParams;

      // If value exists, set the param; otherwise, remove it for a cleaner URL
      if (val) params.set(WORK_DATE_PARAMS.workDate, val);
      else params.delete(WORK_DATE_PARAMS.workDate);

      // Always reset pagination when filtering by a new date
      params.delete(WORK_DATE_PARAMS.page);

      url.search = params.toString();

      // Trigger full page reload with the new filter state
      window.location.href = url.toString();
    } catch {
      // Silently fail if URL is malformed or navigation is blocked
    }
  };

  /**
   * Listen for 'change' events (triggered when date is selected via picker).
   */
  input.addEventListener("change", () => {
    applyWorkDate(input.value);
  });

  /**
   * Listen for 'Enter' key to support manual date typing.
   */
  input.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key !== WORK_DATE_KEYS.enter) return;
    e.preventDefault();
    applyWorkDate(input.value);
  });
});

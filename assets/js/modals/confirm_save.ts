const SAVE_CONFIRM_SELECTORS = {
  confirmSaveButton: "[data-confirm-save]",
} as const;

const SAVE_CONFIRM_IDS = {
  updateForm: "updateForm",
} as const;

/**
 * Handles the final form submission from within the confirmation modal.
 * Uses requestSubmit() to ensure HTML5 validation is triggered.
 */
document.addEventListener("click", (event: Event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;

  // Search for the confirmation button using the data-attribute
  const confirmBtn = target.closest(SAVE_CONFIRM_SELECTORS.confirmSaveButton);
  if (!confirmBtn) return;

  event.preventDefault();

  const mainForm = document.getElementById(
    SAVE_CONFIRM_IDS.updateForm,
  ) as HTMLFormElement | null;

  if (mainForm) {
    // requestSubmit() triggers validation and 'submit' event listeners,
    // while submit() bypasses them.
    if (typeof mainForm.requestSubmit === "function") {
      mainForm.requestSubmit();
    } else {
      mainForm.submit();
    }
  }
});

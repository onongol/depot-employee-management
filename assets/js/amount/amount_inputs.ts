declare global {
  interface Window {
    toggleAllVisible?: (
      source: HTMLInputElement | { checked?: boolean } | null,
      name?: string | Iterable<HTMLInputElement> | null | undefined
    ) => void;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const getAmountInput = (checkboxValue: string | null): HTMLInputElement | null => {
    if (!checkboxValue) return null;
    const el = document.getElementById('amount_' + checkboxValue);
    return el instanceof HTMLInputElement ? el : null;
  };

  function updateAmountInput(checkbox: HTMLInputElement | null): void {
    if (!checkbox) return;
    const amountInput = getAmountInput(checkbox.value);
    if (!amountInput) return;
    amountInput.disabled = !checkbox.checked;
    if (!checkbox.checked) amountInput.value = '';
  }

  function updateAllWorkCheckboxes(): void {
    document.querySelectorAll<HTMLInputElement>('.work-checkbox').forEach((checkbox) => {
      updateAmountInput(checkbox);
    });
  }

  // Initialize
  updateAllWorkCheckboxes();

  // Individual checkbox handlers
  document.querySelectorAll<HTMLInputElement>('.work-checkbox').forEach((checkbox) => {
    checkbox.addEventListener('change', () => updateAmountInput(checkbox));
  });

  // "Select all works" checkbox behavior
  const selectAllWorks = document.getElementById('select-all-works') as HTMLInputElement | null;
  if (selectAllWorks) {
    selectAllWorks.addEventListener('change', () => {
      // call global helper (kept for backward compatibility)
      window.toggleAllVisible?.(selectAllWorks, 'work_ids');
      // update only visible checkboxes' amount inputs
      document.querySelectorAll<HTMLInputElement>('.work-checkbox').forEach((checkbox) => {
        if (checkbox.offsetParent !== null) updateAmountInput(checkbox);
      });
    });
  }

  // Prevent Enter from submitting when focused in amount inputs
  document.querySelectorAll<HTMLInputElement>('.amount-input').forEach((input) => {
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter' || (event as any).keyCode === 13) {
        event.preventDefault();
      }
    });
  });
});
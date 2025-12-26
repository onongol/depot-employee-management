// Validates amount inputs for selected piecework items before form submission:
// - highlights invalid inputs, shows/clears error messages,
// - prevents submission when selected works have missing/invalid amounts,
// - exposes initializer `setupAmountValidation` on window for compatibility.

type Nullable<T> = T | null;

function addRedBorder(input: Nullable<HTMLInputElement>): void {
  if (!input) return;
  input.classList.add(
    'border-red-500', 'focus:border-red-500', 'focus:ring-red-500',
    'dark:border-red-500', 'dark:focus:border-red-500', 'dark:focus:ring-red-500'
  );
}

function removeRedBorder(input: Nullable<HTMLInputElement>): void {
  if (!input) return;
  input.classList.remove(
    'border-red-500', 'focus:border-red-500', 'focus:ring-red-500',
    'dark:border-red-500', 'dark:focus:border-red-500', 'dark:focus:ring-red-500'
  );
}

function showAmountError(message: string, container: Nullable<Element>): void {
  if (!container) return;
  const existing = document.getElementById('amount-error');
  if (existing) existing.remove();

  const errorDiv = document.createElement('div');
  errorDiv.id = 'amount-error';
  errorDiv.className = 'text-red-500 text-sm mb-2';
  errorDiv.textContent = message;

  const parent = container.parentNode;
  if (parent) parent.insertBefore(errorDiv, container.nextSibling);
  (container as HTMLElement).classList.add('border-red-500', 'dark:border-red-500');
}

function clearAmountError(container: Nullable<Element>): void {
  if (!container) return;
  const err = document.getElementById('amount-error');
  if (err) err.remove();
  // keep other errors like checkbox selection error if present
  if (!document.getElementById('work_ids-selection-error')) {
    (container as HTMLElement).classList.remove('border-red-500', 'dark:border-red-500');
  }
}

function isPositiveNumberString(v: string): boolean {
  if (v.trim() === '') return false;
  const n = Number(v);
  return Number.isFinite(n) && n > 0;
}

function validateSelectedWorkAmounts(checkboxName: string, containerSelector: string, message: string): boolean {
  const container = document.querySelector(containerSelector);
  // Reset previous invalid state
  document.querySelectorAll<HTMLInputElement>('input[id^="amount_"]').forEach(removeRedBorder);

  const selected = Array.from(document.querySelectorAll<HTMLInputElement>(`input[name="${checkboxName}"]:checked`));
  if (selected.length === 0) {
    clearAmountError(container);
    return true;
  }

  let invalid = false;
  for (const cb of selected) {
    const input = document.getElementById(`amount_${cb.value}`) as HTMLInputElement | null;
    const val = input ? String(input.value).trim() : '';
    if (!input || !isPositiveNumberString(val)) {
      invalid = true;
      addRedBorder(input);
    }
  }

  if (invalid) {
    if (container) (container as HTMLElement).scrollIntoView({ behavior: 'smooth', block: 'start' });
    showAmountError(message, container);
    return false;
  }

  clearAmountError(container);
  return true;
}

/**
 * Public initializer
 * formId: id of the form element
 * checkboxName: name attribute of work checkboxes (e.g. "work_ids")
 * containerSelector: selector to the container used for showing errors (e.g. '.work-table-container')
 * message: translated message to show
 */
export function setupAmountValidation(formId: string, checkboxName: string, containerSelector: string, message: string): void {
  const form = document.getElementById(formId) as HTMLFormElement | null;
  if (!form) return;

  function allSelectedAmountsValid(): boolean {
    const selected = Array.from(document.querySelectorAll<HTMLInputElement>(`input[name="${checkboxName}"]:checked`));
    if (selected.length === 0) return true;
    for (const cb of selected) {
      const input = document.getElementById(`amount_${cb.value}`) as HTMLInputElement | null;
      const val = input ? String(input.value).trim() : '';
      if (!input || !isPositiveNumberString(val)) return false;
    }
    return true;
  }

  function attachLiveClearHandlers(): void {
    document.querySelectorAll<HTMLInputElement>('input[id^="amount_"]').forEach(input => {
      input.addEventListener('input', () => {
        removeRedBorder(input);
        const container = document.querySelector(containerSelector);
        if (allSelectedAmountsValid()) clearAmountError(container);
      });
    });

    document.querySelectorAll<HTMLInputElement>(`input[name="${checkboxName}"]`).forEach(cb => {
      cb.addEventListener('change', () => {
        const container = document.querySelector(containerSelector);
        if (!cb.checked) {
          const input = document.getElementById(`amount_${cb.value}`) as HTMLInputElement | null;
          removeRedBorder(input);
        }
        if (allSelectedAmountsValid()) clearAmountError(container);
      });
    });
  }

  attachLiveClearHandlers();

  form.addEventListener('submit', (e: Event) => {
    if (!validateSelectedWorkAmounts(checkboxName, containerSelector, message)) {
      e.preventDefault();
    }
  });
}

/* expose for legacy templates that call window.setupAmountValidation */
declare global {
  interface Window {
    setupAmountValidation?: (formId: string, checkboxName: string, containerSelector: string, message: string) => void;
  }
}
if (typeof window !== 'undefined') {
  window.setupAmountValidation = setupAmountValidation;
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll<HTMLElement>('[data-amount-validation="true"]').forEach(el => {
    const formId = el.getAttribute('data-form-id') || 'createForm';
    const checkboxName = el.getAttribute('data-checkbox-name') || 'work_ids';
    const containerSelector = el.getAttribute('data-container-selector') || '.works-table-container';
    const message = el.getAttribute('data-amount-error-message') || '';
    setupAmountValidation(formId, checkboxName, containerSelector, message);
  });
});
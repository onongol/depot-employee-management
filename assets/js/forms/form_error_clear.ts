/**
 * Remove validation UI (red borders + error node with id "<fieldId>_error")
 * when user edits inputs/selects/textareas.
 */

type FormElement = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;

const RED_BORDER_CLASSES = [
  'border-red-600', 'focus:ring-red-600', 'focus:border-red-600', 'focus:text-red-600',
  'dark:border-red-600', 'dark:focus:ring-red-600', 'dark:focus:border-red-600', 'dark:focus:text-red-600'
];

function clearValidationUi(el: FormElement): void {
  el.classList.remove(...RED_BORDER_CLASSES);

  // try id-based error id (e.g. id="amount_1" -> "amount_1_error")
  const id = el.id?.trim();
  if (id) {
    const errorDiv = document.getElementById(`${id}_error`);
    if (errorDiv) {
      errorDiv.remove();
      return;
    }
  }

  // fallback: try name-based error id (e.g. name="amount" -> "amount_error")
  const name = (el as HTMLInputElement).name?.trim();
  if (name) {
    const nameErr = document.getElementById(`${name}_error`);
    if (nameErr) nameErr.remove();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const nodeList = document.querySelectorAll<FormElement>('input, select, textarea');
  nodeList.forEach((el) => {
    el.addEventListener('input', () => clearValidationUi(el));
  });
});
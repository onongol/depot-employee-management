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
  const id = el.id?.trim();
  if (!id) return;
  const errorDiv = document.getElementById(`${id}_error`);
  if (errorDiv) errorDiv.remove();
}

document.addEventListener('DOMContentLoaded', () => {
  const nodeList = document.querySelectorAll<FormElement>('input, select, textarea');
  nodeList.forEach((el) => {
    el.addEventListener('input', () => clearValidationUi(el));
  });
});
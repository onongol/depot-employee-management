/**
 * Compact, type-safe rewrite of summary_selected_works.js
 * - strict types, no `any`
 * - safe DOM queries and null checks
 * - exports and attaches helper for legacy usage
 */

declare function gettext(s: string): string;

type Nullable<T> = T | null;

function getEl<T extends Element = Element>(id: string): Nullable<T> {
  return document.getElementById(id) as Nullable<T>;
}

function getWorkNameFromCheckbox(cb: HTMLInputElement | null): string {
  if (!cb) return '';
  const row = cb.closest('tr');
  if (!row) return '';
  const workNameCell = row.querySelector<HTMLTableCellElement>('td:nth-child(2)');
  if (!workNameCell) return '';
  // Prefer direct text nodes (avoid nested tags)
  const txt = Array.from(workNameCell.childNodes)
    .filter((n): n is ChildNode => n.nodeType === Node.TEXT_NODE)
    .map(n => n.textContent?.trim() ?? '')
    .find(Boolean);
  return txt ?? (workNameCell.textContent?.trim() ?? '');
}

export function toggleWorksFullSummary(workNames: string[]): void {
  const existing = getEl<HTMLElement>('works-full-summary');
  if (existing) {
    existing.remove();
    return;
  }
  const worksListDiv = getEl<HTMLElement>('selected-works-list');
  if (!worksListDiv || !worksListDiv.parentNode) return;
  const fullSummary = document.createElement('div');
  fullSummary.id = 'works-full-summary';
  fullSummary.className = 'mt-2 p-2 text-sm';
  fullSummary.textContent = workNames.join(', ');
  worksListDiv.parentNode.insertBefore(fullSummary, worksListDiv.nextSibling);
}

export function updateSelectedWorksSummary(): void {
  const workCheckboxes = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="work_ids"]'));
  const workChecked = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="work_ids"]:checked'));
  const selectAllWork = getEl<HTMLInputElement>('select-all-works');
  const worksListDiv = getEl<HTMLElement>('selected-works-list');
  const summaryBox = getEl<HTMLElement>('selected-summary');
  if (!worksListDiv || !summaryBox) return;

  let workSummary = gettext('No works selected');

  const workNames = workChecked
    .map(cb => (cb.dataset?.workName?.trim() ? cb.dataset.workName.trim() : getWorkNameFromCheckbox(cb)))
    .filter(Boolean);

  if (selectAllWork && selectAllWork.checked && workChecked.length === workCheckboxes.length && workChecked.length > 0) {
    workSummary = gettext('Selected all');
    worksListDiv.textContent = workSummary;
    const full = getEl<HTMLElement>('works-full-summary');
    if (full) full.remove();
  } else if (workNames.length > 0) {
    const head = workNames.slice(0, 5).join(', ');
    worksListDiv.textContent = head;
    const full = getEl<HTMLElement>('works-full-summary');
    if (full) full.remove();

    if (workNames.length > 5) {
      const moreSpan = document.createElement('span');
      moreSpan.textContent = '...';
      moreSpan.className = 'works-summary-more cursor-pointer text-blue-500 underline';
      moreSpan.addEventListener('click', () => toggleWorksFullSummary(workNames));
      worksListDiv.appendChild(document.createTextNode(', '));
      worksListDiv.appendChild(moreSpan);
    }
  } else {
    worksListDiv.textContent = workSummary;
    const full = getEl<HTMLElement>('works-full-summary');
    if (full) full.remove();
  }

  const empChecked = document.querySelectorAll<HTMLInputElement>('input[name="employee_ids"]:checked');
  summaryBox.style.display = (empChecked.length > 0 || workChecked.length > 0) ? '' : 'none';
}

/* Init listeners */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll<HTMLInputElement>('input[name="work_ids"]').forEach(cb => {
    cb.addEventListener('change', updateSelectedWorksSummary);
  });
  const selectAllWork = getEl<HTMLInputElement>('select-all-works');
  if (selectAllWork) selectAllWork.addEventListener('change', updateSelectedWorksSummary);
  updateSelectedWorksSummary();
});

/* Expose for legacy templates expecting globals */
declare global {
  interface Window {
    updateSelectedWorksSummary?: typeof updateSelectedWorksSummary;
    toggleWorksFullSummary?: typeof toggleWorksFullSummary;
  }
}
window.updateSelectedWorksSummary = updateSelectedWorksSummary;
window.toggleWorksFullSummary = toggleWorksFullSummary;
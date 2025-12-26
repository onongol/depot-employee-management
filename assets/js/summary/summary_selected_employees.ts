/**
 * Type-safe rewrite of summary_selected_employees.js
 * - Strict typing, no `any`
 * - Safe DOM queries and null checks
 * - Small helpers to extract text nodes reliably
 */

declare function gettext(s: string): string;

interface EmployeeInfo {
  id: string;
  name: string;
}

function getTextNodeTrimmed(cell: Element | null): string {
  if (!cell) return '';
  // prefer direct visible text node (skip labels/elements)
  const txt = Array.from(cell.childNodes)
    .filter((n): n is ChildNode => n.nodeType === Node.TEXT_NODE)
    .map(n => n.textContent?.trim() ?? '')
    .find(Boolean);
  return txt ?? (cell.textContent?.trim() ?? '');
}

function getEmployeeIdAndName(cb: HTMLInputElement | null): EmployeeInfo {
  if (!cb) return { id: '', name: '' };
  const row = cb.closest('tr');
  if (!row) return { id: '', name: '' };
  const empIdCell = row.querySelector('td:nth-child(2)');
  const empNameCell = row.querySelector('td:nth-child(3)');
  return {
    id: getTextNodeTrimmed(empIdCell),
    name: empNameCell ? (empNameCell.textContent?.trim() ?? '') : '',
  };
}

export function updateSelectedEmployeesSummary(): void {
  const empCheckboxes = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="employee_ids"]'));
  const empChecked = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="employee_ids"]:checked'));
  const selectAllEmp = document.getElementById('select-all-employees') as HTMLInputElement | null;

  let empSummary = gettext('No employees selected');

  if (selectAllEmp && empCheckboxes.length > 0 && selectAllEmp.checked && empChecked.length === empCheckboxes.length) {
    empSummary = gettext('Selected all');
  } else {
    const names: string[] = empChecked.map(cb => {
      const { id, name } = getEmployeeIdAndName(cb);
      return id && name ? `${id}/${name}` : '';
    }).filter(Boolean);
    if (names.length) empSummary = names.join(', ');
  }

  const summaryEl = document.getElementById('selected-employees-list');
  if (summaryEl) summaryEl.textContent = empSummary;

  const workChecked = document.querySelectorAll<HTMLInputElement>('input[name="work_ids"]:checked');
  const selectedSummary = document.getElementById('selected-summary') as HTMLElement | null;
  if (selectedSummary) {
    selectedSummary.style.display = (empChecked.length > 0 || workChecked.length > 0) ? '' : 'none';
  }
}

// Init listeners
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll<HTMLInputElement>('input[name="employee_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateSelectedEmployeesSummary());
  });
  const selectAllEmp = document.getElementById('select-all-employees') as HTMLInputElement | null;
  if (selectAllEmp) selectAllEmp.addEventListener('change', () => updateSelectedEmployeesSummary());
  updateSelectedEmployeesSummary();
});
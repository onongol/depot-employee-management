/**
 * Summary for selected daily salaries.
 * Fills #selected-daily-salary with "ID/Name - YYYY-MM-DD" entries for checked rows.
 */

function getTextNodeTrimmed(cell: Element | null): string {
  if (!cell) return '';
  const txt = Array.from(cell.childNodes)
    .filter((n): n is ChildNode => n.nodeType === Node.TEXT_NODE)
    .map(n => n.textContent?.trim() ?? '')
    .find(Boolean);
  return txt ?? (cell?.textContent?.trim() ?? '');
}

interface DailySalaryInfo {
  id: string;
  name: string;
  date: string;
}

function getDailySalaryInfo(cb: HTMLInputElement | null): DailySalaryInfo {
  if (!cb) return { id: '', name: '', date: '' };
  const row = cb.closest('tr');
  if (!row) return { id: '', name: '', date: '' };
  const tds = Array.from(row.querySelectorAll('td'));
  const hasCheckbox = !!row.querySelector('input[name="daily_salary_ids"]');
  const idIdx = hasCheckbox ? 2 : 1; // based on template structure
  const nameIdx = idIdx + 1;
  const id = getTextNodeTrimmed(tds[idIdx] ?? null);
  const name = getTextNodeTrimmed(tds[nameIdx] ?? null);
  const dateCell = tds.find(td => /\d{4}-\d{2}-\d{2}/.test(td.textContent ?? '')) ?? null;
  const date = getTextNodeTrimmed(dateCell);
  return { id, name, date };
}

export function updateSelectedDailySalariesSummary(): void {
  const checked = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="daily_salary_ids"]:checked'));

  const summaryEl = document.getElementById('selected-daily-salary');
  if (!summaryEl) return;

  let text = (checked.length === 0) ? 'No daily salaries selected' : '';

  if (checked.length > 0) {
    const items = checked.map(cb => {
      const { id, name, date } = getDailySalaryInfo(cb);
      const idName = id && name ? `${id}/${name}` : id || name || '';
      return idName && date ? `${idName} - ${date}` : idName || date;
    }).filter(Boolean);
    text = items.join(', ');
  }

  summaryEl.textContent = text;

  const selectedSummary = document.getElementById('selected-summary') as HTMLElement | null;
  if (selectedSummary) {
    selectedSummary.style.display = (checked.length > 0) ? '' : 'none';
  }
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll<HTMLInputElement>('input[name="daily_salary_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateSelectedDailySalariesSummary());
  });
  updateSelectedDailySalariesSummary();
});

// expose (optional) for inline usage
// (window as any).updateSelectedDailySalariesSummary = updateSelectedDailySalariesSummary;
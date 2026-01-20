function getTextNodeTrimmed(cell: Element | null): string {
  if (!cell) return '';
  const txt = Array.from(cell.childNodes)
    .filter((n): n is ChildNode => n.nodeType === Node.TEXT_NODE)
    .map(n => n.textContent?.trim() ?? '')
    .find(Boolean);
  return txt ?? (cell?.textContent?.trim() ?? '');
}

interface DailyWorkInfo {
  work: string;
  type: string;
  date: string;
}

function getDailyWorkInfo(cb: HTMLInputElement | null): DailyWorkInfo {
  if (!cb) return { work: '', type: '', date: '' };
  const row = cb.closest('tr');
  if (!row) return { work: '', type: '', date: '' };
  const tds = Array.from(row.querySelectorAll('td'));
  const hasCheckbox = !!row.querySelector('input[name="daily_work_ids"]');
  const workIdx = hasCheckbox ? 2 : 1;
  const typeIdx = hasCheckbox ? 4 : 3;
  const dateCell = tds.find(td => /\d{4}-\d{2}-\d{2}/.test(td.textContent ?? '')) ?? null;
  const work = getTextNodeTrimmed(tds[workIdx] ?? null);
  const type = getTextNodeTrimmed(tds[typeIdx] ?? null);
  const date = getTextNodeTrimmed(dateCell);
  return { work, type, date };
}

export function updateSelectedDailyWorksSummary(): void {
  const checked = Array.from(document.querySelectorAll<HTMLInputElement>('input[name="daily_work_ids"]:checked'));
  const summaryEl = document.getElementById('selected-daily-work');
  if (!summaryEl) return;

  let text = (checked.length === 0) ? 'No daily works selected' : '';

  if (checked.length > 0) {
    const items = checked.map(cb => {
      const { work, type, date } = getDailyWorkInfo(cb);
      let label = work;
      if (type) label += ` (${type})`;
      if (date) label += ` - ${date}`;
      return label;
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
  document.querySelectorAll<HTMLInputElement>('input[name="daily_work_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateSelectedDailyWorksSummary());
  });
  updateSelectedDailyWorksSummary();
});
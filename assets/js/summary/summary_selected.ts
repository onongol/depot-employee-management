type SummaryConfig = {
  checkboxName: string;
  summarySpanId: string;
  summaryBoxId?: string;
  emptyText: string;
  allText?: string;
  selectAllId?: string;
  countId?: string;
  labelId?: string;
  getLabel: (cb: HTMLInputElement) => string;
};

export function updateGenericSummary(config: SummaryConfig): void {
  const checkboxes = Array.from(document.querySelectorAll<HTMLInputElement>(`input[name="${config.checkboxName}"]`));
  const checked = checkboxes.filter(cb => cb.checked);
  const summaryEl = document.getElementById(config.summarySpanId);
  const summaryBox = config.summaryBoxId ? document.getElementById(config.summaryBoxId) : null;
  const countEl = config.countId ? document.getElementById(config.countId) : null;

  const selectAll = config.selectAllId ? document.getElementById(config.selectAllId) as HTMLInputElement | null : null;
  const emptyText = summaryBox?.dataset.emptyText ?? config.emptyText;
  const allText = summaryBox?.dataset.allText ?? config.allText ?? emptyText;
  const selectedText = summaryBox?.dataset.selectedText ?? 'selected';

  const allSelected = Boolean(selectAll && checkboxes.length > 0 && selectAll.checked && checked.length === checkboxes.length);

  let text = emptyText;

  if (allSelected) {
    text = `${allText} ${checked.length} ${selectedText}`.trim();
  } else if (checked.length > 0) {
    text = checked.map(cb => config.getLabel(cb)).filter(Boolean).join(', ');
  }

  if (summaryEl) summaryEl.textContent = text;

  if (countEl) {
    if (allSelected) {
      countEl.style.display = 'none';
    } else {
      countEl.style.display = '';
      countEl.textContent = String(checked.length);
    }
  }

  if (summaryBox) {
    const detailsEl = summaryBox.querySelector<HTMLDetailsElement>('details');
    if (detailsEl) {
      const summaryToggle = detailsEl.querySelector<HTMLElement>('summary');
      const labelSpan = config.labelId ? document.getElementById(config.labelId) : summaryToggle ? summaryToggle.querySelectorAll('span')[1] as HTMLElement | undefined : undefined;
      const chevron = summaryToggle ? summaryToggle.querySelector<HTMLElement>('svg') : null;

      if (labelSpan && labelSpan.dataset.origLabel === undefined) {
        labelSpan.dataset.origLabel = labelSpan.textContent ?? '';
      }

      if (!detailsEl.dataset.toggleGuardAdded) {
        detailsEl.addEventListener('toggle', () => {
          if (detailsEl.dataset.preventOpen === 'true') {
            detailsEl.open = false;
          }
        });
        detailsEl.dataset.toggleGuardAdded = '1';
      }

      if (allSelected) {
        detailsEl.open = false;
        detailsEl.dataset.preventOpen = 'true';
        if (summaryToggle) summaryToggle.style.pointerEvents = 'none';
        if (labelSpan) labelSpan.textContent = `${allText} ${checked.length} ${selectedText}`.trim();
        if (chevron) chevron.classList.add('hidden');
      } else {
        detailsEl.dataset.preventOpen = 'false';
        if (summaryToggle) summaryToggle.style.pointerEvents = '';
        if (labelSpan) labelSpan.textContent = labelSpan.dataset.origLabel ?? selectedText;
        if (chevron) chevron.classList.remove('hidden');
      }
    }

    if (checked.length > 0) {
      summaryBox.classList.remove('hidden');
      summaryBox.style.display = '';
    } else {
      summaryBox.classList.add('hidden');
      summaryBox.style.display = 'none';
    }
  }
}

const employeesSummaryConfig: SummaryConfig = {
  checkboxName: 'employee_ids',
  summarySpanId: 'selected-employees-list',
  summaryBoxId: 'selected-employees-summary',
  selectAllId: 'select-all-employees',
  countId: 'selected-employees-count',
  labelId: 'selected-employees-label',
  emptyText: '',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const id = (row.dataset.empId ?? '').trim();
    const name = (row.dataset.empName ?? '').trim();
    return id && name ? `(ID: ${id}) ${name}` : id || name;
  }
};

const worksSummaryConfig: SummaryConfig = {
  checkboxName: 'work_ids',
  summarySpanId: 'selected-works-list',
  summaryBoxId: 'selected-works-summary',
  selectAllId: 'select-all-works',
  countId: 'selected-works-count',
  labelId: 'selected-works-label',
  emptyText: '',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const workName = (row.dataset.workName ?? '').trim();
    return workName;
  },
};

const dailySalariesSummaryConfig: SummaryConfig = {
  checkboxName: 'daily_salary_ids',
  summarySpanId: 'selected-daily-salary-list',
  summaryBoxId: 'selected-daily-salary-summary',
  selectAllId: 'select-all-daily-salary',
  countId: 'selected-daily-salary-count',
  labelId: 'selected-daily-salary-label',
  emptyText: '',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const id = (row.dataset.empId ?? '').trim();
    const name = (row.dataset.empName ?? '').trim();
    const date = (row.dataset.salaryDate ?? '').trim();
    return `(ID: ${id}) ${name} - ${date}`;
  }
};

const dailyWorksSummaryConfig: SummaryConfig = {
  checkboxName: 'daily_work_ids',
  summarySpanId: 'selected-daily-work-list',
  summaryBoxId: 'selected-daily-work-summary',
  selectAllId: 'select-all-daily-work',
  countId: 'selected-daily-work-count',
  labelId: 'selected-daily-work-label',
  emptyText: '',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const work = (row.dataset.workName ?? '').trim();
    const type = (row.dataset.typeWork ?? '').trim();
    const date = (row.dataset.workDate ?? '').trim();
    return `${work} (${type}) - ${date}`;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  // Employees
  document.querySelectorAll<HTMLInputElement>('input[name="employee_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateGenericSummary(employeesSummaryConfig));
  });
  // Works
  document.querySelectorAll<HTMLInputElement>('input[name="work_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateGenericSummary(worksSummaryConfig));
  });
  // Daily Salaries
  document.querySelectorAll<HTMLInputElement>('input[name="daily_salary_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateGenericSummary(dailySalariesSummaryConfig));
  });
  // Daily Works
  document.querySelectorAll<HTMLInputElement>('input[name="daily_work_ids"]').forEach(cb => {
    cb.addEventListener('change', () => updateGenericSummary(dailyWorksSummaryConfig));
  });

  updateGenericSummary(employeesSummaryConfig);
  updateGenericSummary(worksSummaryConfig);
  updateGenericSummary(dailySalariesSummaryConfig);
  updateGenericSummary(dailyWorksSummaryConfig);
});

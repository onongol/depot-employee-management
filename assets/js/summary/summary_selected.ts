type SummaryConfig = {
  checkboxName: string;
  summarySpanId: string;
  summaryBoxId?: string;
  emptyText: string;
  allText?: string;
  selectAllId?: string;
  getLabel: (cb: HTMLInputElement) => string;
};

export function updateGenericSummary(config: SummaryConfig): void {
  const checkboxes = Array.from(document.querySelectorAll<HTMLInputElement>(`input[name="${config.checkboxName}"]`));
  const checked = checkboxes.filter(cb => cb.checked);
  const summaryEl = document.getElementById(config.summarySpanId);
  const summaryBox = config.summaryBoxId ? document.getElementById(config.summaryBoxId) : null;
  const selectAll = config.selectAllId ? document.getElementById(config.selectAllId) as HTMLInputElement | null : null;
  const emptyText = summaryBox?.dataset.emptyText ?? config.emptyText;
  const allText = summaryBox?.dataset.allText ?? config.allText ?? emptyText;

  let text = emptyText;

  if (selectAll && checkboxes.length > 0 && selectAll.checked && checked.length === checkboxes.length) {
    text = allText;
  } else if (checked.length > 0) {
    text = checked.map(cb => config.getLabel(cb)).filter(Boolean).join(', ');
  }

  if (summaryEl) summaryEl.textContent = text;

  if (summaryBox) {
    if (checked.length > 0) {
      summaryBox.classList.remove('hidden');
      summaryBox.style.display = '';
    } else {
      summaryBox.classList.add('hidden');
      summaryBox.style.display = 'none';
    }
  }
}

const employeesSummaryConfig = {
  checkboxName: 'employee_ids',
  summarySpanId: 'selected-employees-list',
  summaryBoxId: 'selected-employees-summary',
  selectAllId: 'select-all-employees',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const id = (row.dataset.empId ?? '').trim();
    const name = (row.dataset.empName ?? '').trim();
    return id && name ? `${id}/${name}` : id || name;
  }
};

const worksSummaryConfig = {
  checkboxName: 'work_ids',
  summarySpanId: 'selected-works-list',
  summaryBoxId: 'selected-works-summary',
  selectAllId: 'select-all-works',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const workName = (row.dataset.workName ?? '').trim();
    return workName;
  },
};

const dailySalariesSummaryConfig = {
  checkboxName: 'daily_salary_ids',
  summarySpanId: 'selected-daily-salary',
  summaryBoxId: 'selected-summary',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const id = (row.dataset.empId ?? '').trim();
    const name = (row.dataset.empName ?? '').trim();
    const date = (row.dataset.salaryDate ?? '').trim();
    return `${id}/${name} - ${date}`;
  }
};

const dailyWorksSummaryConfig = {
  checkboxName: 'daily_work_ids',
  summarySpanId: 'selected-daily-work',
  summaryBoxId: 'selected-summary',
  getLabel: (cb: HTMLInputElement) => {
    const row = cb.closest('tr');
    if (!row) return '';
    const work = (row.dataset.workName ?? '').trim();
    const type = (row.dataset.typeWork ?? '').trim();
    const date = (row.dataset.workDate ?? '').trim();
    return `${work}(${type}) - ${date}`;
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

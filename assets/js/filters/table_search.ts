/**
 * Table search + select filters (TypeScript, strict, no any).
 * Keeps backward compatibility with window.TABLE_SEARCHES / TABLE_SELECT_FILTERS.
 */

type TableSearchConfig = [inputId: string, tableBodyId: string, columnIndex?: number];
type TableSelectConfig = [selectId: string, tableBodyId: string, columnIndex?: number];

declare global {
  interface Window {
    TABLE_SEARCHES?: TableSearchConfig[];
    TABLE_SELECT_FILTERS?: TableSelectConfig[];
    filterTableRows?: (inputId: string, tableBodyId: string, columnIndex?: number) => void;
    filterTableBySelect?: (selectId: string, tableBodyId: string, columnIndex?: number) => void;
  }
}

const getEl = <T extends HTMLElement = HTMLElement>(id?: string | null): T | null => {
  if (!id) return null;
  return document.getElementById(id) as T | null;
};

const getCellText = (td: HTMLTableCellElement | undefined | null): string =>
  (td?.textContent ?? '').trim();

const splitIds = (raw?: string | null): string[] =>
  (raw ?? '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);

type ActiveFilter = { col: number; value: string; mode: 'text' | 'select' };

function collectFilters(tableId: string): ActiveFilter[] {
  const filters: ActiveFilter[] = [];

  document.querySelectorAll<HTMLInputElement>('input[data-table]').forEach((input) => {
    const tables = splitIds(input.dataset.table);
    if (!tables.includes(tableId)) return;
    const col = input.dataset.column ? Number(input.dataset.column) : 1;
    const val = (input.value ?? '').trim();
    if (val) filters.push({ col, value: val.toLowerCase(), mode: 'text' });
  });

  document.querySelectorAll<HTMLSelectElement>('select[data-table]').forEach((sel) => {
    const tables = splitIds(sel.dataset.table);
    if (!tables.includes(tableId)) return;
    const cols = splitIds(sel.dataset.column).map((c) => Number(c));
    const col = cols[tables.indexOf(tableId)] ?? cols[cols.length - 1] ?? 1;
    const val = (sel.value ?? '').trim();
    if (val) filters.push({ col, value: val, mode: 'select' });
  });

  return filters;
}

export function applyTableFilters(tableBodyId: string): void {
  const table = getEl<HTMLTableSectionElement>(tableBodyId);
  if (!table) return;
  const filters = collectFilters(tableBodyId);
  const trs = Array.from(table.getElementsByTagName('tr'));

  for (const tr of trs) {
    const keep = filters.every((f) => {
      const td = tr.getElementsByTagName('td')[f.col];
      const cell = getCellText(td);
      return f.mode === 'text'
        ? cell.toLowerCase().includes(f.value)
        : cell === f.value;
    });
    tr.style.display = keep ? '' : 'none';
  }
}

// Update legacy functions for compatibility with the new filtering logic
export function filterTableRows(inputId: string, tableBodyId: string, _columnIndex = 1): void {
  applyTableFilters(tableBodyId);
}

export function filterTableBySelect(selectId: string, tableBodyId: string, _columnIndex = 1): void {
  applyTableFilters(tableBodyId);
}

/* DOM init (backwards-compatible) */
document.addEventListener('DOMContentLoaded', () => {
  // 1) Legacy window.TABLE_SEARCHES initializer
  const searches: TableSearchConfig[] = window.TABLE_SEARCHES ?? [];
  searches.forEach(([inputId, tableBodyId]) => {
    const input = getEl<HTMLInputElement>(inputId);
    if (!input) return;
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        applyTableFilters(tableBodyId);
      }
    });
  });

  // 2) Auto-init from data-attributes on inputs
  document.querySelectorAll<HTMLInputElement>('input[data-table]').forEach((input) => {
    const tables = splitIds(input.dataset.table);
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        tables.forEach(applyTableFilters);
      }
    });
  });

  // 3) Auto-init selects with data-table
  document.querySelectorAll<HTMLSelectElement>('select[data-table]').forEach((sel) => {
    const tables = splitIds(sel.dataset.table);
    sel.addEventListener('change', () => tables.forEach(applyTableFilters));
  });

  // 4) Compatibility: window.TABLE_SELECT_FILTERS
  const selectFilters: TableSelectConfig[] = window.TABLE_SELECT_FILTERS ?? [];
  selectFilters.forEach(([selectId, tableBodyId]) => {
    const sel = getEl<HTMLSelectElement>(selectId);
    if (!sel) return;
    sel.addEventListener('change', () => applyTableFilters(tableBodyId));
  });
});

// Expose for legacy inline usage
window.filterTableRows = filterTableRows;
window.filterTableBySelect = filterTableBySelect;
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

export function filterTableRows(inputId: string, tableBodyId: string, columnIndex = 1): void {
  const input = getEl<HTMLInputElement | HTMLTextAreaElement | HTMLInputElement>(inputId);
  if (!input) return;
  const filter = (input.value ?? '').toLowerCase();
  const table = getEl<HTMLTableSectionElement>(tableBodyId);
  if (!table) return;

  const trs = Array.from(table.getElementsByTagName('tr'));
  for (const tr of trs) {
    const td = tr.getElementsByTagName('td')[columnIndex];
    const txt = getCellText(td).toLowerCase();
    tr.style.display = txt.indexOf(filter) > -1 ? '' : 'none';
  }
}

export function filterTableBySelect(selectId: string, tableBodyId: string, columnIndex = 1): void {
  const select = getEl<HTMLSelectElement>(selectId);
  const table = getEl<HTMLTableSectionElement>(tableBodyId);
  if (!select || !table) return;
  const value = select.value;
  const trs = Array.from(table.getElementsByTagName('tr'));
  for (const tr of trs) {
    const td = tr.getElementsByTagName('td')[columnIndex];
    const cell = getCellText(td);
    tr.style.display = !value || cell === value ? '' : 'none';
  }
}

/* DOM init (backwards-compatible) */
document.addEventListener('DOMContentLoaded', () => {
  // 1) Legacy window.TABLE_SEARCHES initializer
  const searches: TableSearchConfig[] = window.TABLE_SEARCHES ?? [];
  searches.forEach(([inputId, tableBodyId, columnIndex]) => {
    const input = getEl<HTMLInputElement>(inputId);
    if (!input) return;
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        filterTableRows(inputId, tableBodyId, columnIndex ?? 1);
      }
    });
  });

  // 2) Auto-init from data-attributes on inputs
  document.querySelectorAll<HTMLInputElement>('input[data-table]').forEach((input) => {
    const table = input.dataset.table;
    if (!table) return;
    const col = input.dataset.column ? Number(input.dataset.column) : 1;
    input.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        filterTableRows(input.id, table, col);
      }
    });
  });

  // 3) Auto-init selects with data-table
  document.querySelectorAll<HTMLSelectElement>('select[data-table]').forEach((sel) => {
    const table = sel.dataset.table;
    if (!table) return;
    const col = sel.dataset.column ? Number(sel.dataset.column) : 1;
    sel.addEventListener('change', () => {
      filterTableBySelect(sel.id, table, col);
    });
  });

  // 4) Compatibility: window.TABLE_SELECT_FILTERS
  const selectFilters: TableSelectConfig[] = window.TABLE_SELECT_FILTERS ?? [];
  selectFilters.forEach(([selectId, tableBodyId, columnIndex]) => {
    const sel = getEl<HTMLSelectElement>(selectId);
    if (!sel) return;
    sel.addEventListener('change', () => {
      filterTableBySelect(selectId, tableBodyId, columnIndex ?? 1);
    });
  });
});

/* Expose for legacy inline usage */
window.filterTableRows = filterTableRows;
window.filterTableBySelect = filterTableBySelect;
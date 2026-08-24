/**
 * Table search + select filters (TypeScript, strict, no any).
 * Manages table row visibility based on multiple filtering criteria.
 * * Supports two configuration modes:
 * 1. Declarative: via `data-table` and `data-column` attributes on inputs/selects.
 * 2. Centralized: via JSON configurations stored in the root element's dataset.
 * * Keeps backward compatibility with window.TABLE_SEARCHES / TABLE_SELECT_FILTERS.
 */
type TableSearchConfig = [
  inputId: string,
  tableBodyId: string,
  columnIndex?: number,
];

type TableSelectConfig = [
  selectId: string,
  tableBodyId: string,
  columnIndex?: number,
];

/** Column index used when no data-column attribute is present. */
const TABLE_SEARCH_DEFAULT_COLUMN = 0;

/** ID of the root element that holds centralized JSON config in its dataset. */
const TABLE_SEARCH_IDS = {
  app: "app",
} as const;

const TABLE_SEARCH_ATTRS = {
  inputTable: "input[data-table]",
  selectTable: "select[data-table]",
} as const;

const TABLE_SEARCH_MODES = {
  text: "text",
  select: "select",
} as const;

const TABLE_SEARCH_TAGS = {
  tableCell: "td",
  tableRow: "tr",
} as const;

const TABLE_SEARCH_KEYS = {
  enter: "Enter",
  keySearches: "searches",
  keySelectFilters: "selectFilters",
} as const;

const TABLE_SEARCH_DISPLAY = {
  displayNone: "none",
} as const;

/** A resolved filter criterion ready to be applied to a table row. */
type ActiveFilter = {
  col: number;
  value: string;
  mode: (typeof TABLE_SEARCH_MODES)[keyof typeof TABLE_SEARCH_MODES];
};

/* -- Utilities -- */
/** Typed wrapper around `document.getElementById`. Returns null when id is falsy. */
const getById = <T extends HTMLElement = HTMLElement>(
  id?: string | null,
): T | null => (id ? (document.getElementById(id) as T | null) : null);

/** Returns trimmed text content of a table cell, or "" when the cell is absent. */
const getCellText = (td: HTMLTableCellElement | undefined | null): string =>
  (td?.textContent ?? "").trim();

/**
 * Splits a comma-separated attribute value (e.g. "tableA, tableB") into an
 * array of trimmed, non-empty strings.
 */
const splitIds = (raw?: string | null): string[] =>
  (raw ?? "")
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean);

/**
 * Scans the document for all active input/select controls that target
 * `tableId` and returns a list of resolved filter criteria.
 *
 * Called on every submit/change event, so it always reflects the current
 * state of the controls without caching stale values.
 */
function collectFilters(tableId: string): ActiveFilter[] {
  const filters: ActiveFilter[] = [];

  // Inputs
  for (const input of Array.from(
    document.querySelectorAll<HTMLInputElement>(TABLE_SEARCH_ATTRS.inputTable),
  )) {
    const tables = splitIds(input.dataset.table ?? null);
    if (!tables.includes(tableId)) continue;

    const col = input.dataset.column
      ? Number(input.dataset.column)
      : TABLE_SEARCH_DEFAULT_COLUMN;

    const val = (input.value ?? "").trim();
    if (val)
      filters.push({
        col,
        value: val.toLowerCase(),
        mode: TABLE_SEARCH_MODES.text,
      });
  }

  // Selects
  for (const sel of Array.from(
    document.querySelectorAll<HTMLSelectElement>(
      TABLE_SEARCH_ATTRS.selectTable,
    ),
  )) {
    const tables = splitIds(sel.dataset.table ?? null);
    if (!tables.includes(tableId)) continue;

    const cols = splitIds(sel.dataset.column ?? null).map((c) => Number(c));
    const col =
      cols[tables.indexOf(tableId)] ??
      cols[cols.length - 1] ??
      TABLE_SEARCH_DEFAULT_COLUMN;

    const val = (sel.value ?? "").trim();
    if (val) filters.push({ col, value: val, mode: TABLE_SEARCH_MODES.select });
  }

  return filters;
}

/**
 * Applies all active filters to the table identified by `tableBodyId`.
 * Rows that satisfy every filter are shown; others are hidden via `display:none`.
 * When no filters are active, all rows become visible.
 */
export function applyTableFilters(tableBodyId: string): void {
  const table = getById<HTMLTableSectionElement>(tableBodyId);
  if (!table) return;

  const filters = collectFilters(tableBodyId);
  const trs = Array.from(
    table.getElementsByTagName(TABLE_SEARCH_TAGS.tableRow),
  );

  for (const tr of trs) {
    const keep = filters.every((f) => {
      const td = tr.getElementsByTagName(TABLE_SEARCH_TAGS.tableCell)[f.col];
      const cell = getCellText(td);
      return f.mode === TABLE_SEARCH_MODES.text
        ? cell.toLowerCase().includes(f.value)
        : cell === f.value;
    });
    tr.style.display = keep ? "" : TABLE_SEARCH_DISPLAY.displayNone;
  }
}

/**
 * Kept for backward compatibility with existing inline `onkeydown` handlers.
 * The `inputId` and `columnIndex` parameters are no longer used; filtering
 * is driven entirely by `data-table` / `data-column` attributes.
 *
 * @deprecated Use `applyTableFilters` directly, or switch to data-attributes.
 */
export function filterTableRows(
  _inputId: string,
  tableBodyId: string,
  _columnIndex = TABLE_SEARCH_DEFAULT_COLUMN,
): void {
  applyTableFilters(tableBodyId);
}

/**
 * Kept for backward compatibility with existing inline `onchange` handlers.
 * See `filterTableRows` — same deprecation applies.
 *
 * @deprecated Use `applyTableFilters` directly, or switch to data-attributes.
 */
export function filterTableBySelect(
  _selectId: string,
  tableBodyId: string,
  _columnIndex = TABLE_SEARCH_DEFAULT_COLUMN,
): void {
  applyTableFilters(tableBodyId);
}

/**
 * Reads a JSON config array from the root element's dataset.
 * Falls back to `document.documentElement` when no element with id="app" exists.
 * Returns an empty array on parse failure so the rest of init can continue safely.
 */
function parseRootConfigs<T = unknown>(
  key:
    | typeof TABLE_SEARCH_KEYS.keySearches
    | typeof TABLE_SEARCH_KEYS.keySelectFilters,
): T[] {
  const root =
    document.getElementById(TABLE_SEARCH_IDS.app) ?? document.documentElement;
  const raw =
    key === TABLE_SEARCH_KEYS.keySearches
      ? root.dataset.searches
      : root.dataset.selectFilters;
  if (!raw) return [];
  try {
    return JSON.parse(raw) as T[];
  } catch {
    return [];
  }
}

/* DOM initialisation */
document.addEventListener("DOMContentLoaded", () => {
  /**
   * Tracks elements that have already been wired up with event listeners.
   * Prevents double-subscription when the same element appears in both
   * the centralized config and the data-attribute discovery pass.
   */
  const initialized = new WeakSet<HTMLElement>();

  /** Calls `fn` exactly once per element; subsequent calls for the same element are no-ops. */
  const onceInit = <T extends HTMLElement = HTMLElement>(
    el: T | null,
    fn: (el: T) => void,
  ) => {
    if (!el || initialized.has(el)) return;
    fn(el);
    initialized.add(el);
  };

  // Load centralized config from the root element's dataset
  const searches: TableSearchConfig[] = parseRootConfigs<TableSearchConfig>(
    TABLE_SEARCH_KEYS.keySearches,
  );
  const selectFilters: TableSelectConfig[] =
    parseRootConfigs<TableSelectConfig>(TABLE_SEARCH_KEYS.keySelectFilters);

  /**
   * Index of inputId → Set<tableBodyId> built from the centralized config.
   * Merged with the element's own `data-table` attribute during init so that
   * JS config and declarative attributes are both honoured.
   */
  const searchMap = new Map<string, Set<string>>();
  for (const [inputId, tableBodyId] of searches) {
    if (!inputId) continue;
    if (!searchMap.has(inputId)) searchMap.set(inputId, new Set());
    searchMap.get(inputId)?.add(tableBodyId);
  }

  /** Same index for select elements. */
  const selectMap = new Map<string, Set<string>>();
  for (const [selectId, tableBodyId] of selectFilters) {
    if (!selectId) continue;
    if (!selectMap.has(selectId)) selectMap.set(selectId, new Set());
    selectMap.get(selectId)?.add(tableBodyId);
  }

  // Inputs
  // Union of: elements found via data-attribute + elements listed in config.
  // deduplication via Set ensures each element is initialised exactly once
  const dataInputs = Array.from(
    document.querySelectorAll<HTMLInputElement>(TABLE_SEARCH_ATTRS.inputTable),
  );
  const configInputs = Array.from(searchMap.keys())
    .map((id) => getById<HTMLInputElement>(id))
    .filter((el): el is HTMLInputElement => el !== null);
  const allInputs = Array.from(new Set([...dataInputs, ...configInputs]));

  for (const input of allInputs) {
    onceInit(input, (inputEl) => {
      // Merge tables from both sources so neither config takes precedence
      const fromAttr = splitIds(inputEl.dataset.table ?? null);
      const fromConfig = Array.from(searchMap.get(inputEl.id ?? "") ?? []);
      const tableIds = Array.from(new Set([...fromAttr, ...fromConfig]));
      if (tableIds.length === 0) return;

      // Trigger filtering on Enter; preventDefault stops form submission
      inputEl.addEventListener("keydown", (event: KeyboardEvent) => {
        if (event.key !== TABLE_SEARCH_KEYS.enter) return;
        event.preventDefault();
        for (const tableId of tableIds) applyTableFilters(tableId);
      });
    });
  }

  // Selects
  // Union of: elements found via data-attribute + elements listed in config.
  // Deduplication via Set ensures each element is initialised exactly once.
  const dataSelects = Array.from(
    document.querySelectorAll<HTMLSelectElement>(
      TABLE_SEARCH_ATTRS.selectTable,
    ),
  );
  const configSelects = Array.from(selectMap.keys())
    .map((id) => getById<HTMLSelectElement>(id))
    .filter((el): el is HTMLSelectElement => el !== null);
  const allSelects = Array.from(new Set([...dataSelects, ...configSelects]));

  for (const sel of allSelects) {
    onceInit(sel, (selectEl) => {
      const fromAttr = splitIds(selectEl.dataset.table ?? null);
      const fromConfig = Array.from(selectMap.get(selectEl.id ?? "") ?? []);
      const tableIds = Array.from(new Set([...fromAttr, ...fromConfig]));
      if (tableIds.length === 0) return;

      selectEl.addEventListener("change", () => {
        for (const tableId of tableIds) applyTableFilters(tableId);
      });
    });
  }
});

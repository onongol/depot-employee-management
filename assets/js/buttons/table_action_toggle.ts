/**
 * Bulk Action Management (TypeScript, strict, modular).
 * Automatically toggles visibility for Delete (1+ items) and Edit (exactly 1 item).
 * Syncs row metadata (ID, URL, Name) to the action buttons via dataset attributes.
 */

const BULK_ACTION_SELECTORS = {
	deleteButton: "bulk-delete-button",
	editButton: "bulk-edit-button",
	checkboxAll: "[data-checkbox-name]",
	checkboxRow: "[data-row-checkbox-name]",
} as const;

const BULK_ACTION_CLASSES = {
	hidden: "hidden",
} as const;

const BULK_ACTION_TAGS = {
	tableRow: "tr",
} as const;

/**
 * Returns a CSS selector for checked row checkboxes within a specific group.
 */
const getCheckedRowSelector = (name: string) =>
	`[data-row-checkbox-name="${name}"]:checked`;

/**
 * Scans the entire document for all checked row checkboxes.
 */
function getAllCheckedCheckboxes(): NodeListOf<HTMLInputElement> {
	return document.querySelectorAll<HTMLInputElement>(
		`${BULK_ACTION_SELECTORS.checkboxRow}:checked`,
	);
}

/**
 * Calculates the total number of checked checkboxes across specified groups.
 * Optimizes performance for single-group vs. multi-group scenarios.
 */
function getCheckedCount(names: string[]): number {
	if (names.length === 0) return 0;

	const checked = getAllCheckedCheckboxes();

	// Performance optimization for the common case (single group)
	if (names.length === 1) {
		return checked.length;
	}

	// Filter and count for multi-group scenarios
	return Array.from(checked).filter((cb) =>
		names.includes(cb.dataset.rowCheckboxName!),
	).length;
}

/**
 * Retrieves all unique checkbox group names from the page's "Select All" toggles.
 */
function getCheckboxNames(): string[] {
	return Array.from(
		document.querySelectorAll<HTMLInputElement>(
			BULK_ACTION_SELECTORS.checkboxAll,
		),
	)
		.map((checkbox) => checkbox.dataset.checkboxName)
		.filter((name): name is string => Boolean(name));
}

/**
 * Extracts metadata (id, url, name) from the single selected row.
 * Returns null if zero or multiple rows are selected within the group context.
 */
function getSelectedRowData(
	names: string[],
): { id: string; url: string; name: string } | null {
	for (const name of names) {
		const checked = document.querySelectorAll<HTMLInputElement>(
			getCheckedRowSelector(name),
		);

		// Metadata extraction is only valid for a unique selection
		if (checked.length === 1) {
			const checkbox = checked[0];
			if (!checkbox) return null;
			const row = checkbox.closest(BULK_ACTION_TAGS.tableRow);
			return {
				id: row?.dataset.rowId ?? checkbox.value,
				url: row?.dataset.editUrl ?? "",
				name: row?.dataset.rowName ?? "",
			};
		}
	}
	return null;
}

/**
 * Main Orchestrator: Initializes button synchronization on DOM load.
 */
document.addEventListener("DOMContentLoaded", () => {
	const deleteBtn = document.getElementById(
		BULK_ACTION_SELECTORS.deleteButton,
	) as HTMLButtonElement | null;
	const editBtn = document.getElementById(
		BULK_ACTION_SELECTORS.editButton,
	) as HTMLButtonElement | null;

	// Exit early if no action buttons are present on the current page
	if (!deleteBtn && !editBtn) return;

	const names = getCheckboxNames();

	/** Main UI Sync Function: Updates button visibility and datasets based on current selection. */
	function syncButtons(): void {
		const count = getCheckedCount(names);

		// "Delete" logic: Visible when 1 or more items are selected
		deleteBtn?.classList.toggle(BULK_ACTION_CLASSES.hidden, count === 0);

		// "Edit" logic: Visible strictly when exactly 1 item is selected
		if (editBtn) {
			editBtn.classList.toggle(BULK_ACTION_CLASSES.hidden, count !== 1);

			if (count === 1) {
				const data = getSelectedRowData(names);
				if (data) {
					// Inject metadata into button datasets for use in modals or navigation
					editBtn.dataset.id = data.id;
					editBtn.dataset.url = data.url;
					editBtn.dataset.name = data.name;
				}
			} else {
				// Clear datasets when edit mode is inactive
				editBtn.dataset.id = "";
				editBtn.dataset.url = "";
				editBtn.dataset.name = "";
			}
		}
	}

	// Global listener using event delegation for any checkbox changes
	document.addEventListener("change", (e) => {
		const target = e.target;
		if (!(target instanceof HTMLInputElement)) return;
		if (target.dataset.checkboxName || target.dataset.rowCheckboxName) {
			syncButtons();
		}
	});

	// Run initial sync to handle browser-refreshed checkbox states
	syncButtons();
});

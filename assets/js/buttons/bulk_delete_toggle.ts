/**
 * Bulk delete button toggle logic (TypeScript, strict, modular).
 * Automatically handles the visibility of the delete action based on row selection.
 */

const BULK_DELETE_SELECTORS = {
	button: "bulk-delete-button",
	checkboxAll: "[data-checkbox-name]",
	checkboxRow: "[data-row-checkbox-name]",
} as const;

const BULK_DELETE_CLASSES = {
	hidden: "hidden",
} as const;

/** Helper to generate a CSS selector for checked rows in a specific group */
const getCheckedRowSelector = (name: string) =>
	`[data-row-checkbox-name="${name}"]:checked`;

/** Retrieves the primary action button from the DOM */
function getBulkDeleteButton(): HTMLButtonElement | null {
	return document.getElementById(
		BULK_DELETE_SELECTORS.button,
	) as HTMLButtonElement | null;
}

/** Extracts unique group names from master checkboxes found on the page */
function getCheckboxName(): string[] {
	return Array.from(
		document.querySelectorAll<HTMLInputElement>(
			BULK_DELETE_SELECTORS.checkboxAll,
		),
	)
		.map((cb) => cb.dataset.checkboxName)
		.filter((name): name is string => Boolean(name));
}

function getCheckedRows(name: string): NodeListOf<HTMLInputElement> {
	return document.querySelectorAll<HTMLInputElement>(
		getCheckedRowSelector(name),
	);
}

document.addEventListener("DOMContentLoaded", () => {
	const btn = getBulkDeleteButton();
	if (!btn) return;

	// Cache names at load time for performance
	const names = getCheckboxName();

	/** * Scans the table to see if at least one row is selected.
	 * Uses querySelector for early exit performance.
	 */
	function isAnyChecked(): boolean {
		return names.some((name) => getCheckedRows(name).length > 0);
	}

	/** Synchronizes button visibility with the current selection state */
	function toggleBulkDeleteButton(button: HTMLButtonElement): void {
		button.classList.toggle(BULK_DELETE_CLASSES.hidden, !isAnyChecked());
	}

	/** * Global change listener using event delegation.
	 * Efficiently handles interaction with any checkbox in the system.
	 */
	document.addEventListener("change", (e: Event) => {
		const target = e.target;
		if (!(target instanceof HTMLInputElement)) return;

		// Check if the target belongs to a bulk-delete group
		if (target.dataset.checkboxName || target.dataset.rowCheckboxName) {
			toggleBulkDeleteButton(btn);
		}
	});

	// Initial check in case checkboxes were pre-filled by the browser/server
	toggleBulkDeleteButton(btn);
});

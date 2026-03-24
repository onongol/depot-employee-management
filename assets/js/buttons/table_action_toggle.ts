/**
 * Bulk Action Management (TypeScript, strict, modular).
 * Automatically toggles visibility for Delete (1+ items), Edit (exactly 1 item) A.
 * Syncs row metadata (ID, URL, Name) to the action buttons via dataset attributes.
 */

const BULK_ACTION_SELECTORS = {
	deleteButton: "[data-action-btn='delete']",
	editButton: "[data-action-btn='edit']",
	activationButton: "[data-action-btn='activation']",
	deactivationButton: "[data-action-btn='deactivation']",
	checkboxAll: "[data-checkbox-name]",
	checkboxRow: "[data-row-checkbox-name]",
} as const;

const BULK_ACTION_CLASSES = {
	hidden: "hidden",
} as const;

const BULK_ACTION_TAGS = {
	tableRow: "tr",
} as const;

const BULK_ACTION_ATTRS = {
	hrefAttr: "href",
} as const;

const BULK_ACTION_FALLBACKS = {
	defaultHref: "#",
} as const;

const BULK_ACTION_ANCHORS = {
	activateRow: ".row-activate-url",
	deactivateRow: ".row-deactivate-url",
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
		names.includes(cb.dataset.rowCheckboxName ?? ""),
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
function getSelectedRowData(names: string[]): {
	id: string;
	url: string;
	name: string;
	is_active: boolean | null;
	activate_url: string;
	deactivate_url: string;
} | null {
	for (const name of names) {
		const checked = document.querySelectorAll<HTMLInputElement>(
			getCheckedRowSelector(name),
		);

		// Metadata extraction is only valid for a unique selection
		if (checked.length === 1) {
			const checkbox = checked[0];
			if (!checkbox) return null;
			const row = checkbox.closest(BULK_ACTION_TAGS.tableRow);
			const activateAnchor = row?.querySelector<HTMLAnchorElement>(
				BULK_ACTION_ANCHORS.activateRow,
			);
			const deactivateAnchor = row?.querySelector<HTMLAnchorElement>(
				BULK_ACTION_ANCHORS.deactivateRow,
			);
			const isActiveAttr = row?.dataset.isActive;
			const isActive =
				isActiveAttr === "True" || isActiveAttr === "true"
					? true
					: isActiveAttr === "False" || isActiveAttr === "false"
						? false
						: null;
			return {
				id: row?.dataset.rowId ?? checkbox.value,
				url: row?.dataset.editUrl ?? "",
				name: row?.dataset.rowName ?? "",
				is_active: isActive,
				// Prefer explicit anchor href, then tr dataset, then checkbox dataset as fallback
				activate_url:
					activateAnchor?.getAttribute(BULK_ACTION_ATTRS.hrefAttr) ??
					row?.dataset.activateUrl ??
					checkbox.dataset.activateUrl ??
					"",
				deactivate_url:
					deactivateAnchor?.getAttribute(BULK_ACTION_ATTRS.hrefAttr) ??
					row?.dataset.deactivateUrl ??
					checkbox.dataset.deactivateUrl ??
					"",
			};
		}
	}
	return null;
}

/** Main UI Sync Function: Updates button visibility and datasets based on current selection. */
function syncButtons(): void {
	const names = getCheckboxNames();
	const count = getCheckedCount(names);
	const isSingle = count === 1;
	const data = getSelectedRowData(names);

	const deleteBtn = document.querySelector<HTMLButtonElement>(
		BULK_ACTION_SELECTORS.deleteButton,
	);
	const editBtn = document.querySelector<HTMLButtonElement>(
		BULK_ACTION_SELECTORS.editButton,
	);
	const activationBtn = document.querySelector<HTMLAnchorElement>(
		BULK_ACTION_SELECTORS.activationButton,
	);
	const deactivationBtn = document.querySelector<HTMLAnchorElement>(
		BULK_ACTION_SELECTORS.deactivationButton,
	);

	// Exit early if no action buttons are present on the current page
	if (!deleteBtn && !editBtn && !activationBtn && !deactivationBtn) return;

	// "Delete" logic: Visible when 1 or more items are selected
	deleteBtn?.classList.toggle(BULK_ACTION_CLASSES.hidden, count === 0);

	// "Edit" logic: Visible strictly when exactly 1 item is selected
	if (editBtn) {
		editBtn.classList.toggle(BULK_ACTION_CLASSES.hidden, !isSingle);

		if (isSingle) {
			if (data) {
				// Inject metadata into button datasets for use in modals or navigation
				editBtn.dataset.id = data.id;
				editBtn.dataset.url = data.url;
				editBtn.dataset.name = data.name;
				// Activation buttons: toggle based on selected row active state
				if (activationBtn && deactivationBtn) {
					if (data.is_active === true) {
						activationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
						deactivationBtn.classList.remove(BULK_ACTION_CLASSES.hidden);
						deactivationBtn.dataset.id = data.id;
						deactivationBtn.dataset.name = data.name;
						deactivationBtn.href =
							data.deactivate_url || BULK_ACTION_FALLBACKS.defaultHref;
					} else if (data.is_active === false) {
						deactivationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
						activationBtn.classList.remove(BULK_ACTION_CLASSES.hidden);
						activationBtn.dataset.id = data.id;
						activationBtn.dataset.name = data.name;
						activationBtn.href =
							data.activate_url || BULK_ACTION_FALLBACKS.defaultHref;
					} else {
						// Unknown state: hide both
						activationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
						deactivationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
					}
				}
			}
		} else {
			// Clear datasets when edit mode is inactive
			editBtn.dataset.id = "";
			editBtn.dataset.url = "";
			editBtn.dataset.name = "";
			if (activationBtn) {
				activationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
				activationBtn.href = "";
				activationBtn.dataset.id = "";
				activationBtn.dataset.name = "";
			}
			if (deactivationBtn) {
				deactivationBtn.classList.add(BULK_ACTION_CLASSES.hidden);
				deactivationBtn.href = "";
				deactivationBtn.dataset.id = "";
				deactivationBtn.dataset.name = "";
			}
		}
	}
}

/**
 * Main Orchestrator: Initializes button synchronization on DOM load.
 */
document.addEventListener("DOMContentLoaded", () => {
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

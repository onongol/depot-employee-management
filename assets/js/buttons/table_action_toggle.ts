/**
 * Bulk Action Management (TypeScript, strict, modular).
 * Automatically toggles visibility for Delete (1+ items), Edit (exactly 1 item) and Activation/Deactivation (exactly 1 item).
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

	// Fast path for single-group tables
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

			// Resolve boolean status from dataset string
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
				// Fallback sequence: 1. Anchor href, 2. Row dataset, 3. Checkbox dataset
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

/**
 * Initializes the bulk action logic once the DOM is ready.
 */
document.addEventListener("DOMContentLoaded", () => {
	// Cache action buttons once to improve performance during frequent checkbox changes
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

	// Stop initialization if no action buttons are found on the current page
	if (!deleteBtn && !editBtn && !activationBtn && !deactivationBtn) return;

	const names = getCheckboxNames();

	/**
	 * Orchestrates UI updates: toggles visibility and updates button attributes.
	 */
	function syncButtons(): void {
		const count = getCheckedCount(names);
		const isSingle: boolean = count === 1;
		const data = isSingle ? getSelectedRowData(names) : null;

		// "Delete" Action: Requires at least one selection
		deleteBtn?.classList.toggle(BULK_ACTION_CLASSES.hidden, count === 0);

		// "Edit" Action: Strictly requires exactly one selection
		if (editBtn) {
			editBtn.classList.toggle(BULK_ACTION_CLASSES.hidden, !isSingle);

			if (isSingle && data) {
				if (editBtn.dataset) {
					editBtn.dataset.id = data.id;
					editBtn.dataset.url = data.url;
					editBtn.dataset.name = data.name;
				}
			} else if (editBtn.dataset) {
				// Clear metadata when no longer in a valid state
				editBtn.dataset.id = "";
				editBtn.dataset.url = "";
				editBtn.dataset.name = "";
			}
		}

		// "Activation/Deactivation" Logic: Independent state-based visibility
		const shouldShowActivate = !!(isSingle && data && data.is_active === false);
		const shouldShowDeactivate = !!(
			isSingle &&
			data &&
			data.is_active === true
		);

		// Handle Activation Button state
		if (activationBtn) {
			activationBtn.classList.toggle(
				BULK_ACTION_CLASSES.hidden,
				!shouldShowActivate,
			);
			if (shouldShowActivate && data) {
				activationBtn.href =
					data.activate_url || BULK_ACTION_FALLBACKS.defaultHref;
				if (activationBtn.dataset) {
					activationBtn.dataset.id = data.id;
					activationBtn.dataset.name = data.name;
				}
			} else {
				activationBtn.href = "";
				if (activationBtn.dataset) {
					activationBtn.dataset.id = "";
					activationBtn.dataset.name = "";
				}
			}
		}

		// Handle Deactivation Button state
		if (deactivationBtn) {
			deactivationBtn.classList.toggle(
				BULK_ACTION_CLASSES.hidden,
				!shouldShowDeactivate,
			);
			if (shouldShowDeactivate && data) {
				deactivationBtn.href =
					data.deactivate_url || BULK_ACTION_FALLBACKS.defaultHref;
				if (deactivationBtn.dataset) {
					deactivationBtn.dataset.id = data.id;
					deactivationBtn.dataset.name = data.name;
				}
			} else {
				deactivationBtn.href = "";
				if (deactivationBtn.dataset) {
					deactivationBtn.dataset.id = "";
					deactivationBtn.dataset.name = "";
				}
			}
		}
	}

	/**
	 * Global event listener using delegation to track checkbox state changes.
	 */
	document.addEventListener("change", (e) => {
		const target = e.target;
		if (!(target instanceof HTMLInputElement)) return;
		if (target.dataset.checkboxName || target.dataset.rowCheckboxName) {
			syncButtons();
		}
	});

	// Initial sync to account for browser autofill or page refreshes
	syncButtons();
});

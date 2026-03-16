/**
 * Select-all logic (TypeScript, strict).
 * Manages master-slave checkbox relationships with indeterminate state support.
 * Integrates with table filtering by only affecting visible rows.
 */

const SELECT_ALL_SELECTORS = {
	selectAll: 'input[type="checkbox"][data-checkbox-name]',
	groupCheckbox: 'input[type="checkbox"][data-row-checkbox-name]',
} as const;

const SELECT_ALL_TYPES = {
	checkboxType: "checkbox",
} as const;

/** Helper to find row checkboxes by their group name */
function getGroupCheckboxSelector(name: string): string {
	return `${SELECT_ALL_SELECTORS.groupCheckbox}[data-row-checkbox-name="${name}"]`;
}

/** Helper to find the master checkbox by its group name */
function getSelectAllCheckboxSelector(name: string): string {
	return `${SELECT_ALL_SELECTORS.selectAll}[data-checkbox-name="${name}"]`;
}

/** Converts NodeList of checkboxes to an array for easier filtering/mapping */
function resolveCheckboxesByData(name: string): HTMLInputElement[] {
	return Array.from(
		document.querySelectorAll<HTMLInputElement>(getGroupCheckboxSelector(name)),
	);
}

/**
 * Toggles all visible row checkboxes based on the master checkbox state.
 * Triggers 'change' events to ensure other modules (Summary, Bulk Delete) stay in sync.
 */
export function toggleAllVisible(
	source: HTMLInputElement | { checked?: boolean } | null,
	name: string | null | undefined,
): void {
	if (!name) return;
	const checkboxList = resolveCheckboxesByData(name);

	if (checkboxList.length === 0) return;
	const shouldCheck = !!(source && (source as { checked?: boolean }).checked);

	if (source instanceof HTMLInputElement) {
		source.indeterminate = false;
	}

	for (const checkbox of checkboxList) {
		// Only toggle visible checkboxes (respecting active table filters)
		if (
			checkbox instanceof HTMLInputElement &&
			checkbox.type === SELECT_ALL_TYPES.checkboxType &&
			checkbox.offsetParent !== null
		) {
			checkbox.checked = shouldCheck;
			// Bubbling event allows delegation listeners in other scripts to react
			checkbox.dispatchEvent(new Event("change", { bubbles: true }));
		}
	}
}

/**
 * Re-evaluates the master checkbox state (Checked, Unchecked, or Indeterminate)
 * based on the current selection of visible row checkboxes.
 */
function refreshAllCheckbox(selectAll: HTMLInputElement): void {
	const name = selectAll.dataset.checkboxName;
	if (!name) return;

	const checkboxes = resolveCheckboxesByData(name);

	const visible = checkboxes.filter(
		(checkbox) => checkbox.offsetParent !== null,
	);

	const checked = visible.filter((checkbox) => checkbox.checked);

	if (checked.length === 0) {
		selectAll.checked = false;
		selectAll.indeterminate = false;
	} else if (checked.length === visible.length) {
		selectAll.checked = true;
		selectAll.indeterminate = false;
	} else {
		selectAll.checked = false;
		selectAll.indeterminate = true;
	}
}

document.addEventListener("DOMContentLoaded", () => {
	// Initial sync of all master checkboxes on page load
	for (const cb of document.querySelectorAll<HTMLInputElement>(
		SELECT_ALL_SELECTORS.selectAll,
	)) {
		refreshAllCheckbox(cb);
	}

	/**
	 * Unified event delegation for all checkbox interactions.
	 */
	document.addEventListener("change", (event) => {
		const target = event.target as HTMLInputElement | null;
		if (!target || target.type !== SELECT_ALL_TYPES.checkboxType) return;

		// Case: Master checkbox was clicked
		if (target.dataset.checkboxName) {
			toggleAllVisible(target, target.dataset.checkboxName);
			refreshAllCheckbox(target);
			return;
		}

		// Case: Individual row checkbox was clicked
		const groupName = target.dataset.rowCheckboxName;
		if (groupName) {
			const selectAll = document.querySelector<HTMLInputElement>(
				getSelectAllCheckboxSelector(groupName),
			);
			if (selectAll) refreshAllCheckbox(selectAll);
		}
	});
});

/**
 * Mobile details toggle logic (TypeScript, strict).
 * Dynamically expands/collapses metadata blocks within table rows using CSS Grid transitions.
 */

const MOBILE_DETAILS_SELECTORS = {
	mobileMeta: "[data-mobile-meta]",
	rowCheckbox: "input[data-row-checkbox-name]",
} as const;

/** * Utility classes for CSS Grid fractional row animation.
 * Requires: .grid { display: grid; transition: grid-template-rows 0.3s; }
 */
const MOBILE_DETAILS_CLASSES = {
	gridRowsZero: "grid-rows-[0fr]",
	gridRowsOne: "grid-rows-[1fr]",
} as const;

const MOBILE_DETAILS_TAGS = {
	tableRow: "tr",
} as const;

document.addEventListener("DOMContentLoaded", () => {
	/**
	 * Synchronizes the visibility of a row's metadata block with its checkbox state.
	 */
	const syncRowMeta = (checkbox: HTMLInputElement): void => {
		const row = checkbox.closest(MOBILE_DETAILS_TAGS.tableRow);
		if (!row) return;

		const meta = row.querySelector<HTMLElement>(
			MOBILE_DETAILS_SELECTORS.mobileMeta,
		);
		if (!meta) return;

		// Toggle grid height classes based on checked stacheckboxtus
		meta.classList.toggle(MOBILE_DETAILS_CLASSES.gridRowsOne, checkbox.checked);
		meta.classList.toggle(MOBILE_DETAILS_CLASSES.gridRowsZero, !checkbox.checked);
	};

	// Initial sync for all checkboxes on page load
	for (const checkboxEl of document.querySelectorAll<HTMLInputElement>(
		MOBILE_DETAILS_SELECTORS.rowCheckbox,
	)) {
		syncRowMeta(checkboxEl);
	}

	/**
	 * Event delegation for performance and support for dynamically added rows.
	 */
	document.addEventListener("change", (event: Event) => {
		const target = event.target;
		if (!(target instanceof HTMLInputElement)) return;
		if (target.dataset.rowCheckboxName) {
			syncRowMeta(target);
		}
	});
});

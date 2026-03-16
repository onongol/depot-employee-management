/**
 * Summary selection logic (TypeScript, strict, modular).
 * Dynamically links summary blocks to checkbox groups via data-attributes.
 */

type SummaryConfig = {
	allText?: string;
	getLabel: (checkbox: HTMLInputElement) => string;
};

const SUMMARY_SELECTORS = {
	summaryId: "[data-summary-id]",
	summaryList: "[data-summary-list]",
	summaryCount: "[data-summary-count]",
	summaryLabel: "[data-summary-label]",
	summaryDetails: "[data-summary-details]",
} as const;

const SUMMARY_CLASSES = {
	hidden: "hidden",
} as const;

const SUMMARY_ATTRS = {
	origLabel: "origLabel",
	toggleGuardAdded: "toggleGuardAdded",
	preventOpen: "preventOpen",
} as const;

const SUMMARY_TAGS = {
	summaryTag: "summary",
	svgTag: "svg",
	tableRow: "tr",
} as const;

const SUMMARY_DISPLAY = {
	displayNone: "none",
	pointerNone: "none",
} as const;

const SUMMARY_TEXT = {
	textSelected: "selected",
} as const;

const SUMMARY_FLAGS = {
	toggleGuardAdded: "true",
	preventOpenTrue: "true",
	preventOpenFalse: "false",
} as const;

function getRowCheckboxSelector(checkboxName: string): string {
	return `[data-row-checkbox-name="${checkboxName}"]`;
}

function getAllCheckboxSelector(checkboxName: string): string {
	return `[data-checkbox-name="${checkboxName}"]`;
}

/**
 * Updates a specific summary block.
 * Encapsulates UI logic for labels, counts, and the 'All Selected' state.
 */
const labelFactories: Record<string, (checkbox: HTMLInputElement) => string> = {
	employee_ids: (checkbox) => {
		const row = checkbox.closest(SUMMARY_TAGS.tableRow);
		if (!row) return "";
		const id = (row.dataset.empId ?? "").trim();
		const name = (row.dataset.empName ?? "").trim();
		return id && name ? `(ID: ${id}) ${name}` : id || name;
	},
	work_ids: (checkbox) => {
		const row = checkbox.closest(SUMMARY_TAGS.tableRow);
		if (!row) return "";
		const workName = (row.dataset.workName ?? "").trim();
		return workName;
	},
	daily_salary_ids: (checkbox) => {
		const row = checkbox.closest(SUMMARY_TAGS.tableRow);
		if (!row) return "";
		const id = (row.dataset.empId ?? "").trim();
		const name = (row.dataset.empName ?? "").trim();
		const date = (row.dataset.salaryDate ?? "").trim();
		return `(ID: ${id}) ${name} - ${date}`;
	},
	daily_work_ids: (checkbox) => {
		const row = checkbox.closest(SUMMARY_TAGS.tableRow);
		if (!row) return "";
		const work = (row.dataset.workName ?? "").trim();
		const type = (row.dataset.typeWork ?? "").trim();
		const date = (row.dataset.workDate ?? "").trim();
		return `${work} (${type}) - ${date}`;
	},
};

/**
 * Updates a specific summary block.
 * Encapsulates UI logic for labels, counts, and the 'All Selected' state.
 */
export function updateGenericSummary(
	config: SummaryConfig,
	summaryBox: HTMLElement,
): void {
	const checkboxName = summaryBox.dataset.summaryCheckboxName ?? "";

	// Find all related row checkboxes
	const checkboxes = Array.from(
		document.querySelectorAll<HTMLInputElement>(
			getRowCheckboxSelector(checkboxName),
		),
	);
	const checked = checkboxes.filter((checkbox) => checkbox.checked);

	// Contextual search within the specific summaryBox
	const summaryList = summaryBox.querySelector<HTMLElement>(
		SUMMARY_SELECTORS.summaryList,
	);
	const countEl = summaryBox.querySelector<HTMLElement>(
		SUMMARY_SELECTORS.summaryCount,
	);
	const labelSpan = summaryBox.querySelector<HTMLElement>(
		SUMMARY_SELECTORS.summaryLabel,
	);
	const detailsEl = summaryBox.querySelector<HTMLDetailsElement>(
		SUMMARY_SELECTORS.summaryDetails,
	);

	const summaryToggle = detailsEl?.querySelector(SUMMARY_TAGS.summaryTag);
	const chevron = summaryToggle?.querySelector(SUMMARY_TAGS.svgTag);

	// Global check for the "Select All" master checkbox
	const selectAll = document.querySelector<HTMLInputElement>(
		getAllCheckboxSelector(checkboxName),
	);

	const allText = summaryBox.dataset.allText ?? config.allText ?? "";
	const selectedText =
		summaryBox.dataset.selectedText ?? SUMMARY_TEXT.textSelected;

	const allSelected =
		!!selectAll &&
		checkboxes.length > 0 &&
		selectAll.checked &&
		checked.length === checkboxes.length;

	// Determine the summary text display
	let text = "";
	if (allSelected) {
		text = `${allText} ${checked.length} ${selectedText}`.trim();
	} else if (checked.length > 0) {
		text = checked
			.map((checkbox) => config.getLabel(checkbox))
			.filter(Boolean)
			.join(", ");
	}

	// Sync UI elements
	if (summaryList) summaryList.textContent = text;
	if (countEl) {
		countEl.style.display = allSelected ? SUMMARY_DISPLAY.displayNone : "";
		countEl.textContent = allSelected ? "" : String(checked.length);
	}

	// Handle Label and Original Label persistence
	if (labelSpan) {
		if (labelSpan.dataset[SUMMARY_ATTRS.origLabel] === undefined) {
			labelSpan.dataset[SUMMARY_ATTRS.origLabel] = labelSpan.textContent ?? "";
		}
		labelSpan.textContent = allSelected
			? `${allText} ${checked.length} ${selectedText}`.trim()
			: (labelSpan.dataset[SUMMARY_ATTRS.origLabel] ?? selectedText);
	}

	// Update Details disclosure element and prevent interaction when 'All Selected'
	if (detailsEl) {
		if (!detailsEl.dataset[SUMMARY_ATTRS.toggleGuardAdded]) {
			detailsEl.addEventListener("toggle", () => {
				if (
					detailsEl.dataset[SUMMARY_ATTRS.preventOpen] ===
					SUMMARY_FLAGS.preventOpenTrue
				) {
					detailsEl.open = false;
				}
			});
			detailsEl.dataset[SUMMARY_ATTRS.toggleGuardAdded] =
				SUMMARY_FLAGS.toggleGuardAdded;
		}
		if (allSelected) {
			detailsEl.open = false;
			detailsEl.dataset[SUMMARY_ATTRS.preventOpen] =
				SUMMARY_FLAGS.preventOpenTrue;
			if (summaryToggle)
				summaryToggle.style.pointerEvents = SUMMARY_DISPLAY.pointerNone;
			if (chevron) chevron.classList.add(SUMMARY_CLASSES.hidden);
		} else {
			detailsEl.dataset[SUMMARY_ATTRS.preventOpen] =
				SUMMARY_FLAGS.preventOpenFalse;
			if (summaryToggle) summaryToggle.style.pointerEvents = "";
			if (chevron) chevron.classList.remove(SUMMARY_CLASSES.hidden);
		}
	}

	// Show/Hide the entire summary box
	if (checked.length > 0) {
		summaryBox.classList.remove(SUMMARY_CLASSES.hidden);
		summaryBox.style.display = "";
	} else {
		summaryBox.classList.add(SUMMARY_CLASSES.hidden);
		summaryBox.style.display = SUMMARY_DISPLAY.displayNone;
	}
}

/** Initializes event handlers for all summary boxes */
function initSummaryHandlers(
	labelFactories: Record<string, (checkbox: HTMLInputElement) => string>,
): void {
	document.addEventListener("change", (event: Event) => {
		const target = event.target;
		if (!(target instanceof HTMLInputElement)) return;

		document
			.querySelectorAll<HTMLElement>(SUMMARY_SELECTORS.summaryId)
			.forEach((box) => {
				const checkboxName = box.dataset.summaryCheckboxName ?? "";
				if (
					target.name !== checkboxName &&
					target.dataset.rowCheckboxName !== checkboxName
				)
					return;
				const getLabel = labelFactories[checkboxName] ?? (() => "");
				const config: SummaryConfig = { getLabel };
				updateGenericSummary(config, box);
			});
	});
}

/** Initializes summaries on DOMContentLoaded */
document.addEventListener("DOMContentLoaded", () => {
	document
		.querySelectorAll<HTMLElement>(SUMMARY_SELECTORS.summaryId)
		.forEach((box) => {
			const checkboxName = box.dataset.summaryCheckboxName ?? "";
			if (!checkboxName) return;

			const getLabel = labelFactories[checkboxName] ?? (() => "");
			const config: SummaryConfig = { getLabel };

			updateGenericSummary(config, box);
		});

	initSummaryHandlers(labelFactories);
});

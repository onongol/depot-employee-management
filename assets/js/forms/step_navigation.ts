/**
 * Step Navigation Component:
 * Manages a multi-step form process with integrated validation for checkbox selection.
 * Uses data-attributes for flexible DOM decoupling.
 */
const STEP_NAV_IDS = {
	form: "createForm",
	errorId: "employee_ids-selection-error",
} as const;

const STEP_NAV_SELECTORS = {
	step1: '[data-step="1"]',
	step2: '[data-step="2"]',
	nextBtn: '[data-step-action="next"]',
	backBtns: '[data-step-action="back"]',
	mobileBackBtns: '[data-mobile-step-action="back"]',
	stepFrom2: '[data-step-from="2"]',
	validationEl:
		'[data-checkbox-validation="true"][data-checkbox-name="employee_ids"]',
	defaultTable: ".employee-table-container",
	checkedEmployees: 'input[name="employee_ids"]:checked',
	filterJobTitle: 'tbody[data-table-role="filter-job-title"]',
} as const;

const STEP_NAV_ATTRS = {
	tableSelector: "data-table-selector",
	errorMessage: "data-error-message",
	jobTitle: "data-job-title",
} as const;

const STEP_NAV_MESSAGES = {
	selectAtLeastOneEmployee: "Select at least one employee.",
} as const;

const STEP_NAV_CLASSES = {
	hidden: "hidden",
	tableError: ["border-red-500", "dark:border-red-500"],
	errorText: "text-red-500 text-sm",
} as const;

const STEP_NAV_SCROLL = {
	behavior: "smooth" as ScrollBehavior,
	block: "start" as ScrollLogicalPosition,
} as const;

const STEP_NAV_TAGS = {
	div: "div",
} as const;

document.addEventListener("DOMContentLoaded", () => {
	// Select primary step containers
	const step1 = document.querySelector<HTMLElement>(STEP_NAV_SELECTORS.step1);
	const step2 = document.querySelector<HTMLElement>(STEP_NAV_SELECTORS.step2);

	// Collect navigation buttons
	const nextBtn = document.querySelector<HTMLButtonElement>(
		STEP_NAV_SELECTORS.nextBtn,
	);
	const backBtns = Array.from(
		document.querySelectorAll<HTMLButtonElement>(STEP_NAV_SELECTORS.backBtns),
	);

	const formEl = document.getElementById(STEP_NAV_IDS.form);
	if (!(formEl instanceof HTMLFormElement)) return;
	const form = formEl;

	/**
	 * Toggles visibility between Step 1 and Step 2 containers.
	 */
	const setStep = (step: 1 | 2): void => {
		if (!step1 || !step2) return;

		const isStep1 = step === 1;
		step1.classList.toggle(STEP_NAV_CLASSES.hidden, !isStep1);
		step2.classList.toggle(STEP_NAV_CLASSES.hidden, isStep1);

		// Toggle mobile back button visibility based on the current step
		const mobileBackBtns = document.querySelectorAll<HTMLButtonElement>(
			STEP_NAV_SELECTORS.mobileBackBtns,
		);
		mobileBackBtns.forEach((btn) => {
			btn.classList.toggle(STEP_NAV_CLASSES.hidden, isStep1);
		});
	};

	// Extract dynamic validation configuration from the DOM
	const validationEl = document.querySelector<HTMLElement>(
		STEP_NAV_SELECTORS.validationEl,
	);

	const tableSelector =
		validationEl?.getAttribute(STEP_NAV_ATTRS.tableSelector) ||
		STEP_NAV_SELECTORS.defaultTable;
	const errorMessage =
		validationEl?.getAttribute(STEP_NAV_ATTRS.errorMessage) ||
		STEP_NAV_MESSAGES.selectAtLeastOneEmployee;

	// Cache table container once (DOM is static for this form)
	const tableDiv =
		form.querySelector<HTMLElement>(tableSelector) ??
		document.querySelector<HTMLElement>(tableSelector);

	/**
	 * Injects validation error UI when the user fails to select at least one item.
	 */
	const showSelectionError = (container: Element | null): void => {
		if (!container) return;

		container.classList.add(...STEP_NAV_CLASSES.tableError);

		let errorDiv = document.getElementById(STEP_NAV_IDS.errorId);
		if (!errorDiv) {
			errorDiv = document.createElement(STEP_NAV_TAGS.div);
			errorDiv.id = STEP_NAV_IDS.errorId;
			errorDiv.className = STEP_NAV_CLASSES.errorText;
			errorDiv.textContent = errorMessage;

			// Inserts the error message directly after the table container
			const parent = container.parentNode;
			if (parent) {
				if (container.nextSibling) {
					parent.insertBefore(errorDiv, container.nextSibling);
				} else {
					parent.appendChild(errorDiv);
				}
			}
		}
	};

	/**
	 * Clears validation UI highlights and removes error messages.
	 */
	const hideSelectionError = (container: Element | null): void => {
		if (!container) return;

		container.classList.remove(...STEP_NAV_CLASSES.tableError);
		const errorDiv = document.getElementById(STEP_NAV_IDS.errorId);
		if (errorDiv) errorDiv.remove();
	};

	/**
	 * Handles progression back to Step 1.
	 */
	const goStep1 = (): void => {
		if (!step1 || !step2) return;
		setStep(1);
		step1.scrollIntoView(STEP_NAV_SCROLL);
	};

	/**
	 * Handles progression to Step 2.
	 * Validates employee selection before allowing the transition.
	 * Filters works table by job titles of selected employees.
	 */
	const goStep2 = (): void => {
		if (!step1 || !step2) return;

		const checked = form.querySelectorAll<HTMLInputElement>(
			STEP_NAV_SELECTORS.checkedEmployees,
		);

		if (checked.length === 0) {
			showSelectionError(tableDiv);
			return;
		}

		// 1. Collect Job Titles from selected employees for filtering
		const selectedJobTitles = new Set(
			Array.from(checked)
				.map((el) => el.getAttribute(STEP_NAV_ATTRS.jobTitle))
				.filter((jt): jt is string => Boolean(jt)),
		);

		// 2. Filter the "Works" table rows based on collected job titles
		const worksTableBody = document.querySelector(
			STEP_NAV_SELECTORS.filterJobTitle,
		);
		if (worksTableBody instanceof HTMLTableSectionElement) {
			for (const row of Array.from(worksTableBody.rows)) {
				// Find cell with data-job-title to determine visibility
				const jobTitleCell = row.querySelector(`[${STEP_NAV_ATTRS.jobTitle}]`);
				const workJobTitle =
					jobTitleCell?.getAttribute(STEP_NAV_ATTRS.jobTitle) || "";

				const isVisible =
					selectedJobTitles.size === 0 || selectedJobTitles.has(workJobTitle);
				row.classList.toggle(STEP_NAV_CLASSES.hidden, !isVisible);
			}
		}

		hideSelectionError(tableDiv);
		setStep(2);
		step2.scrollIntoView(STEP_NAV_SCROLL);
	};

	// Event Bindings
	if (nextBtn) {
		nextBtn.addEventListener("click", (event: MouseEvent) => {
			event.preventDefault();
			goStep2();
		});
	}

	backBtns.forEach((btn) => {
		btn.addEventListener("click", (event: MouseEvent) => {
			event.preventDefault();
			goStep1();
		});
	});

	// Initialize the view at the first step
	setStep(1);
});

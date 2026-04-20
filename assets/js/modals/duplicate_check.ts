/**
 * Prevent duplicate piecework entries on create:
 * - strict types, no `any`
 * - safer DOM access and early returns
 * - normalized wagon comparison and resilient JSON parsing
 */

type ExistingPiecework = {
	employee_code: number | string;
	work_id: number | string;
	type_work: string;
	work_date: string;
	wagon_number?: string | null;
};

const DUPLICATE_ATTRS = {
	workName: "data-work-name",
	empId: "data-emp-id",
	empName: "data-emp-name",
} as const;

const DUPLICATE_SELECTORS = {
	existingScript: "existing-pieceworks",
	form: "createForm",
	modal: "saveDuplicateModal",
	modalCancel: "[data-modal-cancel]",
	employeeCheckbox: 'input[name="employee_ids"]:checked',
	workCheckbox: 'input[name="work_ids"]:checked',
	workDate: "work_date",
	wagonNumber: "wagon_number",
} as const;

const DUPLICATE_TAGS = {
	tableRow: "tr",
} as const;

const DUPLICATE_CLASSES = {
	hidden: "hidden",
	lockScroll: "overflow-hidden",
} as const;

const DUPLICATE_ELEMENTS = {
	amountError: "amount-error",
	elIdTypeWork: "id_type_work",
	detailEmployee: "duplicateDetailEmployee",
	detailWork: "duplicateDetailWork",
	detailTypeWork: "duplicateDetailTypeWork",
	detailWagonNumber: "duplicateDetailWagonNumber",
	detailWorkDate: "duplicateDetailWorkDate",
} as const;

const DUPLICATE_KEYS = {
	esc: "Escape",
} as const;

const DUPLICATE_TEXT = {
	emptyWagonNumber: "-",
	unknownEmployee: "Unknown",
} as const;

const DUPLICATE_SCROLL = {
	behavior: "smooth" as ScrollBehavior,
	block: "center" as ScrollLogicalPosition,
} as const;

/* Helper Functions */
const getDuplicateById = (id: string): HTMLElement | null =>
	document.getElementById(id);

/**
 * Ensures wagon numbers are compared as null if they are empty strings or whitespace.
 */
function normalizeWagon(val: unknown): string | null {
	if (val === null || val === undefined) return null;
	const valueStr = String(val).trim();
	return valueStr === "" ? null : valueStr;
}

/**
 * Formats employee display as "(ID: 123) John Doe" if name is available, otherwise just "123".
 */
function formatEmployeeDisplay(id: string, name: string | null): string {
	if (!id) return name ?? DUPLICATE_TEXT.unknownEmployee;
	return name ? `(ID: ${id}) ${name}` : id;
}

/**
 * Extracts and parses the JSON data injected by Django into a script tag.
 */
function parseExistingPieceworks(): ExistingPiecework[] {
	const scriptEl = getDuplicateById(
		DUPLICATE_SELECTORS.existingScript,
	) as HTMLScriptElement | null;
	if (!scriptEl || !scriptEl.textContent) return [];
	try {
		return JSON.parse(scriptEl.textContent) as ExistingPiecework[];
	} catch {
		return [];
	}
}

/**
 * Displays the modal and prevents background scrolling.
 */
function openDuplicateModal(modal: HTMLElement) {
	modal.classList.remove(DUPLICATE_CLASSES.hidden);
	document.body.classList.add(DUPLICATE_CLASSES.lockScroll);
}

/**
 * Hides the modal and restores background scrolling.
 */
function closeDuplicateModal(modal: HTMLElement) {
	modal.classList.add(DUPLICATE_CLASSES.hidden);
	document.body.classList.remove(DUPLICATE_CLASSES.lockScroll);
}

function setDuplicateText(id: string, text: string) {
	const textEl = getDuplicateById(id);
	if (textEl) textEl.textContent = text;
}

/**
 * Creates a unique key
 */
function makeDuplicateKey(
	keyEmpID: string,
	keyWorkID: string,
	keyTypeWork: string,
	keyWorkDate: string,
	keyWagonNumber: string | null,
): string {
	return `${keyEmpID}::${keyWorkID}::${keyTypeWork}::${keyWorkDate}::${keyWagonNumber ?? ""}`;
}

/**
 * Generates a unique key
 */
function makeDuplicateKeyFrom(pw: ExistingPiecework): string {
	const wagon = normalizeWagon(pw.wagon_number);
	return makeDuplicateKey(
		String(pw.employee_code),
		String(pw.work_id),
		pw.type_work,
		pw.work_date,
		wagon,
	);
}

/* Initialization */
document.addEventListener("DOMContentLoaded", () => {
	const existingPieceworks = parseExistingPieceworks();

	const existingSet = new Set<string>(
		existingPieceworks.map(makeDuplicateKeyFrom),
	);

	const form = getDuplicateById(
		DUPLICATE_SELECTORS.form,
	) as HTMLFormElement | null;
	const modalDiv = getDuplicateById(DUPLICATE_SELECTORS.modal);

	if (!form) return;

	/* Set up cancel buttons inside the modal */
	const cancelBtns: HTMLElement[] = modalDiv
		? Array.from(
				modalDiv.querySelectorAll<HTMLElement>(DUPLICATE_SELECTORS.modalCancel),
			)
		: [];

	/**
	 * Close modal on cancel button click
	 */
	cancelBtns.forEach((btn) => {
		btn.addEventListener("click", (event) => {
			event.preventDefault();
			if (modalDiv) closeDuplicateModal(modalDiv);
		});
	});

	/**
	 * Close modal on Escape
	 */
	document.addEventListener("keydown", (event: KeyboardEvent) => {
		if (event.key !== DUPLICATE_KEYS.esc || !modalDiv) return;
		if (!modalDiv.classList.contains(DUPLICATE_CLASSES.hidden))
			closeDuplicateModal(modalDiv);
	});

	/**
	 * Core validation logic triggered on form submission.
	 */
	form.addEventListener("submit", (event) => {
		// Stop check if UI already shows an 'Amount' validation error (prevents multiple error types at once)
		const amountErrorEl = document.getElementById(
			DUPLICATE_ELEMENTS.amountError,
		);
		if (amountErrorEl) {
			event.preventDefault();
			amountErrorEl.scrollIntoView(DUPLICATE_SCROLL);
			return;
		}

		// Gather selected employee and work IDs from the form checkboxes
		const employeeCheckboxes = Array.from(
			document.querySelectorAll<HTMLInputElement>(
				DUPLICATE_SELECTORS.employeeCheckbox,
			),
		);
		const workCheckboxes = Array.from(
			document.querySelectorAll<HTMLInputElement>(
				DUPLICATE_SELECTORS.workCheckbox,
			),
		);

		const selectedEmployeeIds = employeeCheckboxes.map(
			(checkbox) => checkbox.value,
		);
		const selectedWorkIds = workCheckboxes.map((checkbox) => checkbox.value);

		// Find the work type field using multiple possible ID/Name variations generated by Django
		const typeWorkEl = getDuplicateById(DUPLICATE_ELEMENTS.elIdTypeWork) as
			| HTMLInputElement
			| HTMLSelectElement
			| null;
		if (!typeWorkEl) return;

		const workDateEl = getDuplicateById(
			DUPLICATE_SELECTORS.workDate,
		) as HTMLInputElement | null;
		if (!workDateEl) return;

		const wagonNumberInput = getDuplicateById(
			DUPLICATE_SELECTORS.wagonNumber,
		) as HTMLInputElement | null;

		const typeWork = typeWorkEl.value;
		const workDate = workDateEl.value;
		const wagonNumber = normalizeWagon(wagonNumberInput?.value);

		// Basic exit if selections are missing
		if (selectedEmployeeIds.length === 0 || selectedWorkIds.length === 0)
			return;

		// Compare every selected Employee + Work combination against existing records
		const duplicatePairs: Array<{ empId: string; workId: string }> = [];

		selectedEmployeeIds.forEach((empId) => {
			selectedWorkIds.forEach((workId) => {
				const exists = existingSet.has(
					makeDuplicateKey(empId, workId, typeWork, workDate, wagonNumber),
				);
				if (exists)
					duplicatePairs.push({ empId: String(empId), workId: String(workId) });
			});
		});

		// Proceed with standard submission if no duplicates were found
		if (duplicatePairs.length === 0) return;

		// Duplicates found: Prevent submission and prepare modal data
		event.preventDefault();
		if (!modalDiv) return;

		// Unique sets for faster filtering of names
		const duplicateEmpIds = new Set(
			duplicatePairs.map((piecework) => piecework.empId),
		);
		const duplicateWorkIds = new Set(
			duplicatePairs.map((piecework) => piecework.workId),
		);

		// Resolve employee names/IDs from table attributes for the error summary
		const selectedEmployees = employeeCheckboxes
			.filter((checkbox) => duplicateEmpIds.has(String(checkbox.value)))
			.map((checkbox) => {
				const tr = checkbox.closest(DUPLICATE_TAGS.tableRow);
				const id = (
					tr?.getAttribute(DUPLICATE_ATTRS.empId) ??
					checkbox.value ??
					""
				).trim();
				const name = (tr?.getAttribute(DUPLICATE_ATTRS.empName) ?? "").trim();
				return formatEmployeeDisplay(id, name);
			});

		// Resolve work names from data-attributes for the error summary
		const selectedWorks = Array.from(
			new Set(
				workCheckboxes
					.filter((checkbox) => duplicateWorkIds.has(String(checkbox.value)))
					.map((checkbox) => {
						const tr = checkbox.closest(DUPLICATE_TAGS.tableRow);
						return (
							checkbox.getAttribute(DUPLICATE_ATTRS.workName)?.trim() ||
							tr?.getAttribute(DUPLICATE_ATTRS.workName)?.trim() ||
							""
						);
					})
					.filter(Boolean),
			),
		);

		// Populate the modal with details about why the submission was blocked
		setDuplicateText(
			DUPLICATE_ELEMENTS.detailEmployee,
			selectedEmployees.join(", "),
		);
		setDuplicateText(DUPLICATE_ELEMENTS.detailWork, selectedWorks.join(", "));
		setDuplicateText(DUPLICATE_ELEMENTS.detailTypeWork, typeWork);
		setDuplicateText(
			DUPLICATE_ELEMENTS.detailWagonNumber,
			wagonNumber ?? DUPLICATE_TEXT.emptyWagonNumber,
		);
		setDuplicateText(DUPLICATE_ELEMENTS.detailWorkDate, workDate);

		openDuplicateModal(modalDiv);
	});
});

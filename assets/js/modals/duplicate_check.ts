/**
 * Shared duplicate check utilities.
 * Used by both Daily Salary and Piecework duplicate detection.
 */

export type ExistingDailySalary = {
	employee_code: number | string;
	salary_date: string;
};

export type ExistingPiecework = {
	employee_code: number | string;
	work_id: number | string;
	type_work: string;
	work_date: string;
	wagon_number?: string | null;
};

export const DUPLICATE_CLASSES = {
	hidden: "hidden",
	lockScroll: "overflow-hidden",
} as const;

export const DUPLICATE_TAGS = {
	tableRow: "tr",
} as const;

export const DUPLICATE_KEYS = {
	esc: "Escape",
} as const;

export const DUPLICATE_TEXT = {
	unknownEmployee: "Unknown",
	emptyWagonNumber: "-",
} as const;

export const DUPLICATE_SCROLL = {
	behavior: "smooth" as ScrollBehavior,
	block: "center" as ScrollLogicalPosition,
} as const;

/* -- Helper Functions -- */

/**
 * Utility to get an element by ID with proper typing.
 */
export function getDuplicateById(id: string): HTMLElement | null {
	return document.getElementById(id);
}

/**
 * Formats employee display as "(ID: 123) John Doe" if name is available, otherwise just "123".
 */
export function formatEmployeeDisplay(id: string, name: string | null): string {
	if (!id) return name ?? DUPLICATE_TEXT.unknownEmployee;
	return name ? `(ID: ${id}) ${name}` : id;
}

/**
 * Extracts and parses the JSON data injected by Django into a script tag.
 */
export function parseJsonScript<T>(scriptId: string): T[] {
	const scriptEl = getDuplicateById(scriptId) as HTMLScriptElement | null;
	if (!scriptEl?.textContent) return [];
	try {
		return JSON.parse(scriptEl.textContent) as T[];
	} catch {
		return [];
	}
}

/**
 * Displays the modal and prevents background scrolling.
 */
export function openDuplicateModal(modal: HTMLElement): void {
	modal.classList.remove(DUPLICATE_CLASSES.hidden);
	document.body.classList.add(DUPLICATE_CLASSES.lockScroll);
}

/**
 * Hides the modal and restores background scrolling.
 */
export function closeDuplicateModal(modal: HTMLElement): void {
	modal.classList.add(DUPLICATE_CLASSES.hidden);
	document.body.classList.remove(DUPLICATE_CLASSES.lockScroll);
}

/**
 * Sets the text content of an element by ID if it exists.
 */
export function setDuplicateText(id: string, text: string): void {
	const textEl = getDuplicateById(id);
	if (textEl) textEl.textContent = text;
}

/**
 * Normalizes a wagon value by trimming and converting empty strings to null.
 */
export function normalizeWagon(val: unknown): string | null {
	if (val === null || val === undefined) return null;
	const valueStr = String(val).trim();
	return valueStr === "" ? null : valueStr;
}

/**
 * Sets up modal cancel buttons and Escape key handler.
 */
export function setupDuplicateModalClose(
	modalDiv: HTMLElement,
	cancelSelector: string,
	escKey: string = DUPLICATE_KEYS.esc,
): void {
	for (const btn of modalDiv.querySelectorAll<HTMLElement>(cancelSelector)) {
		btn.addEventListener("click", (event) => {
			event.preventDefault();
			closeDuplicateModal(modalDiv);
		});
	}
	document.addEventListener("keydown", (event: KeyboardEvent) => {
		if (event.key !== escKey) return;
		if (!modalDiv.classList.contains(DUPLICATE_CLASSES.hidden)) {
			closeDuplicateModal(modalDiv);
		}
	});
}

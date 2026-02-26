/**
 * Validates checkbox selection in tables: shows/removes error messages and red border on submit/change,
 * preventing form submission when no checkboxes are checked.
 */

type Maybe<T> = T | null;

interface ValidationConfig {
	formId: string;
	checkboxName: string;
	tableSelector: string;
	errorMessage: string;
}

function getEl<T extends Element = Element>(
	selector: string,
	ctx: ParentNode = document,
): Maybe<T> {
	return (ctx.querySelector(selector) as Maybe<T>) ?? null;
}

function showSelectionError(
	tableDiv: HTMLElement | null,
	errorId: string,
	errorMessage: string,
): void {
	if (!tableDiv) return;
	tableDiv.classList.add("border-red-500", "dark:border-red-500");
	let errorDiv = document.getElementById(errorId);
	if (!errorDiv) {
		errorDiv = document.createElement("div");
		errorDiv.id = errorId;
		errorDiv.className = "text-red-500 text-sm";
		errorDiv.textContent = errorMessage;
		const parent = tableDiv.parentNode;
		if (parent) parent.insertBefore(errorDiv, tableDiv.nextSibling);
	}
}

function hideSelectionError(
	tableDiv: HTMLElement | null,
	errorId: string,
): void {
	if (!tableDiv) return;
	// only remove border if no amount error exists
	if (!document.getElementById("amount-error")) {
		tableDiv.classList.remove("border-red-500", "dark:border-red-500");
	}
	const errorDiv = document.getElementById(errorId);
	if (errorDiv) errorDiv.remove();
}

export function setupCheckboxValidation(
	formId: string,
	checkboxName: string,
	tableSelector: string,
	errorMessage: string,
): void {
	const form = document.getElementById(formId) as Maybe<HTMLFormElement>;
	if (!form) return;

	const tableDiv = (form.querySelector(tableSelector) ??
		document.querySelector(tableSelector)) as Maybe<HTMLElement>;
	if (!tableDiv) return;

	const errorId = `${checkboxName}-selection-error`;

	form.addEventListener("submit", (e: Event) => {
		const checked = form.querySelectorAll<HTMLInputElement>(
			`input[name="${checkboxName}"]:checked`,
		);
		if (checked.length === 0) {
			e.preventDefault();
			showSelectionError(tableDiv, errorId, errorMessage);
		} else {
			hideSelectionError(tableDiv, errorId);
		}
	});

	form.addEventListener("change", (e: Event) => {
		const target = e.target as Maybe<HTMLInputElement>;
		if (!target) return;
		if (target.name === checkboxName) {
			const checked = form.querySelectorAll<HTMLInputElement>(
				`input[name="${checkboxName}"]:checked`,
			);
			if (checked.length > 0) hideSelectionError(tableDiv, errorId);
		}
	});

	const selectAll = tableDiv.querySelector<HTMLInputElement>(
		'input[type="checkbox"][id^="select-all"]',
	);
	if (selectAll) {
		selectAll.addEventListener("change", () => {
			const checked = form.querySelectorAll<HTMLInputElement>(
				`input[name="${checkboxName}"]:checked`,
			);
			if (checked.length > 0) hideSelectionError(tableDiv, errorId);
		});
	}
}

/* Attach to global for legacy templates that call window.setupCheckboxValidation */
declare global {
	interface Window {
		setupCheckboxValidation?: typeof setupCheckboxValidation;
	}
}
if (typeof window !== "undefined") {
	window.setupCheckboxValidation = setupCheckboxValidation;
}

// Auto-initialize forms that opt-in via data-* attributes
document.addEventListener("DOMContentLoaded", () => {
	document
		.querySelectorAll<HTMLElement>('[data-checkbox-validation="true"]')
		.forEach((el) => {
			const formId = el.getAttribute("data-form-id") || el.id || "createForm";
			const checkboxName =
				el.getAttribute("data-checkbox-name") || "employee_ids";
			const tableSelector =
				el.getAttribute("data-table-selector") || ".employee-table-container";
			const errorMessage = el.getAttribute("data-error-message") || "";
			if (formId) {
				setupCheckboxValidation(
					formId,
					checkboxName,
					tableSelector,
					errorMessage,
				);
			}
		});
});

/**
 * Validation UI Cleanup:
 * Automatically removes error styles (red borders) and error messages
 * when the user interacts with a form field.
 */
const FORM_ERROR_CLEAR_SELECTORS = {
	fields: "input, select, textarea",
} as const;

const FORM_ERROR_CLEAR_SUFFIX = {
	error: "_error",
} as const;

// Tailwind classes used to highlight fields with validation errors
const RED_BORDER_CLASSES = [
	"border-red-600",
	"focus:ring-red-600",
	"focus:border-red-600",
	"focus:text-red-600",
	"dark:border-red-600",
	"dark:focus:ring-red-600",
	"dark:focus:border-red-600",
	"dark:focus:text-red-600",
] as const;

type FormElement = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;

/**
 * Type Guard to ensure the event target is a valid focusable form element.
 */
const isFormElement = (el: EventTarget | null): el is FormElement =>
	el instanceof HTMLInputElement ||
	el instanceof HTMLSelectElement ||
	el instanceof HTMLTextAreaElement;

/**
 * Builds a validation error element ID from a field ID/name.
 */
const getErrorId = (base: string): string =>
	`${base}${FORM_ERROR_CLEAR_SUFFIX.error}`;

/**
 * Removes validation styling and destroys the associated error message element.
 * Tries to find the error node using the field's ID first, then falls back to its Name.
 */
function clearValidationUi(el: FormElement): void {
	el.classList.remove(...RED_BORDER_CLASSES);

	// 1. Try finding error container by element ID (e.g., "id_email_error")
	const id = el.id?.trim();
	if (id) {
		const errorDiv = document.getElementById(getErrorId(id));
		if (errorDiv) {
			errorDiv.remove();
			return;
		}
	}

	// 2. Fallback: Try finding error container by element Name (e.g., "email_error")
	const name = el.name?.trim();
	if (name) {
		const nameErr = document.getElementById(getErrorId(name));
		if (nameErr) nameErr.remove();
	}
}

document.addEventListener("DOMContentLoaded", () => {
	/**
	 * Centralized event handler using Event Delegation.
	 * This catches events bubbling up from fields, including those added dynamically.
	 */
	const handler = (event: Event): void => {
		const target = event.target;
		if (!isFormElement(target)) return;

		// Ensure the element matches our defined selectors for validation clearing
		if (!target.matches(FORM_ERROR_CLEAR_SELECTORS.fields)) return;
		clearValidationUi(target);
	};

	/**
	 * 'input' event captures real-time typing/editing.
	 * 'change' event handles value selection for checkboxes, radios, and selects.
	 */
	document.addEventListener("input", handler);
	document.addEventListener("change", handler);
});

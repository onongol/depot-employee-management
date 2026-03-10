/**
 * Provides keyboard form navigation:
 * - Enter focuses the next input.
 * - Shift + Enter goes back.
 * - Skips textareas, buttons, checkboxes, and radio buttons to preserve default behavior.
 * - Submits the form when Enter is pressed on the last field.
 * - Uses MutationObserver to cache focusable elements efficiently.
 */
const FORM_NAV_IDS = {
	create: "createForm",
	update: "updateForm",
} as const;

const FORM_NAV_KEYS = {
	enter: "Enter",
} as const;

const FORM_NAV_ATTRS = {
	disabled: "disabled",
	type: "type",
	class: "class",
	style: "style",
	hidden: "hidden",
	tabindex: "tabindex",
} as const;

// Defines which elements are considered part of the flow
const FORM_NAV_SELECTORS = {
	focusable:
		'input:not([type="hidden"]):not([disabled]), select:not([disabled]), textarea:not([disabled])',
} as const;

const FORM_NAV_TAGS = {
	textarea: "textarea",
	button: "button",
	input: "input",
} as const;

const FORM_NAV_INPUT_TYPES = {
	checkbox: "checkbox",
	radio: "radio",
} as const;

const FORM_IDS = [FORM_NAV_IDS.create, FORM_NAV_IDS.update] as const;

// Attributes to watch for changes to trigger a cache refresh
const FORM_NAV_OBSERVER_ATTRS = [
	FORM_NAV_ATTRS.disabled,
	FORM_NAV_ATTRS.type,
	FORM_NAV_ATTRS.class,
	FORM_NAV_ATTRS.style,
	FORM_NAV_ATTRS.hidden,
	FORM_NAV_ATTRS.tabindex,
] as const;

document.addEventListener("DOMContentLoaded", () => {
	/**
	 * Checks if an element is actually visible to the user and not explicitly unfocusable.
	 */
	const isVisibleAndFocusable = (el: HTMLElement): boolean =>
		el.getClientRects().length > 0 &&
		!el.hasAttribute(FORM_NAV_ATTRS.disabled) &&
		el.tabIndex !== -1;

	/**
	 * Queries the DOM for all relevant focusable elements within a specific form.
	 */
	function getFocusableInputs(form: HTMLFormElement): HTMLElement[] {
		const nodeList = form.querySelectorAll<HTMLElement>(
			FORM_NAV_SELECTORS.focusable,
		);
		return [...nodeList].filter(isVisibleAndFocusable);
	}

	/**
	 * Implements a lazy-loading cache using MutationObserver.
	 * Prevents expensive DOM queries on every keystroke unless the form structure changes.
	 */
	function createFocusableCache(form: HTMLFormElement) {
		let cache: HTMLElement[] = [];
		let dirty = true; // Flag indicating the cache needs a refresh

		const refresh = (): void => {
			cache = getFocusableInputs(form);
			dirty = false;
		};

		const get = (): HTMLElement[] => {
			if (dirty) refresh();
			return cache;
		};

		const markDirty = (): void => {
			dirty = true;
		};

		// Observe changes to the form (added/removed elements or attribute changes)
		const observer = new MutationObserver(markDirty);
		observer.observe(form, {
			subtree: true,
			childList: true,
			attributes: true,
			attributeFilter: [...FORM_NAV_OBSERVER_ATTRS],
		});

		return { get, markDirty };
	}

	// Initialize logic for each registered form ID
	FORM_IDS.forEach((formId) => {
		const formEl = document.getElementById(formId);
		if (!(formEl instanceof HTMLFormElement)) return;
		const form = formEl;

		const focusableCache = createFocusableCache(form);

		form.addEventListener("keydown", (event: KeyboardEvent) => {
			// Only intercept the Enter key
			if (event.key !== FORM_NAV_KEYS.enter) return;

			const active = document.activeElement as HTMLElement | null;
			if (!active || !form.contains(active)) return;

			// Preserve default Enter behavior for multiline inputs and buttons
			const tag = active.tagName.toLowerCase();
			if (tag === FORM_NAV_TAGS.textarea || tag === FORM_NAV_TAGS.button)
				return;

			// Preserve standard Enter behavior for selection-based inputs
			if (tag === FORM_NAV_TAGS.input && active instanceof HTMLInputElement) {
				const type = active.type.toLowerCase();
				if (
					type === FORM_NAV_INPUT_TYPES.checkbox ||
					type === FORM_NAV_INPUT_TYPES.radio
				) {
					return;
				}
			}

			const inputs = focusableCache.get();
			const currentIndex = inputs.indexOf(active);
			if (currentIndex === -1) return;

			// Stop the default form submission triggered by the Enter key
			event.preventDefault();

			// Handle Backward Navigation (Shift + Enter)
			if (event.shiftKey) {
				if (currentIndex > 0) {
					const prev = inputs[currentIndex - 1];
					if (prev) prev.focus();
				}
				return;
			}

			if (currentIndex < inputs.length - 1) {
				const next = inputs[currentIndex + 1];
				if (next) {
					next.focus();
				}
			} else {
				// If on the last field, trigger a standard form submission
				// requestSubmit() is used to trigger HTML5 validation (required, pattern, etc.)
				form.requestSubmit ? form.requestSubmit() : form.submit();
			}
		});
	});
});

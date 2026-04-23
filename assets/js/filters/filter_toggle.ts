/**
 * Filter panel toggle logic (TypeScript, strict, no any).
 * Manages responsive behavior for filter panels, specifically handling
 * desktop-sidebar vs mobile-overlay transitions.
 */
const FILTER_TOGGLE_SELECTORS = {
	toggleBtn: '[data-filter-toggle="true"]',
	overlay: "[data-filter-overlay]",
} as const;

const FILTER_TOGGLE_CLASSES = {
	hidden: "hidden",
	lockScroll: "overflow-hidden",
	translateYFull: "translate-y-full",
} as const;

const FILTER_TOGGLE_ATTRS = {
	ariaExpanded: "aria-expanded",
} as const;

/** Breakpoint for desktop view - synchronization with Tailwind 'lg' recommended */
const FILTER_TOGGLE_MEDIA_QUERY = "(min-width: 1024px)";
const mql = window.matchMedia(FILTER_TOGGLE_MEDIA_QUERY);

/**
 * WeakSet used to track initialized elements.
 * Prevents duplicate event listener binding during HTMX swaps.
 */
const initialized = new WeakSet<HTMLElement>();

/** Generates a unique key for session storage to persist panel state per target */
function getFilterStorageKey(targetId: string): string {
	return `filtersOpen:${targetId}`;
}

/**
 * Synchronizes the visual state of the panel, overlay, and trigger button.
 * Respects the current device mode (Desktop/Mobile) provided by MediaQueryList.
 * @param panel - The HTML element of the filter panel.
 * @param btn - The button element that triggers the toggle.
 * @param open - Boolean flag representing the target visibility state.
 * @param overlays - Map containing overlay elements associated with their target IDs.
 * @param mql - The MediaQueryList instance for responsive checks.
 */
function applyState(
	panel: HTMLElement,
	btn: HTMLButtonElement,
	open: boolean,
	overlays: Map<string, HTMLElement>,
	mql: MediaQueryList,
) {
	const overlay = overlays.get(panel.id);
	const isDesktop = mql.matches;

	// Handle Overlay visibility and Body scroll locking (Mobile only)
	if (overlay)
		overlay.classList.toggle(FILTER_TOGGLE_CLASSES.hidden, isDesktop || !open);

	document.body.classList.toggle(
		FILTER_TOGGLE_CLASSES.lockScroll,
		!isDesktop && open && !!overlay,
	);

	// Toggle Panel visibility classes based on state and viewport
	panel.classList.toggle(
		FILTER_TOGGLE_CLASSES.hidden,
		isDesktop ? false : !open,
	);
	panel.classList.toggle(
		FILTER_TOGGLE_CLASSES.translateYFull,
		isDesktop ? false : !open,
	);

	// Update ARIA attribute for accessibility
	btn.setAttribute(FILTER_TOGGLE_ATTRS.ariaExpanded, open.toString());
}

/**
 * Re-evaluates the state of all tracked filter toggles.
 * Forces panels to 'open' on Desktop while restoring saved state on Mobile.
 * @param toggles - Array of filter toggle button elements.
 * @param overlays - Map of overlay elements.
 * @param mql - The MediaQueryList instance.
 */
function applyResponsive(
	toggles: HTMLButtonElement[],
	overlays: Map<string, HTMLElement>,
	mql: MediaQueryList,
) {
	for (const btn of toggles) {
		const targetId = btn.dataset.target;
		if (!targetId) continue;

		const panel = document.getElementById(targetId);
		if (!panel) continue;

		const storageKey = getFilterStorageKey(targetId);

		// Always show panels on desktop
		if (mql.matches) {
			applyState(panel, btn, true, overlays, mql);
			continue;
		}

		// Restore user's last session state when switching to mobile
		const saved = sessionStorage.getItem(storageKey);
		applyState(panel, btn, saved === "true", overlays, mql);
	}
}

/**
 * Orchestrates the initialization of filter toggles and overlays.
 * Uses idempotency patterns to safely run after HTMX content swaps.
 */
function initFilterToggles() {
	const toggles = Array.from(
		document.querySelectorAll<HTMLButtonElement>(
			FILTER_TOGGLE_SELECTORS.toggleBtn,
		),
	);
	const overlays = new Map<string, HTMLElement>();

	// Map overlays to their respective target IDs
	for (const overlay of document.querySelectorAll<HTMLElement>(
		FILTER_TOGGLE_SELECTORS.overlay,
	)) {
		const key = overlay.dataset.filterOverlay;
		if (key) overlays.set(key, overlay);
	}

	// Initialize toggle buttons with click listeners
	for (const btn of toggles) {
		if (initialized.has(btn)) continue;

		btn.addEventListener("click", () => {
			if (mql.matches) return;
			const targetId = btn.dataset.target;
			if (!targetId) return;
			const panel = document.getElementById(targetId);
			if (!panel) return;

			const isOpen =
				btn.getAttribute(FILTER_TOGGLE_ATTRS.ariaExpanded) === "true";
			const next = !isOpen;

			applyState(panel, btn, next, overlays, mql);
			sessionStorage.setItem(getFilterStorageKey(targetId), next.toString());
		});

		initialized.add(btn);
	}

	// Initialize overlays to allow closing the panel by clicking outside
	for (const [targetId, overlay] of overlays.entries()) {
		if (initialized.has(overlay)) continue;

		overlay.addEventListener("click", () => {
			if (!targetId) return;
			const panel = document.getElementById(targetId);
			const btn = toggles.find((b) => b.dataset.target === targetId);
			if (!panel || !btn) return;

			applyState(panel, btn, false, overlays, mql);
			sessionStorage.setItem(getFilterStorageKey(targetId), "false");
		});

		initialized.add(overlay);
	}

	// Perform initial synchronization
	applyResponsive(toggles, overlays, mql);
}

/**
 * Global Resize Listener.
 * Re-syncs all filters when the viewport crosses the mobile/desktop threshold.
 */
mql.addEventListener("change", () => {
	const toggles = Array.from(
		document.querySelectorAll<HTMLButtonElement>(
			FILTER_TOGGLE_SELECTORS.toggleBtn,
		),
	);
	const overlays = new Map<string, HTMLElement>();
	for (const el of document.querySelectorAll<HTMLElement>(
		FILTER_TOGGLE_SELECTORS.overlay,
	)) {
		if (el.dataset.filterOverlay) overlays.set(el.dataset.filterOverlay, el);
	}
	applyResponsive(toggles, overlays, mql);
});

/**
 * Initial execution logic.
 * Ensures the script runs only after the DOM is fully interactive.
 */
if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", initFilterToggles);
} else {
	initFilterToggles();
}

/**
 * HTMX Integration.
 * Re-runs initialization whenever HTMX swaps new content into the DOM.
 */
document.addEventListener("htmx:afterSwap", initFilterToggles);

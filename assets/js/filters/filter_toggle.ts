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

/** Generates a unique key for session storage to persist panel state per target */
function getFilterStorageKey(targetId: string): string {
	return `filtersOpen:${targetId}`;
}

/**
 * Synchronizes the visual state of the panel, overlay, and trigger button.
 * Respects the current device mode (Desktop/Mobile) provided by MediaQueryList.
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
 */
function applyResponsive(
	toggles: HTMLButtonElement[],
	overlays: Map<string, HTMLElement>,
	mql: MediaQueryList,
) {
	toggles.forEach((btn) => {
		const targetId = btn.dataset.target;
		if (!targetId) return;

		const panel = document.getElementById(targetId);
		if (!panel) return;

		const storageKey = getFilterStorageKey(targetId);

		// Always show panels on desktop
		if (mql.matches) {
			applyState(panel, btn, true, overlays, mql);
			return;
		}

		// Restore user's last session state when switching to mobile
		const saved = sessionStorage.getItem(storageKey);
		applyState(panel, btn, saved === "true", overlays, mql);
	});
}

document.addEventListener("DOMContentLoaded", () => {
	const mql = window.matchMedia(FILTER_TOGGLE_MEDIA_QUERY);

	/** Collection of all filter trigger buttons */
	const toggles: HTMLButtonElement[] = Array.from(
		document.querySelectorAll<HTMLButtonElement>(
			FILTER_TOGGLE_SELECTORS.toggleBtn,
		),
	);

	/** Mapping of TargetID -> OverlayElement for O(1) lookup performance */
	const overlays = new Map<string, HTMLElement>();
	document
		.querySelectorAll<HTMLElement>(FILTER_TOGGLE_SELECTORS.overlay)
		.forEach((overlay) => {
			const key = overlay.dataset.filterOverlay;
			if (key) overlays.set(key, overlay);
		});

	// Initialize Click Listeners for Toggle Buttons
	toggles.forEach((btn) => {
		btn.addEventListener("click", () => {
			// Toggles are disabled on Desktop as filters are permanently visible
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
	});

	// Close Panel logic when clicking on the background overlay
	overlays.forEach((overlay, targetId) => {
		overlay.addEventListener("click", () => {
			if (!targetId) return;

			const panel = document.getElementById(targetId);
			const btn = toggles.find((b) => b.dataset.target === targetId);

			if (!panel || !btn) return;

			applyState(panel, btn, false, overlays, mql);
			sessionStorage.setItem(getFilterStorageKey(targetId), "false");
		});
	});

	// Listen for window resize / orientation changes via MediaQueryList
	mql.addEventListener("change", () => applyResponsive(toggles, overlays, mql));

	// Initial state application on page load
	applyResponsive(toggles, overlays, mql);
});

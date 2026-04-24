/**
 * Filter panel toggle logic (TypeScript, strict, no any).
 * Manages responsive behavior for filter panels, specifically handling
 * desktop-sidebar vs mobile-overlay transitions.
 */

interface FilterRegistryEntry {
	panel: HTMLElement;
	btn: HTMLButtonElement;
	overlay: HTMLElement | null;
}

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

/** Prevents duplicate listeners during HTMX swaps */
const initializedElements = new WeakSet<HTMLElement>();

/** Storage for initialized filter relationships */
const filterRegistry = new Map<string, FilterRegistryEntry>();

/** Persistence key helper */
function getFilterStorageKey(targetId: string): string {
	return `filtersOpen:${targetId}`;
}

/** Overlay selector helper */
function getOverlaySelector(targetId: string): string {
	return `${FILTER_TOGGLE_SELECTORS.overlay}[data-filter-overlay="${targetId}"]`;
}

/**
 * Core UI Logic: Synchronizes visual and accessibility states.
 */
function applyState(
	entry: FilterRegistryEntry,
	open: boolean,
	isDesktop: boolean,
): void {
	const { panel, btn, overlay } = entry;

	if (overlay) {
		overlay.classList.toggle(FILTER_TOGGLE_CLASSES.hidden, isDesktop || !open);
	}

	// Body scroll lock management (Mobile only)
	if (overlay) {
		document.body.classList.toggle(
			FILTER_TOGGLE_CLASSES.lockScroll,
			!isDesktop && open,
		);
	}

	panel.classList.toggle(
		FILTER_TOGGLE_CLASSES.hidden,
		isDesktop ? false : !open,
	);
	panel.classList.toggle(
		FILTER_TOGGLE_CLASSES.translateYFull,
		isDesktop ? false : !open,
	);

	btn.setAttribute(FILTER_TOGGLE_ATTRS.ariaExpanded, open.toString());
}

/**
 * Evaluates responsive layout transitions for all registered filters.
 */
function applyResponsive(): void {
	const isDesktop = mql.matches;

	for (const [targetId, entry] of filterRegistry) {
		if (isDesktop) {
			applyState(entry, true, true);
		} else {
			const saved = sessionStorage.getItem(getFilterStorageKey(targetId));
			applyState(entry, saved === "true", false);
		}
	}
}

/**
 * Registry-based closer. Clears all mobile states at once.
 */
function closeAllMobileFilters(): void {
	if (mql.matches) return;

	for (const [targetId, entry] of filterRegistry) {
		applyState(entry, false, false);
		sessionStorage.setItem(getFilterStorageKey(targetId), "false");
	}
}

/**
 * Scans DOM for filter components and maps their relationships.
 */
function initFilterToggles(): void {
	const toggleButtons = document.querySelectorAll<HTMLButtonElement>(
		FILTER_TOGGLE_SELECTORS.toggleBtn,
	);

	for (const btn of toggleButtons) {
		const targetId = btn.dataset.target;
		if (!targetId || initializedElements.has(btn)) continue;

		const panel = document.getElementById(targetId);
		if (!panel) continue;

		const overlay = document.querySelector<HTMLElement>(
			getOverlaySelector(targetId),
		);

		// Store relationship in the Registry
		const entry: FilterRegistryEntry = { panel, btn, overlay };
		filterRegistry.set(targetId, entry);

		// Event Binding
		btn.addEventListener("click", () => {
			if (mql.matches) return;
			const isOpen =
				btn.getAttribute(FILTER_TOGGLE_ATTRS.ariaExpanded) === "true";
			const nextState = !isOpen;

			applyState(entry, nextState, mql.matches);
			sessionStorage.setItem(
				getFilterStorageKey(targetId),
				nextState.toString(),
			);
		});

		if (overlay) {
			overlay.addEventListener("click", () => {
				applyState(entry, false, mql.matches);
				sessionStorage.setItem(getFilterStorageKey(targetId), "false");
			});
			initializedElements.add(overlay);
		}

		initializedElements.add(btn);
	}

	// Initial sync
	applyResponsive();
}

// --- Global Event Handlers ---

/** Close filters after mobile form submission */
document.addEventListener("submit", (e) => {
	if (!(e.target instanceof HTMLFormElement)) return;
	if (filterRegistry.size > 0) closeAllMobileFilters();
});

/** Handle viewport resizing */
mql.addEventListener("change", applyResponsive);

/** Standard Lifecycle Initialization */
if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", initFilterToggles);
} else {
	initFilterToggles();
}

/** HTMX Content Swap Lifecycle Support */
document.addEventListener("htmx:afterSwap", initFilterToggles);

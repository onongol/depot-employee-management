// Toggles the left sidebar with overlay: opens on mobile via hamburger, closes on overlay, ESC, or retoggle.

const SIDEBAR_IDS = {
	sidebar: "app-sidebar",
	overlay: "sidebar-overlay",
} as const;

const SIDEBAR_CLASSES = {
	hidden: "hidden",
	translateClosed: "-translate-x-full",
	bodyLock: "overflow-hidden",
} as const;

const SIDEBAR_KEYS = {
	escape: "Escape",
} as const;

const SIDEBAR_MEDIA = {
	desktop: "(min-width: 1024px)",
} as const;

const SIDEBAR_SELECTORS = {
	toggleButtons: "[data-sidebar-toggle]",
} as const;

const SIDEBAR_ATTRS = {
	ariaExpanded: "aria-expanded",
} as const;

document.addEventListener("DOMContentLoaded", () => {
	const buttons = Array.from(
		document.querySelectorAll<HTMLButtonElement>(
			SIDEBAR_SELECTORS.toggleButtons,
		),
	);

	const sidebar = document.getElementById(SIDEBAR_IDS.sidebar);
	const overlay = document.getElementById(SIDEBAR_IDS.overlay);

	if (
		!buttons.length ||
		!(sidebar instanceof HTMLElement) ||
		!(overlay instanceof HTMLElement)
	)
		return;

	let isSidebarOpen = false;

	const setAriaExpanded = (open: boolean): void => {
		buttons.forEach((btn) => {
			btn.setAttribute(SIDEBAR_ATTRS.ariaExpanded, String(open));
		});
	};

	const applySidebarState = (open: boolean): void => {
		isSidebarOpen = open;

		sidebar.classList.toggle(SIDEBAR_CLASSES.translateClosed, !open);

		overlay.classList.toggle(SIDEBAR_CLASSES.hidden, !open);
		document.body.classList.toggle(SIDEBAR_CLASSES.bodyLock, open);

		setAriaExpanded(open);
	};

	const open = (): void => {
		applySidebarState(true);
	};

	const close = (): void => {
		applySidebarState(false);
	};

	const toggle = (): void => {
		if (desktopMql.matches) return;
		if (isSidebarOpen) close();
		else open();
	};

	const desktopMql = window.matchMedia(SIDEBAR_MEDIA.desktop);

	const syncWithViewport = (): void => {
		if (desktopMql.matches) {
			applySidebarState(false);
			return;
		}

		if (!isSidebarOpen) {
			sidebar.classList.add(SIDEBAR_CLASSES.translateClosed);
			overlay.classList.add(SIDEBAR_CLASSES.hidden);
		}
	};

	buttons.forEach((btn) => {
		btn.addEventListener("click", toggle);
	});

	overlay.addEventListener("click", close);

	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === SIDEBAR_KEYS.escape) close();
	});

	desktopMql.addEventListener("change", syncWithViewport);
	syncWithViewport();
});

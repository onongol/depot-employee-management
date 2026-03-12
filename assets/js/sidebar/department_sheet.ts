/**
 * Department Sheet Component:
 * Manages side/bottom panels for different departments.
 * Features: exclusive opening, body scroll synchronization, swipe-to-close on mobile,
 * and global Escape key handling.
 */
const DEPT_SHEET_SELECTORS = {
	root: "[data-department-sheet]",
	openBtn: "[data-department-sheet-open]",
	panel: "[data-department-sheet-panel]",
	backdrop: "[data-department-sheet-backdrop]",
} as const;

const DEPT_SHEET_CLASSES = {
	hidden: "hidden",
	overflowHidden: "overflow-hidden",
} as const;

const DEPT_SHEET_ATTRS = {
	ariaExpanded: "aria-expanded",
} as const;

const DEPT_SHEET_KEYS = {
	escape: "Escape",
} as const;

// Minimum vertical distance in pixels to trigger a swipe-close
const DEPT_SHEET_TOUCH = {
	minSwipeY: 60,
} as const;

const DEPT_SHEET_VALUES = {
    ariaFalse: "false",
} as const;

document.addEventListener("DOMContentLoaded", () => {
	// Convert NodeList to Array to utilize array methods like .some()
	const roots = Array.from(
		document.querySelectorAll<HTMLElement>(DEPT_SHEET_SELECTORS.root),
	);

	if (!roots.length) return;

	/**
	 * Checks if any department panel is currently visible in the DOM.
	 */
	const hasOpenPanel = (): boolean =>
		roots.some((root) => {
			const panel = root.querySelector<HTMLElement>(DEPT_SHEET_SELECTORS.panel);
			return panel
				? !panel.classList.contains(DEPT_SHEET_CLASSES.hidden)
				: false;
		});

	/**
	 * Toggles the scroll lock on the body based on the presence of open panels.
	 */
	const syncBodyLock = (): void => {
		document.body.classList.toggle(
			DEPT_SHEET_CLASSES.overflowHidden,
			hasOpenPanel(),
		);
	};

	/**
	 * Closes all active sheets and cleans up UI states globally.
	 */
	const closeAll = (): void => {
		roots.forEach((root) => {
			const openBtn = root.querySelector<HTMLButtonElement>(
				DEPT_SHEET_SELECTORS.openBtn,
			);
			const panel = root.querySelector<HTMLElement>(DEPT_SHEET_SELECTORS.panel);
			const backdrop = root.querySelector<HTMLElement>(
				DEPT_SHEET_SELECTORS.backdrop,
			);

			if (!openBtn || !panel || !backdrop) return;

			panel.classList.add(DEPT_SHEET_CLASSES.hidden);
			backdrop.classList.add(DEPT_SHEET_CLASSES.hidden);
			openBtn.setAttribute(DEPT_SHEET_ATTRS.ariaExpanded, DEPT_SHEET_VALUES.ariaFalse);
		});

		syncBodyLock();
	};

	// Initialize individual sheet logic
	roots.forEach((root) => {
		const openBtn = root.querySelector<HTMLButtonElement>(
			DEPT_SHEET_SELECTORS.openBtn,
		);
		const panel = root.querySelector<HTMLElement>(DEPT_SHEET_SELECTORS.panel);
		const backdrop = root.querySelector<HTMLElement>(
			DEPT_SHEET_SELECTORS.backdrop,
		);

		if (!openBtn || !panel || !backdrop) return;

		/**
		 * Local state manager for a specific sheet.
		 * Ensures only one sheet is open at any given time.
		 */
		const setOpen = (open: boolean): void => {
			if (open) closeAll(); // only one sheet open at a time

			panel.classList.toggle(DEPT_SHEET_CLASSES.hidden, !open);
			backdrop.classList.toggle(DEPT_SHEET_CLASSES.hidden, !open);
			openBtn.setAttribute(DEPT_SHEET_ATTRS.ariaExpanded, String(open));

			syncBodyLock();
		};

		openBtn.addEventListener("click", () => setOpen(true));
		backdrop.addEventListener("click", () => setOpen(false));

		/**
		 * Mobile UX: Swipe-down to close logic.
		 * Tracks touch movement on the panel to determine if the user is swiping down.
		 */
		let touchStartY: number | null = null;
		let startScrollTop = 0;

		panel.addEventListener(
			"touchstart",
			(e: TouchEvent) => {
				const touch = e.touches.item(0);
				if (!touch) return;

				touchStartY = touch.clientY;
				// Capture scroll position to ensure swipe only triggers when at the top of the content
				startScrollTop = panel.scrollTop;
			},
			{ passive: true },
		);

		panel.addEventListener(
			"touchend",
			(e: TouchEvent) => {
				if (touchStartY === null) return;

				const touch = e.changedTouches.item(0);
				if (!touch) return;

				const touchEndY = touch.clientY;
				const deltaY = touchEndY - touchStartY;

				// Close if swipe distance exceeds threshold and user is at the top of the scrollable content
				if (deltaY > DEPT_SHEET_TOUCH.minSwipeY && startScrollTop <= 0) {
					setOpen(false);
				}

				touchStartY = null;
			},
			{ passive: true },
		);
	});

	/**
	 * Single global listener for the Escape key.
	 * Centralizing this improves performance and simplifies event management.
	 */
	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === DEPT_SHEET_KEYS.escape) closeAll();
	});
});

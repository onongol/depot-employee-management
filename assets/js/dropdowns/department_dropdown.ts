/**
 * Interface representing the core elements of a dropdown component.
 */
interface DropdownElements {
	button: HTMLButtonElement;
	menu: HTMLElement;
}

// Configuration constants for DOM selectors, CSS classes, and key codes.
const SELECTORS = {
	dropdownRoot: "[data-dropdown]",
	dropdownButton: "[data-dropdown-button]",
	dropdownMenu: "[data-dropdown-menu]",
	dropdownItems: "a,button",
} as const;

const CLASSES = {
	hidden: "hidden",
} as const;

const KEYS = {
	escape: "Escape",
} as const;

document.addEventListener("DOMContentLoaded", () => {
	// Keep track of currently active (visible) menus.
	const openMenus = new Set<HTMLElement>();

	// Shows a specific dropdown menu and tracks it.
	const openMenu = (menu: HTMLElement): void => {
		menu.classList.remove(CLASSES.hidden);
		openMenus.add(menu);
	};

	// Hides a specific dropdown menu and updates tracking.
	const closeMenu = (menu: HTMLElement): void => {
		menu.classList.add(CLASSES.hidden);
		openMenus.delete(menu);
	};

	// Closes all currently open dropdown menus.
	const closeAllMenus = (): void => {
		[...openMenus].forEach(closeMenu);
	};

	/**
	 * Finds and validates required dropdown elements within a root container.
	 */
	function getDropdownElements(root: HTMLElement): DropdownElements | null {
		const button = root.querySelector<HTMLButtonElement>(
			SELECTORS.dropdownButton,
		);
		const menu = root.querySelector<HTMLElement>(SELECTORS.dropdownMenu);
		if (!button || !menu) return null;
		return { button, menu };
	}

	/**
	 * Initializes logic and event listeners for a single dropdown instance.
	 */
	function setupDropdown(root: HTMLElement): void {
		const elements = getDropdownElements(root);
		if (!elements) return;

		const { button, menu } = elements;

		// Toggle menu visibility on button click.
		button.addEventListener("click", (e: MouseEvent) => {
			e.stopPropagation();
			if (menu.classList.contains(CLASSES.hidden)) openMenu(menu);
			else closeMenu(menu);
		});

		menu.addEventListener("click", (e: MouseEvent) => e.stopPropagation());

		menu
			.querySelectorAll<HTMLElement>(SELECTORS.dropdownItems)
			.forEach((item) => {
				item.addEventListener("click", () => closeMenu(menu));
			});
	}

	// Initialize all dropdowns found on the page.
	document
		.querySelectorAll<HTMLElement>(SELECTORS.dropdownRoot)
		.forEach(setupDropdown);

	// Global handlers to close menus on outside click or Escape key press.
	document.addEventListener("click", closeAllMenus);
	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === KEYS.escape) closeAllMenus();
	});
});

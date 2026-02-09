type Nullable<T> = T | null;

interface DropdownElements {
	button: HTMLElement;
	menu: HTMLElement;
}

document.addEventListener("DOMContentLoaded", () => {
	const openMenus = new Set<HTMLElement>();

	function setupDropdown(btnId: string, menuId: string): void {
		const btn: Nullable<HTMLElement> = document.getElementById(btnId);
		const menu: Nullable<HTMLElement> = document.getElementById(menuId);

		if (!btn) console.warn(`Button with id "${btnId}" not found`);
		if (!menu) console.warn(`Menu with id "${menuId}" not found`);
		if (!btn || !menu) return;

		btn.addEventListener("click", (e: MouseEvent) => {
			e.stopPropagation();
			if (menu.classList.contains("hidden")) openMenu(menu);
			else closeMenu(menu);
		});

		// prevent clicks inside menu from closing it
		menu.addEventListener("click", (e: MouseEvent) => e.stopPropagation());

		// close when a button inside menu is clicked
		menu.querySelectorAll<HTMLButtonElement>("button").forEach((item) => {
			item.addEventListener("click", () => closeMenu(menu));
		});
	}

	// Close all on outside click
	document.addEventListener("click", () => {
		openMenus.forEach((m) => closeMenu(m));
	});

	// Close all on Escape
	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === "Escape") openMenus.forEach((m) => closeMenu(m));
	});

	// Initialize known dropdowns
	setupDropdown("department-dropdown-btn", "department-dropdown-menu");

	// Helpers
	function openMenu(menu: HTMLElement): void {
		if (!(menu instanceof HTMLElement)) return;
		menu.classList.remove("hidden");
		openMenus.add(menu);
	}

	function closeMenu(menu: HTMLElement): void {
		if (!(menu instanceof HTMLElement)) return;
		menu.classList.add("hidden");
		openMenus.delete(menu);
	}
});

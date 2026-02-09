// Handles user, language, and theme dropdowns: toggles menus, stops click propagation to keep menus open when interacting inside, and closes all menus on outside clicks.

type Nullable<T> = T | null;

interface DropdownPair {
	btn: Nullable<HTMLButtonElement>;
	menu: Nullable<HTMLElement>;
}

const getEl = <T extends HTMLElement = HTMLElement>(id: string): Nullable<T> =>
	document.getElementById(id) as Nullable<T>;

document.addEventListener("DOMContentLoaded", () => {
	const user: DropdownPair = {
		btn: getEl<HTMLButtonElement>("user-dropdown-btn"),
		menu: getEl("user-dropdown-menu"),
	};
	const lang: DropdownPair = {
		btn: getEl<HTMLButtonElement>("language-dropdown-btn"),
		menu: getEl("language-dropdown-menu"),
	};
	const theme: DropdownPair = {
		btn: getEl<HTMLButtonElement>("theme-dropdown-btn"),
		menu: getEl("theme-dropdown-menu"),
	};

	const allPairs: DropdownPair[] = [user, lang, theme];

	function stopPropagationHandler(e: Event): void {
		e.stopPropagation();
	}

	function setupToggle(pair: DropdownPair): void {
		if (!pair.btn || !pair.menu) return;
		pair.btn.addEventListener("click", (e: MouseEvent) => {
			e.stopPropagation();
			pair.menu!.classList.toggle("hidden");
		});
		// clicks inside menu shouldn't close it
		pair.menu.addEventListener("click", stopPropagationHandler);
	}

	function closeAllMenus(): void {
		allPairs.forEach((p) => p.menu?.classList.add("hidden"));
	}

	// init toggles
	setupToggle(user);
	setupToggle(lang);
	setupToggle(theme);

	// clicking outside closes menus
	document.addEventListener("click", () => closeAllMenus());

	// ESC closes menus
	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === "Escape") closeAllMenus();
	});
});

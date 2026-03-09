const THEME_SELECTORS = {
	themePanel: '[data-panel="theme"]',
	themeButtons: "button[data-theme-value]",
	themeButtonByValue: (theme: Theme) => `button[data-theme-value="${theme}"]`,
	svgUse: "use",
} as const;

const THEME_ATTRS = {
	href: "href",
} as const;

const THEME_IDS = {
	themeIcon: "theme-icon",
	themeLabel: "theme-label",
	flatpickrDarkCss: "flatpickr-dark-css",
} as const;

const THEME_STORAGE = {
	themeKey: "theme",
} as const;

const THEME_MEDIA = {
	prefersDark: "(prefers-color-scheme: dark)",
} as const;

const THEME_ICONS = {
	dark: "#moon-stars-fill",
	light: "#sun-fill",
} as const;

const THEME_CLASSES = {
	dark: "dark",
	activeFont: "font-bold",
	activeText: "text-gray-600",
	activeTextDark: "dark:text-gray-400",
} as const;

const THEMES = {
	light: "light",
	dark: "dark",
	auto: "auto",
} as const;

// Define Theme type based on THEMES object
type Theme = (typeof THEMES)[keyof typeof THEMES];

/**
 * Type guard to ensure the string is a valid Theme type.
 */
function isTheme(value: string | null): value is Theme {
	return (
		value === THEMES.light || value === THEMES.dark || value === THEMES.auto
	);
}

document.addEventListener("DOMContentLoaded", () => {
	const themeMenu = document.querySelector<HTMLElement>(
		THEME_SELECTORS.themePanel,
	);

	// Cache theme light/dark/auto
	const themeButtons = new Map<Theme, HTMLButtonElement>();

	// Populate themeButtons map for easy access later
	if (themeMenu) {
		themeMenu
			.querySelectorAll<HTMLButtonElement>(THEME_SELECTORS.themeButtons)
			.forEach((btn) => {
				const value = btn.dataset.themeValue ?? null;
				if (isTheme(value)) {
					themeButtons.set(value, btn);
				}
			});
	}

	const prefersDark = (): boolean =>
		window.matchMedia(THEME_MEDIA.prefersDark).matches;

	/**
	 * Enables or disables the dark theme CSS for Flatpickr.
	 */
	function setFlatpickrTheme(isDark: boolean): void {
		const flatpickrCss = document.getElementById(
			THEME_IDS.flatpickrDarkCss,
		) as HTMLLinkElement | null;
		if (!flatpickrCss) return;
		flatpickrCss.disabled = !isDark;
	}

	function getThemeLabel(theme: Theme): string {
		const btn = themeMenu?.querySelector<HTMLButtonElement>(
			THEME_SELECTORS.themeButtonByValue(theme),
		);
		return btn?.dataset.label ?? btn?.textContent?.trim() ?? theme;
	}

	function updateUI(iconHref: string, labelText: string): void {
		const iconEl = document.getElementById(THEME_IDS.themeIcon);
		iconEl
			?.querySelector<SVGUseElement>(THEME_SELECTORS.svgUse)
			?.setAttribute(THEME_ATTRS.href, iconHref);

		const labelEl = document.getElementById(THEME_IDS.themeLabel);
		if (labelEl) labelEl.textContent = labelText;
	}

	/**
	 * Main function to apply theme logic.
	 */
	function setTheme(theme: Theme): void {
		const isDark =
			theme === THEMES.dark || (theme === THEMES.auto && prefersDark());
		const labelText = getThemeLabel(theme);

		// Apply theme to document
		document.documentElement.classList.toggle(THEME_CLASSES.dark, isDark);

		// Update visual indicators (Icon & Label)
		const iconHref = isDark ? THEME_ICONS.dark : THEME_ICONS.light;
		updateUI(iconHref, labelText);

		// Persistence
		localStorage.setItem(THEME_STORAGE.themeKey, theme);
		setFlatpickrTheme(isDark);

		// Update active state in the menu buttons
		themeButtons.forEach((btn, key) => {
			const isSelected = key === theme;
			btn.classList.toggle(THEME_CLASSES.activeFont, isSelected);
			btn.classList.toggle(THEME_CLASSES.activeText, isSelected);
			btn.classList.toggle(THEME_CLASSES.activeTextDark, isSelected);
		});
	}

	// --- Initialization ---
	const savedRaw = localStorage.getItem(THEME_STORAGE.themeKey);
	const savedTheme: Theme = isTheme(savedRaw) ? savedRaw : THEMES.auto;
	setTheme(savedTheme);

	// --- Event Listeners ---
	// Слушатели тоже из кэша
	themeButtons.forEach((btn, key) => {
		btn.addEventListener("click", () => setTheme(key));
	});

	// Listen for system theme changes (only react if current theme is "auto")
	const mql = window.matchMedia(THEME_MEDIA.prefersDark);
	if (mql) {
		const handler = () => {
			if (localStorage.getItem(THEME_STORAGE.themeKey) === THEMES.auto) {
				setTheme(THEMES.auto);
			}
		};
		mql.addEventListener("change", handler);
	}
});

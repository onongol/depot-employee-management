// Prevents theme flash on page load by applying saved or system-preferred dark mode immediately.
const THEME_INIT_STORAGE = {
	themeKey: "theme",
} as const;

const THEME_INIT_MEDIA = {
	prefersDark: "(prefers-color-scheme: dark)",
} as const;

const THEME_INIT_CLASSES = {
	dark: "dark",
} as const;

const THEME_INIT_THEMES = {
	light: "light",
	dark: "dark",
	auto: "auto",
} as const;

type ThemeInit = (typeof THEME_INIT_THEMES)[keyof typeof THEME_INIT_THEMES];

/**
 * Type guard to ensure the string is a valid ThemeInit type.
 */
function isThemeInit(value: string | null): value is ThemeInit {
	return (
		value === THEME_INIT_THEMES.light ||
		value === THEME_INIT_THEMES.dark ||
		value === THEME_INIT_THEMES.auto
	);
}

/**
 * Immediately apply the saved theme or system preference to prevent flash of incorrect theme on page load.
 */
try {
	const savedRaw = localStorage.getItem(THEME_INIT_STORAGE.themeKey);
	const theme: ThemeInit = isThemeInit(savedRaw)
		? savedRaw
		: THEME_INIT_THEMES.auto;

	const prefersDark = window.matchMedia(THEME_INIT_MEDIA.prefersDark).matches;
	const isAuto = theme === THEME_INIT_THEMES.auto;
	const isDark = theme === THEME_INIT_THEMES.dark || (isAuto && prefersDark);

	document.documentElement.classList.toggle(THEME_INIT_CLASSES.dark, isDark);
} catch {
	// Ignore storage/media access errors silently.
}

// Prevents theme flash on page load by applying saved or system-preferred dark mode immediately; sets or removes the dark class on the root element using localStorage and prefers-color-scheme.

(function () {
  try {
    const theme: string | null = localStorage.getItem('theme');
    const prefersDark: boolean =
      typeof window !== 'undefined' &&
      !!window.matchMedia?.('(prefers-color-scheme: dark)')?.matches;

    if (
      theme === 'dark' ||
      ((!theme || theme === 'auto') && prefersDark)
    ) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  } catch (e) {
    // silently ignore errors (e.g. localStorage access denied)
  }
})();
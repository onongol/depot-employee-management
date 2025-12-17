// Prevents theme flash on page load by applying saved or system-preferred dark mode immediately; sets or removes the dark class on the root element using localStorage and prefers-color-scheme.

(function() {
  try {
    var theme = localStorage.getItem('theme');
    if (
      theme === 'dark' ||
      ((!theme || theme === 'auto') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  } catch (e) {}
})();
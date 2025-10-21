document.addEventListener('DOMContentLoaded', function () {
  // Get theme dropdown button and menu elements
  const themeBtn = document.getElementById('theme-dropdown-btn');
  const themeMenu = document.getElementById('theme-dropdown-menu');

  // Function to enable/disable flatpickr dark theme CSS
  function setFlatpickrTheme(theme) {
    const flatpickrCss = document.querySelector('link[href*="flatpickr_dark.css"]');
    if (flatpickrCss) {
      if (theme === 'dark') {
        flatpickrCss.disabled = false;
      } else {
        flatpickrCss.disabled = true;
      }
    }
  }

  // Function to set the theme: 'light', 'dark', or 'auto'
  function setTheme(theme) {
    let icon = document.getElementById('theme-icon');
    let label = document.getElementById('theme-label');

    // Get the label for the selected theme
    const selectedBtn = themeMenu.querySelector(`button[data-theme-value="${theme}"]`);
    const themeLabel = selectedBtn ? (selectedBtn.getAttribute('data-label') || selectedBtn.textContent.trim()) : theme;

    // Set dark mode
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      // Change icon and label for dark mode
      if (icon) icon.firstElementChild.setAttribute('href', '#moon-stars-fill');
      if (label) label.textContent = themeLabel;
    }
    // Set light mode
    else if (theme === 'light') {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      // Change icon and label for light mode
      if (icon) icon.firstElementChild.setAttribute('href', '#sun-fill');
      if (label) label.textContent = themeLabel;
    }
    // Set auto (system) mode
    else {
      localStorage.setItem('theme', 'auto');
      // Apply theme based on system preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
        if (icon) icon.firstElementChild.setAttribute('href', '#moon-stars-fill');
      } else {
        document.documentElement.classList.remove('dark');
        if (icon) icon.firstElementChild.setAttribute('href', '#sun-fill');
      }
      if (label) label.textContent = themeLabel;
    }

    setFlatpickrTheme(theme);

    // Highlight the selected theme button in the dropdown
    themeMenu.querySelectorAll('button[data-theme-value]').forEach(btn => {
      if (btn.getAttribute('data-theme-value') === theme) {
        btn.classList.add('font-bold', 'text-gray-600', 'dark:text-gray-400');
      } else {
        btn.classList.remove('font-bold', 'text-gray-600', 'dark:text-gray-400');
      }
    });
  }

  // On page load, apply the saved theme or default to 'auto'
  const savedTheme = localStorage.getItem('theme') || 'auto';
  setTheme(savedTheme);

  // Add click event listeners to theme selection buttons
  themeMenu.querySelectorAll('button[data-theme-value]').forEach(btn => {
    btn.addEventListener('click', function () {
      setTheme(btn.getAttribute('data-theme-value'));
      // Close the theme dropdown menu after selection
      themeMenu.classList.add('hidden');
    });
  });

  // Listen for changes in system color scheme and update if in 'auto' mode
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    if (localStorage.getItem('theme') === 'auto') setTheme('auto');
  });
});
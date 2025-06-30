/**
 * Updates the theme icon in the theme switcher label.
 * @param {string} themeName - The current theme ("light", "dark", "auto").
 */
function updateCurrentThemeLabel(themeName) {
    let icon = '';
    if (themeName === 'light') {
        icon = '<svg class="w-5 h-5" aria-hidden="true"><use href="#sun-fill"></use></svg>';
    } else if (themeName === 'dark') {
        icon = '<svg class="w-5 h-5" aria-hidden="true"><use href="#moon-stars-fill"></use></svg>';
    } else if (themeName === 'auto') {
        icon = '<svg class="w-5 h-5" aria-hidden="true"><use href="#circle-half"></use></svg>';
    }
    const label = document.getElementById('current-theme-label');
    if (label) {
        label.innerHTML = icon;
    }
}

/**
 * Sets the theme for the application and saves it to localStorage.
 * @param {string} themeName - The theme to set ("light", "dark", "auto").
 */
function setTheme(themeName) {
    if (themeName === "auto") {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        localStorage.setItem('theme', 'auto');
    } else {
        document.documentElement.setAttribute('data-theme', themeName);
        localStorage.setItem('theme', themeName);
    }
    updateCurrentThemeLabel(themeName);
}

// Initialize theme from localStorage or default to 'light'
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Set the checked radio button if using radios (optional)
    const themeRadios = document.querySelectorAll('input[name="theme-radio"]');
    themeRadios.forEach(radio => {
        if (radio.value === savedTheme) {
            radio.checked = true;
        }
        radio.addEventListener('change', (event) => {
            setTheme(event.target.value);
        });
    });
});

// Listen for system theme changes if "auto" is selected
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('theme') === 'auto') {
        setTheme('auto');
    }
});

// Add click listeners to theme buttons
document.querySelectorAll('[data-theme-value]').forEach(btn => {
    btn.addEventListener('click', () => {
        setTheme(btn.getAttribute('data-theme-value'));
    });
});

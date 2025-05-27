// This script manages the theme switching functionality for a web page.
document.addEventListener('DOMContentLoaded', function() {
  const html = document.documentElement;
  const themeButtons = document.querySelectorAll('[data-bs-theme-value]');
  const themeIconActive = document.querySelector('.theme-icon-active');
  const themeIcons = {
    light: '#sun-fill',
    dark: '#moon-stars-fill',
    auto: '#circle-half'
  };

  function setTheme(theme) {
    if (theme === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      html.setAttribute('data-bs-theme', prefersDark ? 'dark' : 'light');
    } else {
      html.setAttribute('data-bs-theme', theme);
    }
    if (themeIconActive) {
      themeIconActive.querySelector('use').setAttribute('href', themeIcons[theme] || '#sun-fill');
    }
    themeButtons.forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-bs-theme-value') === theme);
      btn.setAttribute('aria-pressed', btn.getAttribute('data-bs-theme-value') === theme);
    });
  }

  let savedTheme = localStorage.getItem('bs-theme') || 'light';
  setTheme(savedTheme);

  themeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const theme = this.getAttribute('data-bs-theme-value');
      localStorage.setItem('bs-theme', theme);
      setTheme(theme);
    });
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (localStorage.getItem('bs-theme') === 'auto') {
      setTheme('auto');
    }
  });
});

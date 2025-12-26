type Theme = 'light' | 'dark' | 'auto';

document.addEventListener('DOMContentLoaded', () => {
  const themeMenu = document.getElementById('theme-dropdown-menu') as HTMLElement | null;

  const prefersDark = () =>
    typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-color-scheme: dark)')?.matches;

  function setFlatpickrTheme(theme: Theme): void {
    const flatpickrCss = document.getElementById('flatpickr-dark-css') as HTMLLinkElement | null;
    if (!flatpickrCss) return;
    flatpickrCss.disabled = !(
      theme === 'dark' || (theme === 'auto' && prefersDark())
    );
  }

  function getThemeLabel(menu: HTMLElement, theme: Theme): string {
    const btn = menu.querySelector<HTMLButtonElement>(`button[data-theme-value="${theme}"]`);
    return btn?.dataset.label ?? btn?.textContent?.trim() ?? theme;
  }

  function updateIconAndLabel(iconId: string, labelId: string, iconHref: string, labelText: string): void {
    const iconEl = document.getElementById(iconId);
    if (iconEl) {
      const useEl = iconEl.querySelector('use');
      if (useEl) useEl.setAttribute('href', iconHref);
    }
    const labelEl = document.getElementById(labelId);
    if (labelEl) labelEl.textContent = labelText;
  }

  function setTheme(theme: Theme): void {
    const menu = themeMenu;
    const labelText = menu ? getThemeLabel(menu, theme) : theme;

    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
      updateIconAndLabel('theme-icon', 'theme-label', '#moon-stars-fill', labelText);
    } else if (theme === 'light') {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      updateIconAndLabel('theme-icon', 'theme-label', '#sun-fill', labelText);
    } else {
      localStorage.setItem('theme', 'auto');
      if (prefersDark()) {
        document.documentElement.classList.add('dark');
        updateIconAndLabel('theme-icon', 'theme-label', '#moon-stars-fill', labelText);
      } else {
        document.documentElement.classList.remove('dark');
        updateIconAndLabel('theme-icon', 'theme-label', '#sun-fill', labelText);
      }
    }

    setFlatpickrTheme(theme);

    if (menu) {
      menu.querySelectorAll<HTMLButtonElement>('button[data-theme-value]').forEach(btn => {
        const isSelected = btn.getAttribute('data-theme-value') === theme;
        btn.classList.toggle('font-bold', isSelected);
        btn.classList.toggle('text-gray-600', isSelected);
        btn.classList.toggle('dark:text-gray-400', isSelected);
      });
    }
  }

  // initialise
  const saved = (localStorage.getItem('theme') as Theme | null) ?? 'auto';
  setTheme(saved);

  // attach handlers
  if (themeMenu) {
    themeMenu.querySelectorAll<HTMLButtonElement>('button[data-theme-value]').forEach(btn => {
      btn.addEventListener('click', () => {
        const val = btn.getAttribute('data-theme-value') as Theme | null;
        if (val) setTheme(val);
        themeMenu.classList.add('hidden');
      });
    });
  }

  // respond to system changes when in auto mode
  const mql = window.matchMedia?.('(prefers-color-scheme: dark)');
  if (mql) {
    const handler = (ev: MediaQueryListEvent) => {
      if (localStorage.getItem('theme') === 'auto') setTheme('auto');
    };
    if ('addEventListener' in mql) mql.addEventListener('change', handler);
    else mql.addListener(handler);
  }
});
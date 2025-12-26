// Toggles the navigation menu for mobile/desktop: manages open/close state at the lg breakpoint, updates aria-expanded for accessibility, adjusts classes for responsive display, and listens to toggle clicks and screen-size changes.

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('[data-collapse-toggle="navbar-menu"]') as HTMLButtonElement | null;
  const wrapper = document.getElementById('navbar-menu') as HTMLElement | null;
  if (!btn || !wrapper) return;

  let menu = wrapper.querySelector('ul') as HTMLElement | null;
  if (!menu) {
    const sib = wrapper.nextElementSibling;
    if (sib && sib.tagName === 'UL') menu = sib as HTMLElement;
  }
  if (!menu) return;

  const mql: MediaQueryList = window.matchMedia('(min-width: 1024px)');

  const setAria = (value: boolean) => btn.setAttribute('aria-expanded', value ? 'true' : 'false');

  const showElements = (...els: HTMLElement[]) => els.forEach(el => el.classList.remove('hidden'));
  const hideElements = (...els: HTMLElement[]) => els.forEach(el => el.classList.add('hidden'));

  const openMenu = (): void => {
    showElements(wrapper, menu);
    if (!mql.matches) menu.classList.add('flex');
    setAria(true);
  };

  const closeMenu = (): void => {
    if (mql.matches) {
      showElements(wrapper, menu);
      setAria(true);
    } else {
      hideElements(wrapper, menu);
      menu.classList.remove('flex');
      setAria(false);
    }
  };

  const apply = (): void => {
    if (mql.matches) {
      showElements(wrapper, menu);
      setAria(true);
    } else {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      expanded ? openMenu() : closeMenu();
    }
  };

  btn.addEventListener('click', () => {
    const isOpen = btn.getAttribute('aria-expanded') === 'true';
    isOpen ? closeMenu() : openMenu();
  });

  // media query change listener with backward compatibility
  const mqHandler = () => apply();
  if ('addEventListener' in mql) mql.addEventListener('change', mqHandler);
  else mql.addListener(mqHandler);

  // ensure sensible initial state
  if (!btn.hasAttribute('aria-expanded')) setAria(false);
  apply();
});
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('[data-collapse-toggle="navbar-menu"]');
  const wrapper = document.getElementById('navbar-menu'); // div-обёртка
  if (!btn || !wrapper) return;

  // находим меню-список: либо внутри div, либо следующий соседний UL
  let menu = wrapper.querySelector('ul');
  if (!menu) {
    const sib = wrapper.nextElementSibling;
    if (sib && sib.tagName === 'UL') menu = sib;
  }
  if (!menu) return;

  const mql = window.matchMedia('(min-width: 1024px)'); // lg breakpoint

  function open() {
    [wrapper, menu].forEach(el => el.classList.remove('hidden'));
    // На мобильных нужен display:flex (на десктопе работает md:flex из разметки)
    if (!mql.matches) menu.classList.add('flex');
    btn.setAttribute('aria-expanded', 'true');
  }

  function close() {
    // На мобильных скрываем; на десктопе — всегда показываем
    if (mql.matches) {
      [wrapper, menu].forEach(el => el.classList.remove('hidden'));
      btn.setAttribute('aria-expanded', 'true');
    } else {
      [wrapper, menu].forEach(el => el.classList.add('hidden'));
      menu.classList.remove('flex');
      btn.setAttribute('aria-expanded', 'false');
    }
  }

  function apply() {
    if (mql.matches) {
      [wrapper, menu].forEach(el => el.classList.remove('hidden'));
      btn.setAttribute('aria-expanded', 'true');
    } else {
      (btn.getAttribute('aria-expanded') === 'true') ? open() : close();
    }
  }

  btn.addEventListener('click', () => {
    const isOpen = btn.getAttribute('aria-expanded') === 'true';
    isOpen ? close() : open();
  });

  if (mql.addEventListener) mql.addEventListener('change', apply);
  else mql.addListener(apply);
  apply();
});
// JavaScript for handling User and Language dropdown menus
document.addEventListener('DOMContentLoaded', function () {
  const userBtn = document.getElementById('user-dropdown-btn');
  const userMenu = document.getElementById('user-dropdown-menu');
  const langBtn = document.getElementById('language-dropdown-btn');
  const langMenu = document.getElementById('language-dropdown-menu');

  // opening/closing User menu only on User avatar button click
  if (userBtn && userMenu) {
    userBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      userMenu.classList.toggle('hidden');
    });
  }

  // opening/closing Language menu only on Language button click
  if (langBtn && langMenu) {
    langBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      langMenu.classList.toggle('hidden');
    });

    // Prevent clicks inside the language menu from closing it
    langMenu.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // Prevent clicks inside the main user menu from closing it
  if (userMenu) {
    userMenu.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }

  // Clicking outside the menus closes both
  document.addEventListener('click', function () {
    if (userMenu) userMenu.classList.add('hidden');
    if (langMenu) langMenu.classList.add('hidden');
  });
});
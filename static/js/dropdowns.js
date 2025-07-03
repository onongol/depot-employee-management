document.addEventListener('DOMContentLoaded', function () {
  const openMenus = new Set();

  // Universal function for any dropdown
  function setupDropdown(btnId, menuId) {
    const btn = document.getElementById(btnId);
    const menu = document.getElementById(menuId);

    if (btn && menu) {
      // Toggle dropdown menu on button click
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        menu.classList.toggle('hidden');
        if (!menu.classList.contains('hidden')) {
          openMenus.add(menu);
        } else {
          openMenus.delete(menu);
        }
      });

      // Click inside the menu does not close it
      menu.addEventListener('click', function (e) {
        e.stopPropagation();
      });

      // Close dropdown after clicking any button inside the menu
      menu.querySelectorAll('button').forEach(function(item) {
        item.addEventListener('click', function () {
          menu.classList.add('hidden');
          openMenus.delete(menu);
        });
      });
    }
  }

  // Global click listener to close all open menus
  document.addEventListener('click', function () {
    openMenus.forEach(menu => {
      menu.classList.add('hidden');
      openMenus.delete(menu);
    });
  });

  // For departments dropdown
  setupDropdown('department-dropdown-btn', 'department-dropdown-menu');
  // For theme dropdown
  setupDropdown('theme-dropdown-btn', 'theme-dropdown-menu');
});
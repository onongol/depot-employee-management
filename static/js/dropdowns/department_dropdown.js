// Manages dropdown menus: toggles visibility, prevents click propagation, auto-closes on outside clicks, and closes menus when internal buttons are clicked; tracks open menus in a Set.

document.addEventListener('DOMContentLoaded', function () {
  const openMenus = new Set();
  // Universal function for any dropdown
  function setupDropdown(btnId, menuId) {
    const btn = document.getElementById(btnId);
    const menu = document.getElementById(menuId);
    if (!btn) console.warn(`Button with id "${btnId}" not found`);
    if (!menu) console.warn(`Menu with id "${menuId}" not found`);
    // Only proceed if both button and menu exist
    if (btn && menu) {
      // Toggle dropdown menu on button click
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (menu.classList.contains('hidden')) {
          openMenu(menu);
        } else {
          closeMenu(menu);
        }
      });

      // Click inside the menu does not close it
      menu.addEventListener('click', function (e) {
        e.stopPropagation();
      });
      
      // Close dropdown after clicking any button inside the menu
      menu.querySelectorAll('button').forEach(function(item) {
        item.addEventListener('click', function () {
          closeMenu(menu);
        });
      });
    }
  }

  // Global click listener to close all open menus
  document.addEventListener('click', function () {
    openMenus.forEach(menu => {
      closeMenu(menu);
    });
  });

  // For dropdown menu
  setupDropdown('department-dropdown-btn', 'department-dropdown-menu');

  // Helper functions to open/close menus without animation
  function openMenu(menu) {
    if (!menu) return;
    menu.classList.remove('hidden');
    openMenus.add(menu);
  }

  // Close menu instantly (no fade-out animation)
  function closeMenu(menu) {
    if (!menu) return;
    menu.classList.add('hidden');
    openMenus.delete(menu);
  }
});
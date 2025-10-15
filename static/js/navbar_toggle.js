document.addEventListener('DOMContentLoaded', () => {
  // Find the mobile menu toggle button by its data attribute
  const btn = document.querySelector('[data-collapse-toggle="navbar-menu"]');
  // Find the menu wrapper by its ID
  const wrapper = document.getElementById('navbar-menu'); // menu container div
  if (!btn || !wrapper) return; // Exit if button or menu is not found

  // Find the menu list (ul) inside the wrapper or as a sibling
  let menu = wrapper.querySelector('ul');
  if (!menu) {
    const sib = wrapper.nextElementSibling;
    if (sib && sib.tagName === 'UL') menu = sib;
  }
  if (!menu) return; // Exit if menu list is not found

  // Create a media query for desktop breakpoint (lg)
  const mql = window.matchMedia('(min-width: 1024px)'); // lg breakpoint

  // Function to open the mobile menu
  function open() {
    // Remove 'hidden' class to show menu and wrapper
    [wrapper, menu].forEach(el => el.classList.remove('hidden'));
    // On mobile, set display to flex for menu list
    if (!mql.matches) menu.classList.add('flex');
    // Set aria-expanded to true for accessibility
    btn.setAttribute('aria-expanded', 'true');
  }

  // Function to close the mobile menu
  function close() {
    // On desktop, always show menu and wrapper
    if (mql.matches) {
      [wrapper, menu].forEach(el => el.classList.remove('hidden'));
      btn.setAttribute('aria-expanded', 'true');
    } else {
      // On mobile, hide menu and wrapper
      [wrapper, menu].forEach(el => el.classList.add('hidden'));
      // Remove flex class from menu list
      menu.classList.remove('flex');
      // Set aria-expanded to false for accessibility
      btn.setAttribute('aria-expanded', 'false');
    }
  }

  // Function to apply menu visibility based on screen size
  function apply() {
    if (mql.matches) {
      // On desktop, always show menu and wrapper
      [wrapper, menu].forEach(el => el.classList.remove('hidden'));
      btn.setAttribute('aria-expanded', 'true');
    } else {
      // On mobile, show or hide menu based on aria-expanded state
      (btn.getAttribute('aria-expanded') === 'true') ? open() : close();
    }
  }

  // Toggle menu open/close on button click
  btn.addEventListener('click', () => {
    const isOpen = btn.getAttribute('aria-expanded') === 'true';
    isOpen ? close() : open();
  });

  // Listen for screen size changes and apply menu visibility
  if (mql.addEventListener) mql.addEventListener('change', apply);
  else mql.addListener(apply); // Fallback for older browsers

  // Initial menu visibility setup
  apply();
});
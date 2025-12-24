// Removes form validation UI when users edit inputs: clears red-border classes and deletes associated error message elements (id + '_error') on input events.

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input, select, textarea').forEach(function (el) {
    el.addEventListener('input', function () {
      // Delete red border
      el.classList.remove(
        'border-red-600', 'focus:ring-red-600', 'focus:border-red-600', 'focus:text-red-600', 'dark:border-red-600', 'dark:focus:ring-red-600', 'dark:focus:border-red-600', 'dark:focus:text-red-600'
      );
      // Find and hide error
      const errorDiv = document.getElementById(el.id + '_error');
      if (errorDiv) errorDiv.remove();
    });
  });
});
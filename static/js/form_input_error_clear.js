// Clear form input errors on user input
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input, select, textarea').forEach(function (el) {
    el.addEventListener('input', function () {
      // Delete red border
      el.classList.remove('border-red-600', 'focus:ring-red-600', 'focus:border-red-600', 'focus:text-red-600');
      // Find and hide error
      const errorDiv = document.getElementById(el.id + '_error');
      if (errorDiv) errorDiv.remove();
    });
  });
});
// Toggle password visibility for any password input with matching eye icons
function togglePasswordVisibility(inputId) {
  const input = document.getElementById(inputId);
  const eye = document.getElementById('eye-' + inputId);
  const eyeOff = document.getElementById('eye-off-' + inputId);

  // Check for required elements before changing properties
  if (!input) {
    console.warn(`Password input with id "${inputId}" not found`);
    return;
  }
  if (!eye) {
    console.warn(`Eye icon with id "eye-${inputId}" not found`);
    return;
  }
  if (!eyeOff) {
    console.warn(`Eye-off icon with id "eye-off-${inputId}" not found`);
    return;
  }
}

// Universal handler for all password fields
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input[type="password"]').forEach(input => {
    const inputId = input.id;
    if (inputId) {
      document.getElementById('eye-' + inputId)?.addEventListener('click', () => togglePasswordVisibility(inputId));
      document.getElementById('eye-off-' + inputId)?.addEventListener('click', () => togglePasswordVisibility(inputId));
    }
  });
});

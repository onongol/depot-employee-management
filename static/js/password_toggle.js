// Toggle password visibility
function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  const eye = document.getElementById('eye-' + inputId);
  const eyeOff = document.getElementById('eye-off-' + inputId);
  // Check current type and toggle
  if (input.type === "password") {
    input.type = "text";
    eye.classList.add('hidden');
    eyeOff.classList.remove('hidden');
  } else {
    input.type = "password";
    eye.classList.remove('hidden');
    eyeOff.classList.add('hidden');
  }
}
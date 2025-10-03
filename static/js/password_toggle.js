// Store auto-hide timers by input id
const autoHideTimers = new Map();

// Toggle password visibility (with optional auto-hide)
// revealMs (optional) — reveal duration in ms. If not provided, it can be set on the button via data-reveal-ms.
function togglePasswordVisibility(inputId, btn, revealMs) {
  const input = document.getElementById(inputId);
  const eye = document.getElementById('eye-' + inputId);
  const eyeOff = document.getElementById('eye-off-' + inputId);

  // Clear previous timer if present
  const prevTimer = autoHideTimers.get(inputId);
  if (prevTimer) {
    clearTimeout(prevTimer);
    autoHideTimers.delete(inputId);
  }

  // Determine auto-hide duration
  const paramMs = Number(revealMs);
  const dataMs = Number(btn?.dataset?.revealMs);
  const autoHideMs =
    (Number.isFinite(paramMs) && paramMs > 0) ? paramMs :
    (Number.isFinite(dataMs) && dataMs > 0) ? dataMs : 0;

  if (input.type === "password") {
    // Reveal
    input.type = "text";
    eye?.classList.add('hidden');
    eyeOff?.classList.remove('hidden');
    if (btn) {
      btn.setAttribute('aria-label', 'Hide password');
      btn.setAttribute('aria-pressed', 'true');
    }

    // Auto-hide by timer (if specified)
    if (autoHideMs > 0) {
      const t = setTimeout(() => {
        input.type = "password";
        eye?.classList.remove('hidden');
        eyeOff?.classList.add('hidden');
        if (btn) {
          btn.setAttribute('aria-label', 'Show password');
          btn.setAttribute('aria-pressed', 'false');
        }
        autoHideTimers.delete(inputId);
      }, autoHideMs);
      autoHideTimers.set(inputId, t);
    }
  } else {
    // Hide immediately
    input.type = "password";
    eye?.classList.remove('hidden');
    eyeOff?.classList.add('hidden');
    if (btn) {
      btn.setAttribute('aria-label', 'Show password');
      btn.setAttribute('aria-pressed', 'false');
    }
  }
}
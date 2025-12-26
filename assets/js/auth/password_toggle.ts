// Toggles password visibility with optional auto-hide: reveals/hides input, updates icons and ARIA attributes, and manages per-input auto-hide timers.

(function () {
  type RevealTimer = number;

  interface ToggleButton extends HTMLElement {
    dataset: DOMStringMap & { revealMs?: string; showLabel?: string; hideLabel?: string };
  }

  const autoHideTimers = new Map<string, RevealTimer>();

  function getInputElement(id: string): HTMLInputElement | null {
    const el = document.getElementById(id);
    return el instanceof HTMLInputElement ? el : null;
  }

  function getIcon(id: string, suffix: 'eye' | 'eye-off'): SVGElement | null {
    const el = document.getElementById(`${suffix}-${id}`);
    return el instanceof SVGElement ? el : null;
  }

  function setButtonState(btn: ToggleButton | null, revealed: boolean): void {
    if (!btn) return;
    const showLabel = btn.dataset.showLabel ?? 'Show password';
    const hideLabel = btn.dataset.hideLabel ?? 'Hide password';
    btn.setAttribute('aria-pressed', revealed ? 'true' : 'false');
    btn.setAttribute('aria-label', revealed ? hideLabel : showLabel);
  }

  function toggleIcons(inputId: string, revealed: boolean): void {
    const eye = getIcon(inputId, 'eye');
    const eyeOff = getIcon(inputId, 'eye-off');
    eye?.classList.toggle('hidden', revealed);
    eyeOff?.classList.toggle('hidden', !revealed);
  }

  /**
   * Toggle password visibility for a given input id.
   * @param inputId - id of the password input
   * @param btn - optional toggle button element (used for dataset and ARIA)
   * @param revealMs - optional override ms to auto-hide (positive number), 0 = no auto-hide
   */
  function togglePasswordVisibility(inputId: string, btn?: ToggleButton | null, revealMs?: number): void {
    const input = getInputElement(inputId);
    if (!input) {
      console.warn(`togglePasswordVisibility: input "${inputId}" not found`);
      return;
    }

    // Clear previous timer if present
    const prev = autoHideTimers.get(inputId);
    if (prev !== undefined) {
      clearTimeout(prev);
      autoHideTimers.delete(inputId);
    }

    const paramMs = typeof revealMs === 'number' && Number.isFinite(revealMs) ? revealMs : 0;
    const dataMs = btn && btn.dataset?.revealMs ? Number(btn.dataset.revealMs) || 0 : 0;
    const autoHideMs = paramMs > 0 ? paramMs : dataMs > 0 ? dataMs : 0;

    const isPassword = input.type === 'password';

    if (isPassword) {
      // reveal
      input.type = 'text';
      toggleIcons(inputId, true);
      setButtonState(btn ?? null, true);

      if (autoHideMs > 0) {
        const t = window.setTimeout(() => {
          input.type = 'password';
          toggleIcons(inputId, false);
          setButtonState(btn ?? null, false);
          autoHideTimers.delete(inputId);
        }, autoHideMs) as unknown as RevealTimer;
        autoHideTimers.set(inputId, t);
      }
    } else {
      // hide immediately
      input.type = 'password';
      toggleIcons(inputId, false);
      setButtonState(btn ?? null, false);
    }
  }

  // Expose to global for existing templates that call this function
  declare global {
    interface Window {
      togglePasswordVisibility?: (inputId: string, btn?: ToggleButton | null, revealMs?: number) => void;
    }
  }
  window.togglePasswordVisibility = togglePasswordVisibility;
})();
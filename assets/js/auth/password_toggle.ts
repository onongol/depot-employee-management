/**
 * Password Visibility Toggle:
 * Uses Event Delegation to manage password visibility.
 * Decouples logic from HTML attributes via data-selectors.
 */
type RevealTimer = number;

const PWD_TOGGLE_SELECTORS = {
  button: "[data-password-toggle]",
  eyeIcon: '[data-icon="eye"]',
  eyeOffIcon: '[data-icon="eye-off"]',
} as const;

const PWD_TOGGLE_TYPES = {
  password: "password",
  text: "text",
} as const;

const PWD_TOGGLE_ATTRS = {
  ariaPressed: "aria-pressed",
  ariaLabel: "aria-label",
} as const;

const PWD_TOGGLE_DATA = {
  revealMs: "revealMs",
  showLabel: "showLabel",
  hideLabel: "hideLabel",
  inputId: "inputId",
} as const;

const PWD_TOGGLE_CLASSES = {
  hidden: "hidden",
} as const;

const PWD_TOGGLE_VALUES = {
  ariaTrue: "true",
  ariaFalse: "false",
  defaultShowLabel: "Show password",
  defaultHideLabel: "Hide password",
} as const;

// Prevents double-script execution
const PWD_TOGGLE_INIT = {
  attr: "data-password-toggle-init",
} as const;

interface ToggleButton extends HTMLButtonElement {
  dataset: DOMStringMap & {
    revealMs?: string;
    showLabel?: string;
    hideLabel?: string;
    inputId?: string;
  };
}

const autoHideTimers = new Map<string, RevealTimer>();

function getInputElement(id: string): HTMLInputElement | null {
  const el = document.getElementById(id);
  return el instanceof HTMLInputElement ? el : null;
}

/**
 * Synchronizes ARIA attributes for screen reader accessibility.
 */
function setButtonState(btn: ToggleButton | null, revealed: boolean): void {
  if (!btn) return;

  const showLabel =
    btn.dataset[PWD_TOGGLE_DATA.showLabel] ??
    PWD_TOGGLE_VALUES.defaultShowLabel;
  const hideLabel =
    btn.dataset[PWD_TOGGLE_DATA.hideLabel] ??
    PWD_TOGGLE_VALUES.defaultHideLabel;

  btn.setAttribute(
    PWD_TOGGLE_ATTRS.ariaPressed,
    revealed ? PWD_TOGGLE_VALUES.ariaTrue : PWD_TOGGLE_VALUES.ariaFalse,
  );
  btn.setAttribute(
    PWD_TOGGLE_ATTRS.ariaLabel,
    revealed ? hideLabel : showLabel,
  );
}

/**
 * Toggles visibility of icons scoped within the clicked button.
 */
function toggleIcons(btn: ToggleButton | null, revealed: boolean): void {
  if (!btn) return;

  const eye = btn.querySelector<SVGElement>(PWD_TOGGLE_SELECTORS.eyeIcon);
  const eyeOff = btn.querySelector<SVGElement>(PWD_TOGGLE_SELECTORS.eyeOffIcon);

  eye?.classList.toggle(PWD_TOGGLE_CLASSES.hidden, revealed);
  eyeOff?.classList.toggle(PWD_TOGGLE_CLASSES.hidden, !revealed);
}

function resolveInputId(btn: ToggleButton): string | null {
  const direct = btn.dataset[PWD_TOGGLE_DATA.inputId]?.trim();
  return direct || null;
}

/**
 * Main logic to flip input type and manage auto-hide timers.
 */
function togglePasswordVisibility(
  inputId: string,
  btn?: ToggleButton | null,
  revealMs?: number,
): void {
  const input = getInputElement(inputId);
  if (!input) return;

  // Reset any existing timer for this specific input
  const existingTimerId = autoHideTimers.get(inputId);
  if (existingTimerId !== undefined) {
    window.clearTimeout(existingTimerId);
    autoHideTimers.delete(inputId);
  }

  const paramMs =
    typeof revealMs === "number" && Number.isFinite(revealMs) ? revealMs : 0;
  const dataMs = btn?.dataset[PWD_TOGGLE_DATA.revealMs]
    ? Number(btn.dataset[PWD_TOGGLE_DATA.revealMs]) || 0
    : 0;
  const autoHideMs = paramMs > 0 ? paramMs : dataMs;

  const isPassword = input.type === PWD_TOGGLE_TYPES.password;

  if (isPassword) {
    input.type = PWD_TOGGLE_TYPES.text;
    toggleIcons(btn ?? null, true);
    setButtonState(btn ?? null, true);

    if (autoHideMs > 0) {
      const autoHideTimerId: RevealTimer = window.setTimeout(() => {
        input.type = PWD_TOGGLE_TYPES.password;
        toggleIcons(btn ?? null, false);
        setButtonState(btn ?? null, false);
        autoHideTimers.delete(inputId);
      }, autoHideMs);

      autoHideTimers.set(inputId, autoHideTimerId);
    }
  } else {
    input.type = PWD_TOGGLE_TYPES.password;
    toggleIcons(btn ?? null, false);
    setButtonState(btn ?? null, false);
  }
}

/**
 * Initialize Event Delegation.
 * Using a guard on the <html> element to ensure logic is bound only once.
 */
if (!document.documentElement.hasAttribute(PWD_TOGGLE_INIT.attr)) {
  document.documentElement.setAttribute(PWD_TOGGLE_INIT.attr, "true");

  document.addEventListener("DOMContentLoaded", () => {
    /**
     * Global click listener handles all current and future toggle buttons.
     */
    document.addEventListener("click", (event: Event) => {
      const target = event.target;
      if (!(target instanceof Element)) return;

      // Search for the button in the event bubbling path
      const btn = target.closest<ToggleButton>(PWD_TOGGLE_SELECTORS.button);
      if (!btn) return;

      const inputId = resolveInputId(btn);
      if (!inputId) return;

      togglePasswordVisibility(inputId, btn);
    });
  });
}

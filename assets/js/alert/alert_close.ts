/**
 * Global Alert Management (TypeScript, strict).
 * Uses event delegation to handle closing alerts.
 * Compatible with dynamically injected alerts (AJAX/JS).
 */

const ALERT_CLOSE_SELECTORS = {
  alert: "[data-alert-close]",
} as const;

const ALERT_CLOSE_ROLE = '[role="alert"]' as const;

/**
 * Global click listener for alert close buttons.
 */
document.addEventListener("click", (event) => {
  const target = event.target;

  // Ensure we are dealing with a DOM element
  if (!(target instanceof Element)) return;

  // Find the closest button or trigger with the close attribute
  const closeBtn = target.closest<HTMLElement>(ALERT_CLOSE_SELECTORS.alert);
  if (!closeBtn) return;

  // Find the actual alert container to be removed
  event.preventDefault();

  const alert = closeBtn.closest(ALERT_CLOSE_ROLE);

  if (alert) {
    alert.remove();
  }
});

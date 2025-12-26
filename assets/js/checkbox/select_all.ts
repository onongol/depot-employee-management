type CheckboxLike = HTMLInputElement;

/** Safe CSS.escape accessor without using `any` */
const cssEscape = ((): ((s: string) => string) => {
  if (typeof CSS !== 'undefined' && (CSS as unknown as { escape?: (s: string) => string }).escape) {
    return (CSS as unknown as { escape: (s: string) => string }).escape;
  }
  return (s: string) => s;
})();

function resolveCheckboxes(input: string | Iterable<CheckboxLike> | null | undefined): CheckboxLike[] {
  if (!input) return [];
  if (typeof input === 'string') {
    const selector = `input[name="${cssEscape(input)}"]`;
    return Array.from(document.querySelectorAll<HTMLInputElement>(selector));
  }
  return Array.from(input);
}

/**
 * Toggle all visible checkboxes sharing the same name.
 * - source: checkbox element (or any object with `.checked`) that controls the group
 * - name: string name OR NodeList/Array of checkboxes
 */
export function toggleAllVisible(
  source: CheckboxLike | { checked?: boolean } | null,
  name: string | Iterable<CheckboxLike> | null | undefined
): void {
  const checkboxList = resolveCheckboxes(name);
  if (checkboxList.length === 0) {
    // silent no-op (keeps backward compatibility)
    return;
  }
  const shouldCheck = !!(source && (source as { checked?: boolean }).checked);

  checkboxList.forEach((cb) => {
    if (cb instanceof HTMLInputElement && cb.type === 'checkbox' && cb.offsetParent !== null) {
      cb.checked = shouldCheck;
      cb.dispatchEvent(new Event('change', { bubbles: true }));
    }
  });
}

// expose for legacy templates
declare global {
  interface Window {
    toggleAllVisible?: typeof toggleAllVisible;
  }
}

// Make sure the runtime attaches the function to window
window.toggleAllVisible = toggleAllVisible;
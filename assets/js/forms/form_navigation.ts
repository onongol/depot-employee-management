// Provides keyboard form navigation: Enter focuses the next input (Shift+Enter goes back), skips textareas/hidden/disabled elements, and submits when Enter is pressed on the last field for forms with IDs "createForm" and "updateForm".

document.addEventListener('DOMContentLoaded', () => {
  const formIds: readonly string[] = ['createForm', 'updateForm'];

  const isVisibleAndFocusable = (el: HTMLElement): boolean =>
    el.offsetParent !== null && el.tabIndex !== -1;

  function getFocusableInputs(form: HTMLFormElement): HTMLElement[] {
    const nodeList = form.querySelectorAll(
      'input:not([type="hidden"]):not([disabled]), select:not([disabled]), textarea:not([disabled])'
    ) as NodeListOf<HTMLElement>;
    return Array.from(nodeList).filter(isVisibleAndFocusable);
  }

  formIds.forEach((formId) => {
    const form = document.getElementById(formId) as HTMLFormElement | null;
    if (!form) return;

    form.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key !== 'Enter') return;

      const active = document.activeElement as Element | null;
      if (active && active.tagName.toLowerCase() === 'textarea') return;

      event.preventDefault();

      const inputs = getFocusableInputs(form);
      const currentIndex = active ? inputs.indexOf(active as HTMLElement) : -1;

      if (event.shiftKey) {
        if (currentIndex > 0) {
          inputs[currentIndex - 1].focus();
        }
        return;
      }

      // Forward navigation or submit if last
      if (currentIndex > -1 && currentIndex < inputs.length - 1) {
        inputs[currentIndex + 1].focus();
      } else if (currentIndex === inputs.length - 1) {
        // submit form: use requestSubmit when available for modern behavior
        (form.requestSubmit ? form.requestSubmit() : form.submit());
      } else if (inputs.length > 0) {
        // fallback: focus first focusable input
        inputs[0].focus();
      }
    });
  });
});
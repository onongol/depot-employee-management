/**
 * Handle work_date input: update URL param and navigate.
 * Strict types, safe DOM access, no `any`.
 */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('work_date') as HTMLInputElement | null;
  if (!input) return;

  const applyWorkDate = (val: string | null): void => {
    if (!val) return;
    try {
      const url = new URL(window.location.href);
      const params = url.searchParams;
      params.set('work_date', val);
      params.delete('page'); // reset pagination on date change
      url.search = params.toString();
      window.location.href = url.toString();
    } catch (err) {
      // Ignore malformed URL / navigation errors in constrained environments
      // (keeps behavior resilient)
      // console.warn(err);
    }
  };

  input.addEventListener('change', function (this: HTMLInputElement) {
    applyWorkDate(this.value ?? null);
  });

  input.addEventListener('keydown', function (this: HTMLInputElement, e: KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault();
      applyWorkDate(this.value ?? null);
    }
  });
});
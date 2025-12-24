// Handles the work date input: on change or Enter it updates the URL's work_date param, clears page, and navigates to the new URL.

(function() {
  const input = document.getElementById('work_date');
  if (!input) return;

  function applyWorkDate(val) {
    if (!val) return;
    const url = new URL(window.location.href);
    const params = url.searchParams;
    params.set('work_date', val);
    params.delete('page'); // reset pagination on date change
    url.search = params.toString();
    window.location.href = url.toString();
  }

  // on change of the date input
  input.addEventListener('change', function() {
    applyWorkDate(this.value);
  });

  // on Enter key press
  input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      applyWorkDate(this.value);
    }
  });
})();
// Creates a form navigation script that allows users to navigate through form fields using the Enter key.
document.getElementById('create_form').addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    // Only move to next field if not inside a textarea
    if (document.activeElement.tagName.toLowerCase() !== 'textarea') {
      event.preventDefault();
      const inputs = Array.from(this.querySelectorAll('input, select, textarea'));
      const currentFocus = document.activeElement;
      const currentIndex = inputs.indexOf(currentFocus);
      const nextIndex = (currentIndex + 1) % inputs.length;
      inputs[nextIndex].focus();
    }
  }
});

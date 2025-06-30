// Universal form navigation: move to next input/select/textarea on Enter (except textarea itself)
document.addEventListener('DOMContentLoaded', function () {
  // List all form IDs you want to enable navigation for
  const formIds = ['createForm', 'updateForm'];

  formIds.forEach(function (formId) {
    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('keydown', function (event) {
        if (
          event.key === 'Enter' &&
          document.activeElement.tagName.toLowerCase() !== 'textarea'
        ) {
          event.preventDefault();
          const inputs = Array.from(
            this.querySelectorAll('input, select, textarea')
          );
          const currentFocus = document.activeElement;
          const currentIndex = inputs.indexOf(currentFocus);
          const nextIndex = (currentIndex + 1) % inputs.length;
          inputs[nextIndex].focus();
        }
      });
    }
  });
});
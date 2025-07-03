// Universal form navigation: move to next input/select/textarea on Enter (except textarea itself)
document.addEventListener('DOMContentLoaded', function () {
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
            this.querySelectorAll(
              'input:not([type=hidden]):not([disabled]), select:not([disabled]), textarea:not([disabled])'
            )
          ).filter((el) => el.offsetParent !== null); // только видимые
          const currentFocus = document.activeElement;
          const currentIndex = inputs.indexOf(currentFocus);
          if (currentIndex > -1 && currentIndex < inputs.length - 1) {
            inputs[currentIndex + 1].focus();
          }
        }
      });
    }
  });
});
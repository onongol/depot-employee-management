// Provides keyboard form navigation: Enter focuses the next input (Shift+Enter goes back), skips textareas/hidden/disabled elements, and submits when Enter is pressed on the last field for forms with IDs "createForm" and "updateForm".

document.addEventListener('DOMContentLoaded', function () {
  const formIds = ['createForm', 'updateForm'];
  // Add more form IDs as needed
  formIds.forEach(function (formId) {
    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('keydown', function (event) {
        // Handle Enter key navigation, except inside textarea
        if (
          event.key === 'Enter' &&
          document.activeElement.tagName.toLowerCase() !== 'textarea'
        ) {
          event.preventDefault();
          // Only visible and focusable elements (tabindex !== -1)
          const inputs = Array.from(
            this.querySelectorAll(
              'input:not([type=hidden]):not([disabled]), select:not([disabled]), textarea:not([disabled])'
            )
          ).filter((el) => el.offsetParent !== null && el.tabIndex !== -1); // Only visible and focusable elements
          const currentFocus = document.activeElement;
          const currentIndex = inputs.indexOf(currentFocus);
          if (event.shiftKey) {
            // Move backward on Shift+Enter
            if (currentIndex > 0) {
              inputs[currentIndex - 1].focus();
            }
          } else {
            // Move forward on Enter
            if (currentIndex > -1 && currentIndex < inputs.length - 1) {
              inputs[currentIndex + 1].focus();
            } else if (currentIndex === inputs.length - 1) {
              // Handle Enter in the last field: submit the form
              form.requestSubmit ? form.requestSubmit() : form.submit();
            }
          }
        }
      });
    }
  });
});
// Update form navigation and save confirmation modal script
document.addEventListener("DOMContentLoaded", function () {
  const saveModal = document.getElementById("saveModal");
  const saveObjectDetails = document.getElementById("saveObjectDetails");
  const confirmSaveButton = document.getElementById("confirmSaveButton");
  const updateForm = document.getElementById("updateForm");
  if (saveModal) {
    saveModal.addEventListener("show.bs.modal", function () {
      const objectName = saveModal.getAttribute("data-object-name");
      if (saveObjectDetails) {
        saveObjectDetails.textContent = objectName;
      }
    });
  }
  if (confirmSaveButton && updateForm) {
    confirmSaveButton.addEventListener("click", function () {
      updateForm.submit();
    });
  }
  if (updateForm) {
    updateForm.addEventListener("keydown", function (event) {
      if (
        event.key === "Enter" &&
        document.activeElement.tagName.toLowerCase() !== "textarea"
      ) {
        event.preventDefault();
        const inputs = Array.from(
          this.querySelectorAll("input, select, textarea")
        );
        const currentFocus = document.activeElement;
        const currentIndex = inputs.indexOf(currentFocus);
        const nextIndex = (currentIndex + 1) % inputs.length;
        inputs[nextIndex].focus();
      }
    });
  }
});
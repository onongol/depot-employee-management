// Delete and Update Modal Logic
document.addEventListener("DOMContentLoaded", function () {
  // Delete Modal Logic
  const deleteModal = document.getElementById("deleteModal");
  if (deleteModal) {
    deleteModal.addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const itemUrl = button.getAttribute("data-url");
      const deleteForm = document.getElementById("deleteForm");
      const deleteDetails = document.getElementById("deleteDetails");
      deleteForm.action = itemUrl; // Update the URL dynamically
      deleteDetails.textContent = `${itemId} ${itemName}`;
    });
  }
  // Update Modal Logic
  const updateModal = document.getElementById("updateModal");
  if (updateModal) {
    updateModal.addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const updateUrl = button.getAttribute("data-url");
      const updateLink = document.getElementById("updateLink");
      const updateDetails = document.getElementById("updateDetails");
      updateLink.href = updateUrl; // Update the URL dynamically
      updateDetails.textContent = `${itemId} ${itemName}`;
    });
  }
});
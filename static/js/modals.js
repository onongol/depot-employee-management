// DaisyUI Modal Logic for Delete and Update

document.addEventListener("DOMContentLoaded", function () {
  // Edit
  document.querySelectorAll('button[aria-label^="Edit"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const updateUrl = button.getAttribute("data-url");
      document.getElementById("updateLink").href = updateUrl;
      document.getElementById("updateDetails").textContent = `${itemId}/${itemName}`;
      document.getElementById('updateModal').classList.remove('hidden'); // исправлено
    });
  });

  // Delete
  document.querySelectorAll('button[aria-label^="Delete"]').forEach(function (button) {
    button.addEventListener("click", function () {
      const itemId = button.getAttribute("data-id");
      const itemName = button.getAttribute("data-name");
      const itemUrl = button.getAttribute("data-url");
      document.getElementById("deleteForm").action = itemUrl;
      document.getElementById("deleteDetails").textContent = `${itemId}/${itemName}`;
      document.getElementById('deleteModal').classList.remove('hidden'); // исправлено
    });
  });
});
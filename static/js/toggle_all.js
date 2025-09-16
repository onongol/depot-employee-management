// Function to toggle all visible checkboxes with the same name
function toggleAllVisible(source, name) {
  const checkboxes = document.getElementsByName(name);
  for (let i = 0, n = checkboxes.length; i < n; i++) {
    // Only check/uncheck if checkbox is visible (not filtered out)
    if (checkboxes[i].offsetParent !== null) {
      checkboxes[i].checked = source.checked;
    }
  }
}
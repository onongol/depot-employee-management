// Function to toggle all checkboxes with the same name  
function toggleAll(source, name) {
  const checkboxes = document.getElementsByName(name);
  for (let i = 0, n = checkboxes.length; i < n; i++) {
    checkboxes[i].checked = source.checked;
  }
}
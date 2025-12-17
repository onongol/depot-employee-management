// Toggles all visible checkboxes sharing the same name (used for "select all" controls); ignores hidden elements and warns if no checkboxes found.

function toggleAllVisible(source, name) {
  const checkboxes = document.getElementsByName(name);
  if (!checkboxes || checkboxes.length === 0) {
    console.warn(`No checkboxes found with name "${name}"`);
    return;
  }
  for (let i = 0, n = checkboxes.length; i < n; i++) {
    const cb = checkboxes[i];
    // Only check/uncheck if element is a visible checkbox
    if (
      cb.type === 'checkbox' &&
      cb.offsetParent !== null
    ) {
      cb.checked = source.checked;
    }
  }
}
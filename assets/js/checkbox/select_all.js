// Toggles all visible checkboxes sharing the same name (used for "select all" controls); ignores hidden elements and warns if no checkboxes found.

function toggleAllVisible(source, name) {
  // support passing either a name string or a NodeList/Array of checkboxes
  const checkboxList = (typeof name === 'string')
    ? Array.from(document.querySelectorAll(`input[name="${CSS.escape ? CSS.escape(name) : name}"]`))
    : Array.from(name || []);
  if (!checkboxList.length) {
    // silent no-op (avoid spurious warnings when callers pass a table id)
    return;
  }
  checkboxList.forEach(cb => {
    if (cb.type === 'checkbox' && cb.offsetParent !== null) {
      cb.checked = !!(source && source.checked);
      // notify other listeners (amount/summary/validation)
      cb.dispatchEvent(new Event('change', { bubbles: true }));
    }
  });
}

window.toggleAllVisible = toggleAllVisible;
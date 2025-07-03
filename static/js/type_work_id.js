// Ensure select[name="type_work"] has id="type_work" for compatibility with other scripts
document.addEventListener('DOMContentLoaded', function () {
  const typeWork = document.querySelector('select[name="type_work"]');
  if (typeWork && typeWork.id !== 'type_work') {
    typeWork.id = 'type_work';
  }
});
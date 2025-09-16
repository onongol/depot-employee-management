// Ensure all select[name="type_work"] elements have id="type_work" for compatibility with other scripts
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('select[name="type_work"]').forEach(function(typeWork) {
    if (typeWork && typeWork.id !== 'type_work') {
      typeWork.id = 'type_work';
    }
  });
});
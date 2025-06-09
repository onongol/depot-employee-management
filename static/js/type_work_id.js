document.addEventListener('DOMContentLoaded', function () {
  var typeWork = document.querySelector('select[name="type_work"]');
  if (typeWork && typeWork.id !== 'type_work') {
    typeWork.id = 'type_work';
  }
});
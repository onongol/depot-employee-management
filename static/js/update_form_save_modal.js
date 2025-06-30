// Save button
document.getElementById('saveButton').addEventListener('click', function() {
document.getElementById('saveModal').classList.remove('hidden');
});
document.getElementById('confirmSaveButton').addEventListener('click', function() {
document.getElementById('updateForm').submit();
});

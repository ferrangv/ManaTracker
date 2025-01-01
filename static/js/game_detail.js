function confirmDelete() {
    if (confirm("Are you sure you want to delete this game?")) {
        document.getElementById('delete-form').submit();
    }
}


function toggleEditForm() {
    const editForm = document.getElementById('edit-form-container');
    if (editForm.classList.contains('hidden')) {
        editForm.classList.remove('hidden');
    } else {
        editForm.classList.add('hidden');
    }
}

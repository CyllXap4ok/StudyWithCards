document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('userDropdown').addEventListener('click', function() {
        document.getElementById('dropdownMenu').classList.toggle('show');
    });

    // Закрытие меню при клике вне его
    window.addEventListener('click', function(event) {
        if (!event.target.closest('#userDropdown')) {
            document.getElementById('dropdownMenu').classList.remove('show');
        }
    });
});
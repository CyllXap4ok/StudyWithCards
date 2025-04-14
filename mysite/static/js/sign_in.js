document.querySelectorAll('.input-field input').forEach(input => {
    // Устанавливаем черную границу при наличии значения
    if (input.value) {
        input.style.borderBottomColor = '#000';
    }

    input.addEventListener('focus', function() {
        this.style.borderBottomColor = '#000';
    });

    input.addEventListener('blur', function() {
        if (!this.value) {
            this.style.borderBottomColor = '#ccc';
        }
    });
});
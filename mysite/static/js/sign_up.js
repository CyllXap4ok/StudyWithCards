document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('id_avatar');
    const preview = document.getElementById('user-icon-preview');

    avatarInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Проверяем тип файла
            if (!file.type.match('image.*')) {
                alert('Пожалуйста, выберите изображение (PNG или JPEG)');
                return;
            }

            const reader = new FileReader();

            reader.onload = function(e) {
                preview.style.backgroundImage = `url('${e.target.result}')`;
            }

            reader.readAsDataURL(file);
        }
    });
});
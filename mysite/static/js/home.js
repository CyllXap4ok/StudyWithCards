document.addEventListener('DOMContentLoaded', function() {
    // Запись элементов в переменные для дальнейшего обращения
    const deleteButtons = document.querySelectorAll('.delete-card-btn');
    const modal = document.getElementById('deleteModal');
    const cancelBtn = modal.querySelector('.cancel-btn');
    const deleteConfirmBtn = modal.querySelector('.delete-confirm-btn');

    let currentCardsetId = null;
    let currentCardsetElement = null;

    // Показываем кнопку удаления при наведении
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            currentCardsetId = this.getAttribute('data-cardset-id');
            currentCardsetElement = this.closest('.cardset-item-container');
            modal.classList.add('show');
        });
    });

    function closeModal() {
        modal.classList.remove('show');
        currentCardsetId = null;
        currentCardsetElement = null;
    }

    cancelBtn.addEventListener('click', closeModal);

    // Закрытие при клике вне всплывающего окна
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Подтверждение удаления
    deleteConfirmBtn.addEventListener('click', function() {
        if (!currentCardsetId) return;

        // AJAX запрос для удаления
        fetch(`/cards/delete/${currentCardsetId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.success) {
                // Полное удаление элемента и перезагрузка страницы
                window.location.reload();
            } else if (data) {
                alert('Ошибка при удалении: ' + (data.error || 'Неизвестная ошибка'));
            }
            closeModal();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при удалении');
            closeModal();
        });
    });
});
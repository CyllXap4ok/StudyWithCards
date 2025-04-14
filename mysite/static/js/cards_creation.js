document.addEventListener('DOMContentLoaded', function() {
    // Добавляем пустую карточку при загрузке страницы
    addCard();

    // Обработчики для кнопок
    document.getElementById('addCardBtn').addEventListener('click', addCard);
    document.getElementById('saveSetBtn').addEventListener('click', showSaveModal);
    document.getElementById('cancelSaveBtn').addEventListener('click', hideSaveModal);
    document.getElementById('confirmSaveBtn').addEventListener('click', saveCardSet);

    // Обработчик для поля ввода названия набора
    const nameInput = document.getElementById('setNameInput');
    nameInput.addEventListener('input', function() {
        document.querySelector('.modal-char-counter').textContent =
            `${this.value.length}/50`;
    });

    // Обработчик окна, закрывающий его при нажатии вне окна
    window.addEventListener('click', function(event) {
        if (event.target.matches('.modal-overlay')) {
            hideSaveModal();
        }
    });
});

function showSaveModal() {
    // Проверяем карточки перед показом модального окна
    if (!validateCards()) {
        return;
    }

    const modal = document.getElementById('modalOverlay');
    const nameInput = document.getElementById('setNameInput');
    nameInput.value = '';
    document.querySelector('.modal-char-counter').textContent = '0/50';
    modal.classList.add('show');
    nameInput.focus();
}

function hideSaveModal() {
    const modal = document.getElementById('modalOverlay');
    modal.classList.remove('show');
}

async function loadCard(container) {
    try {
        const response = await fetch(`/api/get_card_html/`);

        if (!response.ok) {
            throw new Error('Ошибка загрузки карточки');
        }

        const html = await response.text();
        container.innerHTML = html;

    } catch (error) {
        console.error('Ошибка:', error);
        container.innerHTML = '<div class="error">Не удалось загрузить карточку</div>';
    }
}

function addCard() {
    const container = document.getElementById('cardsContainer');
    const cardCount = container.children.length;

    const cardDiv = document.createElement('div');
    loadCard(cardDiv);

    container.appendChild(cardDiv);

    // Обработчики для снятия выделения при вводе
    const inputs = cardDiv.querySelectorAll('.card-input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.closest('.card').classList.remove('invalid');
        });
    });

    // Прокручиваем к новой карточке при её добавлении
    setTimeout(() => {
        cardDiv.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

document.getElementById('cardsContainer').addEventListener('input', function(e) {
    const target = e.target;
    if (target.matches('textarea[name^="term_"]')) {
        const counter = target.closest('.card-side').querySelector('.char-counter');
        counter.textContent = `${target.value.length}/50`;
        target.closest('.card').classList.remove('invalid');
    } else if (target.matches('textarea[name^="definition_"]')) {
        const counter = target.closest('.card-side').querySelector('.char-counter');
        counter.textContent = `${target.value.length}/150`;
        target.closest('.card').classList.remove('invalid');
    }
});

function deleteCard(button) {
    const card = button.closest('.card');
    card.classList.add('card-deleting');

    setTimeout(() => {
        card.remove();
        updateCardInputNames();
    }, 300);
}

// Обновление списка после удаления карточки
function updateCardInputNames() {
    const container = document.getElementById('cardsContainer');
    const cards = container.querySelectorAll('.card');

    cards.forEach((card, index) => {
        const termInput = card.querySelector(`textarea[name^="term_"]`);
        const definitionInput = card.querySelector(`textarea[name^="definition_"]`);

        if (termInput) termInput.name = `term_${index}`;
        if (definitionInput) definitionInput.name = `definition_${index}`;
    });
}

// Проверка карточек на заполненность
function validateCards() {
    const container = document.getElementById('cardsContainer');
    const cards = container.querySelectorAll('.card');
    let isValid = true;

    // Убираем все подсветки, чтобы установить их уже в случае ошибок
    cards.forEach(card => {
        card.classList.remove('invalid');
    });

    // Проверяем каждую карточку
    cards.forEach(card => {
        const termInput = card.querySelector('textarea[name^="term_"]');
        const definitionInput = card.querySelector('textarea[name^="definition_"]');

        const term = termInput.value.trim();
        const definition = definitionInput.value.trim();

        if (!term || !definition) {
            card.classList.add('invalid');
            isValid = false;
        }
    });

    if (!isValid) {
        alert('Заполните все поля карточек!');
        return false;
    }

    // Проверяем, есть ли карточки
    if (cards.length === 0) {
        alert('Добавьте хотя бы одну карточку!');
        return false;
    }

    return true;
}

// Сохранение всех карточек в набор и БД
function saveCardSet() {
    const cardSetName = document.getElementById('setNameInput').value.trim();

    if (!cardSetName) {
        alert('Введите название набора!');
        document.getElementById('setNameInput').focus();
        return;
    }

    const container = document.getElementById('cardsContainer');
    const cards = container.querySelectorAll('.card');

    // Собираем данные карточек
    const cardsData = [];

    cards.forEach(card => {
        const termInput = card.querySelector('textarea[name^="term_"]');
        const definitionInput = card.querySelector('textarea[name^="definition_"]');

        const term = termInput.value.trim();
        const definition = definitionInput.value.trim();

        cardsData.push({
            term: term,
            definition: definition
        });
    });

    document.getElementById('cardSetNameInput').value = cardSetName;
    const form = document.getElementById('cardSetForm');
    // Очищаем старые данные
    while (form.children.length > 2) {  // Оставляем только csrf и cardSetNameInput
        form.removeChild(form.lastChild);
    }

    // Добавляем данные карточек в форму
    cardsData.forEach((card, index) => {
        const termInput = document.createElement('input');
        termInput.type = 'hidden';
        termInput.name = `term_${index}`;
        termInput.value = card.term;
        form.appendChild(termInput);

        const definitionInput = document.createElement('input');
        definitionInput.type = 'hidden';
        definitionInput.name = `definition_${index}`;
        definitionInput.value = card.definition;
        form.appendChild(definitionInput);
    });

    // Скрываем всплывающее окно ввода названия набора
    hideSaveModal();

    // Отправляем форму
    form.submit();
}
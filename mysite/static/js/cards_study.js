function flipCard() {
    document.getElementById('card').classList.toggle('flipped');
}

function updateCard() {
    const card = document.getElementById('card');
    const frontContent = document.getElementById('front-content');
    const backContent = document.getElementById('back-content');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    // Установка front-side для карточки
    if (card.classList.contains('flipped')) {
        card.classList.remove('flipped');
    }

    // Обновление термина и определения
    frontContent.textContent = cards[currentCardIndex].term;
    backContent.textContent = cards[currentCardIndex].definition;

    // Обновление кнопок переключения между карточками
    prevBtn.disabled = currentCardIndex === 0;
    nextBtn.disabled = currentCardIndex === cards.length - 1;
}

function nextCard() {
    if (currentCardIndex < cards.length - 1) {
        currentCardIndex++;
        animateCard('right');
        updateCard();
    }
}

function prevCard() {
    if (currentCardIndex > 0) {
        currentCardIndex--;
        animateCard('left');
        updateCard();
    }
}

function animateCard(direction) {
    const cardContainer = document.querySelector('.card-container');
    const card = document.getElementById('card');

    // Создание класса анимации
    cardContainer.classList.add(`slide-${direction}`);
    // Удаление класса анимации после ее окончания
    setTimeout(() => {
        cardContainer.classList.remove(`slide-${direction}`);
    }, 500);
}
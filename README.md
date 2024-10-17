<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Generation</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
</head>
<body>
    <!-- Логотип и заголовок -->
    <header>
        <a href="https://www.vtb.ru" target="_blank">
            <img src="{{ url_for('static', filename='vtb-logo.png') }}" alt="VTB Logo" class="logo">
        </a>
        <h1>Введите запрос для генерации</h1>
    </header>

    <!-- Форма для ввода запроса -->
    <form action="/process" method="post">
        <textarea name="user_input" placeholder="Введите текст здесь..." rows="5" required></textarea>
        <button type="submit">Сгенерировать текст</button>
    </form>

    <!-- Результаты генерации -->
    {% if result %}
    <section class="results">
        <h2>Результаты генерации</h2>
        <div class="iteration">
            <h3>Итерация №1:</h3>
            <p>{{ result['iter_1'] }}</p>
        </div>
        <div class="iteration">
            <h3>Итерация №2:</h3>
            <p>{{ result['iter_2'] }}</p>
        </div>
        <div class="iteration">
            <h3>Итерация №3:</h3>
            <p>{{ result['iter_3'] }}</p>
        </div>
    </section>
    {% endif %}
</body>
</html>

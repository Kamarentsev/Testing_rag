@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    
    # Отправляем запрос на сервер обработки
    response = requests.post("http://10.235.78.137:8505/process", json={'input': user_input})
    
    # Проверяем, что вернул сервер
    try:
        response_data = response.json()
        print("Response Data:", response_data)  # Для отладки, чтобы увидеть ответ
        
        # Получаем пять результатов из ответа
        results = response_data.get('results', None)
        if not results:
            results = {"error": "Ошибка при обработке запроса"}
    except ValueError:
        # Если ответ не JSON, устанавливаем сообщение об ошибке
        results = {"error": "Ошибка при обработке запроса - неверный формат ответа"}

    return render_template('index.html', results=results)

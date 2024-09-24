import socket

# Настройки сервера
HOST = '0.0.0.0'  # Слушаем все интерфейсы (серверная часть)
PORT = 65432      # Порт для связи

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен на порту {PORT}. Ожидание подключения...")

    conn, addr = s.accept()  # Ожидание подключения клиента
    with conn:
        print(f"Подключено к клиенту: {addr}")

        # Отправка данных для вычислений на клиент (например, число 5 для обработки)
        data_to_process = "5"
        print(f"Отправка данных: {data_to_process}")
        conn.sendall(data_to_process.encode())  # Отправляем строку на клиент

        # Получаем результат обратно от клиента
        result = conn.recv(1024)  # Ожидание результата от клиента
        print(f"Получено от клиента: {result.decode()}")

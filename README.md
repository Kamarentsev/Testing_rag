import socket

# Настройки сервера
HOST = '0.0.0.0'  # Сервер слушает все сетевые интерфейсы
PORT = 65432      # Указанный порт для связи

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен на порту {PORT}. Ожидание подключений...")
    
    conn, addr = s.accept()  # Ожидание подключения от клиента
    with conn:
        print(f"Подключено с {addr}")
        data = conn.recv(1024)  # Получение данных от клиента
        print(f"Получено: {data.decode()}")
        
        # Обработка данных и отправка ответа
        response = f"Обработанные данные: {data.decode().upper()}"
        conn.sendall(response.encode())

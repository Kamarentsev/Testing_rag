import socket

# Настройки клиента
HOST = 'адрес_сервера'  # IP-адрес сервера, например, '192.168.1.100'
PORT = 65432            # Тот же порт, что и у сервера

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Подключение к серверу
    s.sendall(b"Привет от клиента!")  # Отправка данных серверу
    
    # Получение ответа от сервера
    data = s.recv(1024)
    print(f"Получено от сервера: {data.decode()}")

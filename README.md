import socket

# Настройки клиента
SERVER_IP = 'адрес_сервера'  # IP-адрес сервера, например, '192.168.1.100'
PORT = 65432                 # Тот же порт, что и на сервере

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, PORT))  # Подключение к серверу

    # Принимаем данные для вычисления
    data = s.recv(1024)
    print(f"Получено от сервера для вычисления: {data.decode()}")

    # Выполняем вычисления (например, возводим число в квадрат)
    result = str(int(data.decode()) ** 2)
    print(f"Результат вычисления: {result}")

    # Отправляем результат обратно на сервер
    s.sendall(result.encode())

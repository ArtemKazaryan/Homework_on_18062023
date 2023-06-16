
# Домашняя работа на 18.06.2023.

# Задание 3 (Обязательное)
# Измените задание номер 2. Добавьте получение прогноза погоды из внешнего источника.
# Для этого воспользуйтесь сайтом https://openweathermap.
# org. Для начала нужно зарегистрироваться на сайте по
# ссылке https://home.openweathermap.org/users/sign_up
# и получить ключ для дальнейшей работы. На странице
# https://openweathermap.org/current есть подробная документация как работать с API. Теперь после запроса от
# клиента необходимо получать данные о погоде с этого
# источника. Полученный результат возвращать клиенту

# Решение(клиент):

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 1234

client_socket.connect((host, port))

server_message = client_socket.recv(1024).decode()
print(server_message)

while True:
    client_message = input('Введите название города с большой буквы на латинском: ')
    client_socket.send(client_message.encode())

    if not client_message:
        print('Отключаемся от сервера...')
        break

    server_response = client_socket.recv(2048).decode()
    print(f'{server_response}')

client_socket.close()


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

# Решение(сервер):

import socket
import threading
import json
import urllib.request

# Укажите свой API-ключ
api_key = 'API-ключ'
city = ''

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    data = json.loads(data)
    weather = data['weather'][0]['description']
    temp = round(data['main']['temp'] - 273.15, 1)  # перевод из Кельвинов в Цельсии
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    answer = f"Погода в городе {city[0].upper() + city[1:]}: {weather}, температура {temp}°C, влажность {humidity}%, скорость ветра {wind_speed} м/с.\n"
    return answer

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"  # / localhost / socket.gethostbyname(socket.gethostname())
port = 1234

server_socket.bind((host, port))
print(f'Сервер запущен по адресу {host}, порту {port}')

server_socket.listen(5)

welcome_message = 'Добро пожаловать! Вы подключены к серверу сайта о погоде https://openweathermap.'

def handle_client(client_socket, client_address):
    print(f'Подключился клиент: {client_address}')
    client_socket.send(welcome_message.encode())

    while True:
        client_message = client_socket.recv(1024).decode()
        if not client_message:
            print('Клиент отключился: ', client_address)
            break

        global city
        city = client_message
        weather_info = get_weather(city)

        client_socket.send(weather_info.encode('utf-8'))
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
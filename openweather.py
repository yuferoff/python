""" 
== OpenWeatherMap ==
OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.
Необходимо решить следующие задачи:
== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)
        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up
        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in
        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"
        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a
    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    
== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):
    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных
2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))
3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.
При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.
При работе с XML-файлами:
Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>
Чтобы работать с пространствами имен удобно пользоваться такими функциями:
    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''
    tree = ET.parse(f)
    root = tree.getroot()
    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}
    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...
"""

import os
import datetime
import json
import sqlite3
import urllib.request


# Конвертация времени из timestamp
def time_converter(time, key=False):
    if key:
        converted_time = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        converted_time = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%H:%M')
    return converted_time


# Формирование полной ссылки запроса
def url_builder(city_id):
    # Считывание APPID из файла app.id
    path_appid = os.path.join('app.id')
    with open(path_appid, 'r', encoding='UTF-8') as f:
        user_api = f.read()

    unit = 'metric'  # Градусы цельсия
    api = 'http://api.openweathermap.org/data/2.5/weather?id='

    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


# Выборка данных в JSON формате
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


# Организовываем данные в словарь
def data_organizer(raw_api_dict):
    data = dict(
            id_city=raw_api_dict.get('id'),
            city=raw_api_dict.get('name'),
            country=raw_api_dict.get('sys').get('country'),
            temp=raw_api_dict.get('main').get('temp'),
            temp_max=raw_api_dict.get('main').get('temp_max'),
            temp_min=raw_api_dict.get('main').get('temp_min'),
            humidity=raw_api_dict.get('main').get('humidity'),
            pressure=raw_api_dict.get('main').get('pressure'),
            sky=raw_api_dict['weather'][0]['main'],
            id_weather=raw_api_dict['weather'][0]['id'],
            sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
            sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
            wind=raw_api_dict.get('wind').get('speed'),
            wind_deg=raw_api_dict.get('deg'),
            dt=time_converter(raw_api_dict.get('dt'), key=True),
            time=time_converter(raw_api_dict.get('dt')),
            cloudiness=raw_api_dict.get('clouds').get('all')
        )
    return data


# Вывод данных на печать
def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol, data['sky'])
    print('weather_id:', data['id_weather'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
    print('Humidity: {}'.format(data['humidity']))
    print('Cloud: {}'.format(data['cloudiness']))
    print('Pressure: {}'.format(data['pressure']))
    print('Sunrise at: {}'.format(data['sunrise']))
    print('Sunset at: {}'.format(data['sunset']))
    print('')
    print('Last update from the server: {} {}'.format(data['dt'], data['time']))
    print('---------------------------------------')


# Подключение и запись в базу данных
def connect_db(data):
    db_name='weather.db'
    # os.remove(db_name)
    with sqlite3.connect(db_name) as conn:
        # Create table on first connection
        try:
            conn.execute('''
            create table weather (
                id_city     integer primary key,
                city        varchar(255),
                country     varchar(255),                
                temp        integer,
                id_weather  integer,
                date        date
            );
            ''')
        except sqlite3.OperationalError:
            pass  # Таблица уже существует

        # Insert or Update
        try:
            conn.execute('''
                insert into weather (id_city, city, country, temp, id_weather, date) VALUES (?,?,?,?,?,?)''', (
                    data['id_city'],
                    data['city'],
                    data['country'],
                    data['temp'],
                    data['id_weather'],
                    data['dt']
                )
            )
        # If exist then will update
        except sqlite3.IntegrityError:
            conn.execute("update weather set "
                         "city=:city, country=:country, temp=:temp, id_weather=:id_weather, date=:date "
                         "where id_city=:id_city",
                         {'city': data['city'],
                          'country': data['country'],
                          'temp': data['temp'],
                          'id_weather': data['id_weather'],
                          'date': data['dt'],
                          'id_city': data['id_city']
                          })


# Печать из базы данных
def get_db(id_city, db_name='weather.db'):
    with sqlite3.connect(db_name) as conn:
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM weather WHERE id_city=%s'%id_city)
        data = cur.fetchone()
        print('----------------------')
        print('id city: %s'%data[0])
        print('city: %s'%data[1])
        print('country: %s'%data[2])
        print('temp: %s'%data[3])
        print('id_weather: %s'%data[4])
        print('date: %s'%data[5])


id_tlv = 293396
id_nv = 1497543


if __name__ == '__main__':
    try:
        connect_db(data_organizer(data_fetch(url_builder(id_tlv))))
        connect_db(data_organizer(data_fetch(url_builder(id_nv))))
        get_db(id_tlv)
        get_db(id_nv)
        pass
    except IOError:
        print('no internet')

from django.shortcuts import render
from .models import Weather
from datetime import datetime
from .forms import WeatherForm
import requests


# Головна сторінка
def home(request):
    conclusion = {'info': {}, 'message': ''}
    # Якщо отримуємо POST із форми "WeatherForm" - парсимо
    if request.method == 'POST':
        name = request.POST['name'].lower().capitalize()
        api_get = f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid=80d395580678199c313aaa6731d7c45f'
        response = requests.get(api_get).json()
        if 'message' in response:
            if response['message'] == 'city not found':
                # Якщо місто не знайдено
                conclusion['message'] = 'city not found'
        else:
            # Якщо місто знайдено - записуємо в табилицю і в словник "conclusion"
            conclusion['message'] = f'Weather in {name}'
            w = Weather()
            w.name = conclusion['info']['name'] = name
            w.country = conclusion['info']['country'] = response['sys']['country']
            w.dat = conclusion['info']['dat'] = datetime.now()
            w.wind = conclusion['info']['wind'] = response['wind']['speed']
            w.visibility = conclusion['info']['visibility'] = response['visibility']
            w.temp = conclusion['info']['temp'] = response['main']['temp']
            w.feels_like = conclusion['info']['feels_like'] = response['main']['feels_like']
            w.humidity = conclusion['info']['humidity'] = response['main']['humidity']
            w.pressure = conclusion['info']['pressure'] = response['main']['pressure']
            w.icon = conclusion['info']['icon'] = response['weather'][0]['icon']
            # Зберігаємо запис
            w.save()
            # select distinct name FROM main_weather
    form = WeatherForm()
    # data_list magic
    el_list = []
    for el in Weather.objects.raw('SELECT id, name FROM main_weather Order by name ASC'):
        el_list.append(el.name)
    el_set = set(el_list)
    context = {'form': form, 'conclusion': conclusion, 'el_set': el_set}
    return render(request, 'main/home.html', context)


# Історія запитів
def history(request):
    city_name = ''
    date_from = ''
    date_to = ''

    el_list = []
    for el in Weather.objects.raw('SELECT id, name FROM main_weather Order by name ASC'):
        el_list.append(el.name)
    el_set = set(el_list)

    qs = 'SELECT * FROM main_weather WHERE 1'
    if request.GET.get('name'):
        city_name = request.GET['name']
        qs += f" AND name = '{city_name}'"

    if request.GET.get('date_from'):
        date_from = request.GET['date_from']
        qs += f" AND `dat` >= '{date_from}'"

    if request.GET.get('date_to'):
        date_to = request.GET['date_to']
        qs += f" AND `dat` <= '{date_to}'"

    qs += ' ORDER BY id desc'
    items = Weather.objects.raw(qs)

    context = {
        "items": items,
        "city_name": city_name,
        "date_from": date_from,
        "date_to": date_to,
        "el_set": el_set
    }
    return render(request, 'main/history.html', context)
import eel 
from pyowm import OWM
from pyowm.utils.config import get_default_config
import requests
from pprint import pprint
from config import open_weather_token  


config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('c1c7f73448aab7430eb1ba3a56f8876a',  config_dict)



@eel.expose
def get_weather(place):
	code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
	try:

		r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={open_weather_token}&units=metric"
        )
		data = r.json()
		print(data)

		place = data["name"]

		cur_weather = data["main"]["temp"]

		weather_description = data["weather"][0]["main"]
		if weather_description in code_to_smile:
			wd = code_to_smile[weather_description]
		else:
			wd = "Посмотри в окно, не пойму что там за погода!"
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather
		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance




		return f'В городе {place} температура: {t1}°C, ощущается как: {t2}°C,<br>Максимальная: {t3}°C, минимальня {t4}°C,<br>Скорость ветра: {wi}м/с, влажность: {humi}%,<br>Облачность: {cl}%, статус: {wd},<br>Детальный статус: {dt}, справочное время: {ti},<br>Давление: {pr}мм.рт.ст., видимость: {vd}м. '
		
	except Exception as ex:
	    print(ex)
	    return f"Проверьте название города"

eel.init('web')
eel.start('proga.html', mode='chrome',  size=(700, 700), position=(500, 500))
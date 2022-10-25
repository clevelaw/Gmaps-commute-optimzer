import requests

city = "Austin"

class Commute_weather:

    def __init__(self, city):
        self._city = city

    def gather_weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        weather_api = open('weather_api.txt', 'r').read()
        url = base_url + "appid=" + weather_api + "&q=" + self._city
        weather_dict = requests.get(url).json()

        temp = weather_dict["main"]["temp"]
        temp_f =self.k_to_f(temp)
        humidity = weather_dict["main"]["humidity"]
        weather = weather_dict["weather"][0]["main"]
        visibility = weather_dict["visibility"]
        sunrise = weather_dict["sys"]["sunrise"]
        sunset = weather_dict["sys"]["sunset"]
        wind = weather_dict["wind"]["speed"]
        wind_deg = weather_dict["wind"]["deg"]
        wind_dir = self.deg_to_cardinal(wind_deg)

        current_weather = {
            "temp" : temp,
            "temp_f" : temp_f,
            "humidity" : humidity,
            "weather" : weather,
            "visibility" : visibility,
            "sunrise" : sunrise,
            "sunset" : sunset,
            "wind" : wind,
            "wind_dir" : wind_dir
        }

        return current_weather

    def show_weather(self, dict):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"In {city} the weather is:")
        print(f'It is currently {dict["temp_f"]: .3} °F out and weather is {dict["weather"]}')
        print(f'Humidity is {dict["humidity"]}% and visibility is {dict["visibility"]/1000}km')
        print(f'Wind speed is {dict["wind"]}m/s blowing {dict["wind_dir"]}')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def k_to_f(self, temp):
        fahrenheit = 1.8 * (temp - 273) + 32
        return round(fahrenheit, 2)

    def deg_to_cardinal(self, direction):
        dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        ix = round(direction / (360. / len(dirs)))
        return dirs[ix % len(dirs)]

def weather_test():
    hehe = Commute_weather("Austin").gather_weather()
    ww = Commute_weather("Austin")
    whats_weather = ww.gather_weather()
    ww.show_weather(whats_weather)


import requests
import datetime as dt
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime

# base request URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# loading the API key
API_KEY = open("api_key", "r").read()

# user credentials for proxy
USER = open("username", "r").read()
PASSW = open("password", "r").read()

isCelsius = True
isFahrenheit = False

KELVIN_CELSIUS = 273.15
KELVIN_FAHRENHEIT = 457.87

# main proxy
http_proxy = f"http://{USER}:{PASSW}@proxy.dunaferr.hu:8080"

# proxies
proxies = {
    "http": http_proxy,
    "https": http_proxy
}


"""
        Converting kelvin to celsius
"""
def celsius() -> str:
    return str(int(resp['main']['temp'] - KELVIN_CELSIUS)) + "°"


"""
        what the weather feels like in celsius
"""
def feels_like_celsius() -> str:
    return "Hőérzet |" + str(int(resp['main']['feels_like'] - KELVIN_CELSIUS)) + "°C"


"""
    Minimum and maximum temperature in celsius
"""
def temp_min_celsius() -> str:
    return str(int(resp['main']['temp_min'] - KELVIN_CELSIUS)) + "°C"

def temp_max_celsius() -> str:
    return str(int(resp['main']['temp_max'] - KELVIN_CELSIUS)) + "°C"

def temp_min_max_celsius() -> str:
    return str(int(resp['main']['temp_min'] - KELVIN_CELSIUS)) + "°C / " + \
        str(int(resp['main']['temp_max'] - KELVIN_CELSIUS)) + "°C"


"""
        converting kelvin to fahrenheit
"""

def fahrenheit() -> str:
    return str(int(resp['main']['temp'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°"


"""
        what the weather feels like in fahrenheit
"""
def feels_like_fahrenheit() -> str:
    return "Hőérzet |" + str(int(resp['main']['feels_like'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


"""
    Minimum and maximum temperature in fahrenheit
"""
def temp_min_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"

def temp_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"

def temp_min_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F / " + \
        str(int(resp['main']['temp_max'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


"""
        Getting the pollution level in integer and returning the string value in hungarian
"""
def air_pollution() -> str:
    pollution = coordinate_to_city()

    if pollution == 1:
        return "Kiváló"
    elif pollution == 2:
        return "Jó"
    elif pollution == 3:
        return "megfelelő"
    elif pollution == 4:
        return "Részben rossz"
    elif pollution == 5:
        return "Rossz"


"""
        Ask the API to search the given city longitude and latitude and return the pollution level
"""
def coordinate_to_city() -> str:
    # URL and request for the city coordinates: latitude and longtitude
    coordinate_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY.get()}&appid={API_KEY}"
    response = requests.get(coordinate_url, proxies=proxies).json()

    # getting the latitude and longtitude from the json data
    latitude = response[0]["lat"]
    longtitude = response[0]["lon"]

    # URL and request for the air pollution level, using the latitude and longtitude
    air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longtitude}&appid={API_KEY}"
    air_poll_req = requests.get(air_pollution_url, proxies=proxies).json()

    # returning the air pollution level
    return air_poll_req['list'][0]['main']['aqi']


"""
        Getting and translating the weather data
"""
def sky() -> str:
    weather = resp['weather'][0]['main']
    if weather == "Clear":
        return "Derült"
    elif weather == "Clouds":
        return "Felhős"
    elif weather == "Rain":
        return "Esős"
    elif weather == "Thunderstorm":
        return "Viharos"
    elif weather == "Snow":
        return "havazás"
    elif weather == "Mist":
        return "Ködös"
    elif weather == "Smoke":
        return "Szmogos"
    else:
        return weather


""" sky description """
def sky_description() -> str:
    return resp['weather'][0]['description'].capitalize()


""" humidity in % """
def humidity() -> str:
    return "Páratartalom |" + str(resp['main']['humidity']) + "%"


""" pressure in hPa """
def pressure() -> str:
    return "Légnyomás |" + str(resp['main']['pressure']) + " hPa"


""" Wind speed in km/h """
def wind_speed() -> str:
    return "Szélsebesség |" + str(round(float(resp['wind']['speed'] * 3.6), 1)) + " km/h"

def wind_speed_mph() -> str:
    return "Szélsebesség |" + str(round(float(resp['wind']['speed'] * 2.237), 1)) + " mph/h"

""" Time hour:minute:second restarts every second """
def time():
    string = dt.datetime.now().strftime("%H:%M:%S")
    lbl.config(text=string)
    # update every second
    lbl.after(1000, time)


""" Choose the weather icon based on the weather """
def for_weather_icon() -> str:
    if sky() == "Clear" or sky() == "Clear sky" or sky() == "Sunny" or sky() == "Derült":
        return "assets/sunny.png"
    elif sky() == "Clouds" or sky() == "Few clouds" or sky() == "Scattered clouds" or sky() == "Broken clouds" \
            or sky() == "Felhős":
        return "assets/cloudy.png"
    elif sky() == "Rain" or sky() == "Light rain" or sky() == "Moderate rain" or sky() == "Heavy rain" or \
            sky() == "Very heavy rain" or sky() == "Extreme rain" or sky() == "Freezing rain" or \
            sky() == "Light intensity shower rain" or sky() == "Shower rain" or \
            sky() == "Heavy intensity shower rain" or sky() == "Ragged shower rain" or sky() == "Esős":
        return "assets/rainy.png"
    elif sky() == "Thunderstorm" or sky() == "Thunderstorm with light rain" or sky() == "Thunderstorm with rain" or \
            sky() == "Thunderstorm with heavy rain" or sky() == "Light thunderstorm" or \
            sky() == "Heavy thunderstorm" or sky() == "Ragged thunderstorm" or \
            sky() == "Thunderstorm with light drizzle" or \
            sky() == "Thunderstorm with drizzle" or sky() == "Thunderstorm with heavy drizzle" or sky() == "Viharos":
        return "assets/thunderstorm.png"
    elif sky() == "Snow" or sky() == "Light snow" or sky() == "Heavy snow" or sky() == "Sleet" or \
            sky() == "Light shower sleet" or sky() == "Shower sleet" or sky() == "Light rain and snow" or \
            sky() == "Rain and snow" or sky() == "Light shower snow" or sky() == "Shower snow" or \
            sky() == "Heavy shower snow" or sky() == "Havazás":
        return "assets/snowy.png"
    elif sky() == "Mist" or sky() == "Smoke" or sky() == "Haze" or sky() == "Sand, dust whirls" or \
            sky() == "Fog" or sky() == "Sand" or sky() == "Dust" or sky() == "Volcanic ash" or \
            sky() == "Squalls" or sky() == "Tornado" or sky() == "Ködös":
        return "assets/foggy.png"


""" Compiles the request URL based on the city name """
def exec_city_req():
    if CITY.get() == "":
        CITY.set("Dunaújváros")
        return f"{BASE_URL}q={CITY.get()}&lang=hu&appid={API_KEY}"
    else:
        print(CITY.get().capitalize())
        return f"{BASE_URL}q={CITY.get()}&lang=hu&appid={API_KEY}"


# creating the window
window = tk.Tk()
window.title("Weather App")
window.geometry("900x500+500+250")
window.resizable(False, False)

frame = tk.Frame(window, bg="#878787")
frame.place(relwidth=1, relheight=0.5)

frame2 = tk.Frame(window, bg="black")
frame2.place(rely=0.5, relwidth=1, relheight=0.5)

canvas = tk.Canvas(window, width=600, height=0.5, border=0, borderwidth=0, highlightthickness=0)
canvas.place(x=150, y=205)
canvas.configure(background='#878787', border=0)
# Egy vonal rajzolása
canvas.create_line(0, 0, 600, 0, fill="black", width=0)

CITY = tk.StringVar()

# response from the API
resp = requests.get(exec_city_req(), proxies=proxies).json()

print(resp)


""" which unit is active: Celsius """
def active_button_celsius():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label

    isCelsius = True
    isFahrenheit = False

    to_celsius_button.configure(background="black", foreground="#878787")

    to_fahrenheit_button.configure(background="#878787", foreground="black")

    celsius_label.configure(text=celsius())

    feels_like_celsius_label.configure(text=feels_like_celsius())

    wind_speed_label.configure(text=wind_speed())

    min_max_celsius.configure(text=temp_min_max_celsius())


""" which unit is active: Fahrenheit """
def active_button_fahrenheit():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label

    isCelsius = False
    isFahrenheit = True

    to_celsius_button.configure(background="#878787", foreground="black")

    to_fahrenheit_button.configure(background="black", foreground="#878787")

    celsius_label.configure(text=fahrenheit())

    feels_like_celsius_label.configure(text=feels_like_fahrenheit())

    wind_speed_label.configure(text=wind_speed_mph())

    min_max_celsius.configure(text=temp_min_max_fahrenheit())


def save_city():
    city = CITY.get()
    return city.capitalize()


def update_data():
    # call the API and update the data
    global resp, weather_photo
    param = f"{BASE_URL}q={save_city()}&lang=hu&appid={API_KEY}"
    resp = requests.get(param, proxies=proxies).json()
    print(resp)

    if resp.get("cod") == 200:
        # update the weather icon
        weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
        weather_label.configure(image=weather_photo, background="#878787")
        city_label.configure(text=CITY.get().capitalize())

        # update the temperature
        if isCelsius:
            celsius_label.configure(text=celsius())
        elif isFahrenheit:
            celsius_label.configure(text=fahrenheit())
        feels_like_celsius_label.configure(text=feels_like_celsius())

        # update other information
        humidity_label.configure(text=humidity())
        pressure_label.configure(text=pressure())
        wind_speed_label.configure(text=wind_speed())
        sky_label.configure(text=sky())
        sky_label_description.configure(text=sky_description())
        min_max_celsius.configure(text=temp_min_max_celsius())
    else:
        print("City not found", CITY.get().capitalize())

    # schedule the function to be called again after 2 minutes
    window.after(120000, update_data)


# schedule the first call to the function
window.after(12000, update_data)

# CLOCK
lbl = Label(window, font=("Georgia", 20, 'bold'), background="#878787", foreground="black")
lbl.place(relx=0.8, rely=0.3, anchor=CENTER)
time()

# create the weather icon label and keep a reference to it
weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
weather_label = Label(image=weather_photo, bg="#878787", fg="white")
weather_label.place(relx=0.4, rely=0.27, anchor=CENTER)

city_label = Label(window, text=CITY.get(), font=("Open sans", 28, 'bold'), background="#878787", foreground="black")
city_label.place(relx=0.5, rely=0.12, anchor=CENTER)

"""                     temperature                     """

# create the temperature labels and keep references to them

celsius_label = Label(window, text=celsius(), font=("Arial", 32, 'bold'), background="#878787", foreground="black")
celsius_label.place(relx=0.495, rely=0.26, anchor=CENTER)

feels_like_celsius_label = Label(window, text=feels_like_celsius(), font=("Garamond", 16, 'bold'), background="#878787",
                                 foreground="black")
feels_like_celsius_label.place(relx=0.275, rely=0.45, anchor=CENTER)

"""                     other infos                     """

# create other information labels and keep references to them

humidity_label = Label(window, text=humidity(), font=("Garamond", 16, 'bold'), background="black", foreground="#878787")
humidity_label.place(relx=0.275, rely=0.55, anchor=CENTER)

pressure_label = Label(window, text=pressure(), font=("Garamond", 16, 'bold'), background="#878787", foreground="black")
pressure_label.place(relx=0.52, rely=0.45, anchor=CENTER)

wind_speed_label = Label(window, text=wind_speed(), font=("Garamond", 16, 'bold'), background="black", foreground="#878787")
wind_speed_label.place(relx=0.52, rely=0.55, anchor=CENTER)

sky_label = Label(window, text=sky(), font=("Open sans", 18, 'bold'), background="#878787", foreground="black")
sky_label.place(relx=0.5, rely=0.37, anchor=CENTER)

sky_label_description = Label(window, text=sky_description(), font=("Garamond", 16, 'bold'), background="#878787",
                              foreground="black")
sky_label_description.place(relx=0.75, rely=0.45, anchor=CENTER)

min_max_celsius = Label(window, text=temp_min_max_celsius(), font=("Garamond", 16, 'bold'), background="black",
                        foreground="#878787")
min_max_celsius.place(relx=0.75, rely=0.55, anchor=CENTER)

# creating the search bar
Label(window, foreground="black", background="#878787", border=2).place(relx=0.75, rely=0.1, anchor=CENTER)
print(CITY.get().capitalize())

# ENTRY FIELDS

# input field
input_field = Entry(window, justify="center", font=("Open sans", 18), bg="#878787", fg="black", border=0,
                    textvariable=CITY, insertbackground="black")
input_field.place(width=170, height=30, relx=0.83, rely=0.1, anchor=CENTER)

# BUTTONS

to_celsius_button = Button(window, text="C", command=active_button_celsius, font=("Open sans", 16, 'bold'),
                           background="black", foreground="#878787", border=0)
to_celsius_button.place(relx=0.56, rely=0.22, anchor=CENTER)

to_fahrenheit_button = Button(window, text="F", command=active_button_fahrenheit, font=("Open sans", 16, 'bold'),
                              background="#878787", foreground="black", border=0)
to_fahrenheit_button.place(relx=0.56, rely=0.3, anchor=CENTER)

search_button_icon = ImageTk.PhotoImage(file="assets/search_icon2.png")
search_button = Button(image=search_button_icon, background="#878787", foreground="black", border=0,
                       command=update_data)
search_button.place(relx=0.96, rely=0.1, anchor=CENTER)

url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY.get()}&exclude=daily,minutely&lang=hu&appid={API_KEY}"
data = requests.get(url, proxies=proxies).json()
print(data)
forecast_data = {}

for item in data['list']:
    # Az időpont konvertálása
    timestamp = item['dt']
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    # Az adatok hozzáadása a szótárhoz
    if date not in forecast_data:
        forecast_data[date] = []
    forecast_data[date].append(item)
print(forecast_data)




canvas = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas.place(relx=0.2, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas.create_polygon(x1+radius, y1, x2-radius, y1, x2, y1+radius, x2, y2-radius,
                      x2-radius, y2, x1+radius, y2, x1, y2-radius, x1, y1+radius,
                      outline='#878787', fill='#878787')

canvas2 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas2.place(relx=0.4, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas2.create_polygon(x1+radius, y1, x2-radius, y1, x2, y1+radius, x2, y2-radius,
                      x2-radius, y2, x1+radius, y2, x1, y2-radius, x1, y1+radius,
                      outline='#878787', fill='#878787')


canvas3 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas3.place(relx=0.6, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas3.create_polygon(x1+radius, y1, x2-radius, y1, x2, y1+radius, x2, y2-radius,
                      x2-radius, y2, x1+radius, y2, x1, y2-radius, x1, y1+radius,
                      outline='#878787', fill='#878787')


canvas4 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas4.place(relx=0.8, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas4.create_polygon(x1+radius, y1, x2-radius, y1, x2, y1+radius, x2, y2-radius,
                      x2-radius, y2, x1+radius, y2, x1, y2-radius, x1, y1+radius,
                      outline='#878787', fill='#878787')

window.mainloop()

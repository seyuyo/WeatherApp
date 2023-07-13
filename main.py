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


# converting Kelvin to Celsius
def celsius() -> str:
    return str(int(resp['main']['temp'] - KELVIN_CELSIUS)) + "°"


def feels_like_celsius() -> str:
    return "Hőérzet |" + str(int(resp['main']['feels_like'] - KELVIN_CELSIUS)) + "°C"


def temp_min_celsius() -> str:
    return str(int(resp['main']['temp_min'] - KELVIN_CELSIUS)) + "°C"


def temp_max_celsius() -> str:
    return str(int(resp['main']['temp_max'] - KELVIN_CELSIUS)) + "°C"


def temp_min_max_celsius() -> str:
    return str(int(resp['main']['temp_min'] - KELVIN_CELSIUS)) + "°C / " + str(
        int(resp['main']['temp_max'] - KELVIN_CELSIUS)) + "°C"


# converting kelvin to fahrenheit

def fahrenheit() -> str:
    return str(int(resp['main']['temp'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°"


def feels_like_fahrenheit() -> str:
    return "Hőérzet " + str(int(resp['main']['feels_like'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def temp_min_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def temp_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def error() -> str:
    if resp['cod'] == 404:
        return "Nincs ilyen város az adatbázisunkban!"


# weather
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


def sky_description() -> str:
    return resp['weather'][0]['description'].capitalize()


def humidity() -> str:
    return "Páratartalom |" + str(resp['main']['humidity']) + "%"


def pressure() -> str:
    return "Légnyomás |" + str(resp['main']['pressure']) + " hPa"


def wind_speed() -> str:
    return "Szélsebesség |" + str(int(resp['wind']['speed'] * 3.6)) + " km/h"


# clock
def time():
    string = dt.datetime.now().strftime("%H:%M:%S")
    lbl.config(text=string)
    # update every second
    lbl.after(1000, time)


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
window.configure(background="#4f4fff")

canvas = tk.Canvas(window, width=600, height=0.5, border=0, borderwidth=0, highlightthickness=0)
canvas.place(x=150, y=220)
canvas.configure(background='#4f4fff', border=0)
# Egy vonal rajzolása
canvas.create_line(0, 0, 600, 0, fill="black", width=0)

CITY = tk.StringVar()

# response from the API
resp = requests.get(exec_city_req(), proxies=proxies).json()

print(resp)


def active_button_celsius():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label

    isCelsius = True
    isFahrenheit = False

    to_celsius_button.configure(background="#c5e90b", foreground="black")

    to_fahrenheit_button.configure(background="#4f4fff", foreground="black")

    celsius_label.configure(text=celsius())


def active_button_fahrenheit():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label

    isCelsius = False
    isFahrenheit = True

    to_celsius_button.configure(background="#4f4fff", foreground="black")

    to_fahrenheit_button.configure(background="#c5e90b", foreground="black")

    celsius_label.configure(text=fahrenheit())


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
        weather_label.configure(image=weather_photo, background="#4f4fff")
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
        sky_label_description.configure(text=sky_description())
        min_max_celsius.configure(text=temp_min_max_celsius())
    else:
        print("City not found", CITY.get().capitalize())

    # schedule the function to be called again after 2 minutes
    window.after(120000, update_data)


# schedule the first call to the function
window.after(12000, update_data)

# CLOCK
lbl = Label(window, font=("Georgia", 20, 'bold'), background="#4f4fff", foreground="black")
lbl.place(relx=0.8, rely=0.3, anchor=CENTER)
time()

# create the weather icon label and keep a reference to it
weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
weather_label = Label(image=weather_photo, bg="#4f4fff", fg="white")
weather_label.place(relx=0.4, rely=0.3, anchor=CENTER)

city_label = Label(window, text=CITY.get(), font=("Open sans", 25, 'bold'), background="#4f4fff", foreground="white")
city_label.place(relx=0.5, rely=0.15, anchor=CENTER)

"""                     temperature                     """

# create the temperature labels and keep references to them

celsius_label = Label(window, text=celsius(), font=("Arial", 32, 'bold'), background="#4f4fff", foreground="black")
celsius_label.place(relx=0.495, rely=0.29, anchor=CENTER)

feels_like_celsius_label = Label(window, text=feels_like_celsius(), font=("Garamond", 16, 'bold'), background="#4f4fff",
                                 foreground="white")
feels_like_celsius_label.place(relx=0.3, rely=0.48, anchor=CENTER)

"""                     other infos                     """

# create other information labels and keep references to them

humidity_label = Label(window, text=humidity(), font=("Garamond", 16, 'bold'), background="#4f4fff", foreground="black")
humidity_label.place(relx=0.3, rely=0.55, anchor=CENTER)

pressure_label = Label(window, text=pressure(), font=("Garamond", 16, 'bold'), background="#4f4fff", foreground="black")
pressure_label.place(relx=0.52, rely=0.48, anchor=CENTER)

wind_speed_label = Label(window, text=wind_speed(), font=("Garamond", 16, 'bold'), background="#4f4fff",
                         foreground="white")
wind_speed_label.place(relx=0.52, rely=0.55, anchor=CENTER)

sky_label = Label(window, text=sky(), font=("Open sans", 18, 'bold'), background="#4f4fff", foreground="white")
sky_label.place(relx=0.5, rely=0.4, anchor=CENTER)

sky_label_description = Label(window, text=sky_description(), font=("Garamond", 16, 'bold'), background="#4f4fff",
                              foreground="white")
sky_label_description.place(relx=0.75, rely=0.48, anchor=CENTER)

min_max_celsius = Label(window, text=temp_min_max_celsius(), font=("Garamond", 16, 'bold'), background="#4f4fff",
                        foreground="black")
min_max_celsius.place(relx=0.75, rely=0.55, anchor=CENTER)

# creating the search bar
Label(window, foreground="white", background="#4f4fff", border=2).place(relx=0.75, rely=0.1, anchor=CENTER)
print(CITY.get().capitalize())

# ENTRY FIELDS

# input field
input_field = Entry(window, justify="center", font=("Open sans", 18), bg="#2e2eff", fg="white", border=1,
                    textvariable=CITY)
input_field.place(width=150, height=25, relx=0.83, rely=0.1, anchor=CENTER)

# BUTTONS

to_celsius_button = Button(window, text="C", command=active_button_celsius, font=("Open sans", 16, 'bold'),
                           background="#c5e90b", foreground="black", border=0)
to_celsius_button.place(relx=0.56, rely=0.25, anchor=CENTER)

to_fahrenheit_button = Button(window, text="F", command=active_button_fahrenheit, font=("Open sans", 16, 'bold'),
                              background="#4f4fff", foreground="black", border=0)
to_fahrenheit_button.place(relx=0.56, rely=0.33, anchor=CENTER)

search_button_icon = ImageTk.PhotoImage(file="assets/search_icon2.png")
search_button = Button(image=search_button_icon, background="#4f4fff", foreground="black", border=0,
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

window.mainloop()

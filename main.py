import requests
import datetime as dt
import tkinter as tk
from tkinter import ttk

# base request URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Dunaújváros"

# loading the API key
API_KEY = open("api_key", "r").read()

# user credentials for proxy
USER = "bsimon1"
PASSW = open("password", "r").read()

KELVIN_CELSIUS = 273.15
KELVIN_FAHRENHEIT = 457.87


# converting Kelvin to Celsius
def celsius() -> str:
    return str(int(resp['main']['temp'] - KELVIN_CELSIUS)) + "°C"


def feels_like_celsius() -> str:
    return str(int(resp['main']['feels_like'] - KELVIN_CELSIUS)) + "°C"


def temp_min_celsius() -> str:
    return str(int(resp['main']['temp_min'] - KELVIN_CELSIUS)) + "°C"


def temp_max_celsius() -> str:
    return str(int(resp['main']['temp_max'] - KELVIN_CELSIUS)) + "°C"


# converting kelvin to fahrenheit

def fahrenheit() -> str:
    return str(int(resp['main']['temp'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def feels_like_fahrenheit() -> str:
    return str(int(resp['main']['feels_like'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def temp_min_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def temp_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"



# weather
def sky() -> str:
    return resp['weather'][0]['description']


def humidity() -> str:
    return str(resp['main']['humidity']) + "%"


def pressure() -> str:
    return str(resp['main']['pressure']) + " hPa"


def wind_speed() -> str:
    return str(resp['wind']['speed']) + " m/s"


# main request url
Q_URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

# main proxy
http_proxy = "http://" + USER + ":" + PASSW + "@proxy.dunaferr.hu:8080"

# proxies
proxies = {
    "http": http_proxy,
    "https": http_proxy
}

# response from the api
resp = requests.get(Q_URL, proxies=proxies).json()

# print(resp)

print(celsius())
print(fahrenheit())
print(sky())
print(humidity())
print(pressure())
print(wind_speed())

# creating the window
window = tk.Tk()
window.title("Időjárás")
window.geometry("900x500")
window.resizable(False, False)
window.configure(bg="black")


ttk.Label(window, text="Időjárás", font=("Arial", 20), foreground="white", background="black").grid(column=0, row=0)
window.mainloop()
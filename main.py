import customtkinter
import requests
import datetime as dt
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import customtkinter as ctk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


# base request URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# loading the API key
API_KEY = open("api_key", "r").read()

# user credentials for proxy
USER = open("username", "r").read()
PASSW = open("password", "r").read()

KELVIN_CELSIUS = 273.15
KELVIN_FAHRENHEIT = 457.87


# converting Kelvin to Celsius
def celsius() -> str:
    return str(int(resp['main']['temp'])) + "°C"


def feels_like_celsius() -> str:
    return sky() + " | Hőérzet " + str(int(resp['main']['feels_like'])) + "°C"


def temp_min_celsius() -> str:
    return str(int(resp['main']['temp_min'])) + "°C"


def temp_max_celsius() -> str:
    return str(int(resp['main']['temp_max'])) + "°C"


# converting kelvin to fahrenheit

def fahrenheit() -> str:
    return str(int(resp['main']['temp'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


def feels_like_fahrenheit() -> str:
    return "HŐÉRZET " + str(int(resp['main']['feels_like'] * (9 / 5) - KELVIN_FAHRENHEIT)) + "°F"


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
        return "Tiszta"
    elif weather == "Clouds":
        return "Felhős"
    elif weather == "Rain":
        return "Esős"
    elif weather == "Thunderstorm":
        return "Viharos"
    elif weather == "Snow":
        return "Havazik"
    elif weather == "Mist":
        return "Ködös"


def sky_description() -> str:
    return resp['weather'][0]['description']


def humidity() -> str:
    return str(resp['main']['humidity']) + "%"


def pressure() -> str:
    return str(resp['main']['pressure']) + " hPa"


def wind_speed() -> str:
    return str(int(resp['wind']['speed'] * 3.6)) + " km/h"


# clock
def time():
    string = dt.datetime.now().strftime("%H:%M:%S")
    lbl.config(text=string)
    # update every second
    lbl.after(1000, time)

def current_date():
    string = dt.datetime.now().strftime("%Y-%m-%d")
    lbl2.config(text=string)

def for_weather_icon() -> str:
    if sky() == "Clear" or sky() == "Clear sky" or sky() == "Sunny" or sky()  == "Tiszta":
        return "assets/sunny.png"
    elif sky() == "Clouds" or sky() == "Few clouds" or sky() == "Scattered clouds" or sky() == "Broken clouds" or \
            sky() == "Felhős":
        return "assets/rain.png"
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
        return "assets/storm.png"
    elif sky() == "Snow" or sky() == "Light snow" or sky() == "Heavy snow" or sky() == "Sleet" or \
            sky() == "Light shower sleet" or sky() == "Shower sleet" or sky() == "Light rain and snow" or \
            sky() == "Rain and snow" or sky() == "Light shower snow" or sky() == "Shower snow" or \
            sky() == "Heavy shower snow" or sky() == "Havazik":
        return "assets/snowy.png"
    elif sky() == "Mist" or sky() == "Smoke" or sky() == "Haze" or sky() == "Sand, dust whirls" or \
            sky() == "Fog" or sky() == "Sand" or sky() == "Dust" or sky() == "Volcanic ash" or \
            sky() == "Squalls" or sky() == "Tornado" or sky() == "Ködös":
        return "assets/cloudy2.png"


def exec_city_req():
    if CITY.get() == "":
        CITY.set("Dunaújváros")
        return BASE_URL + "q=" + CITY.get() + "&lang=hu&appid=" + API_KEY + "&units=metric"
    else:
        print(CITY.get())
        return BASE_URL + "q=" + CITY.get() + "&lang=hu&appid=" + API_KEY + "&units=metric"


# Q_URL = BASE_URL + "q=" + CITY.get() + "&appid=" + API_KEY

# main proxy
http_proxy = "http://" + USER + ":" + PASSW + "@proxy.dunaferr.hu:8080"

# proxies
proxies = {
    "http": http_proxy,
    "https": http_proxy
}

# # print(resp)
# print(celsius())
# print(fahrenheit())
# print(sky())
# print(humidity())
# print(pressure())
# print(wind_speed())

# creating the window
window = ctk.CTk()
window.title("Weather App")
window.geometry("900x500")
window.resizable(False, False)

# window.configure(background="#00A5F9")


# creating the background
background = ImageTk.PhotoImage(file="assets/sky2.jpeg")
Label(image=background).place(relx=0.5, rely=0.5, anchor=CENTER)



CITY = tk.StringVar()

# response from the API
resp = requests.get(exec_city_req()).json()

print(resp)

# creating the search bar
search_bar = ImageTk.PhotoImage(file="assets/search_bar2.png")
Label(image=search_bar, bg="#00A5F9", fg="white").place(relx=0.5, rely=0.13, anchor=CENTER)
print(CITY.get())

info_bar = ImageTk.PhotoImage(file="assets/bar.png")
info_label = Label(image=info_bar)
info_label.place(relx=0.5, rely=0.7, anchor=CENTER)

# input field
Entry(window, font=("Arial", 14), foreground="black", border=0, textvariable=CITY) \
    .place(width=200, height=25, relx=0.5, rely=0.13, anchor=CENTER)


def save_city():
    city = CITY.get()
    return city


def update_data():
    # call the API and update the data
    global resp, weather_photo
    param = BASE_URL + "q=" + save_city() + "&lang=hu&appid=" + API_KEY + "&units=metric"
    resp = requests.get(param).json()
    print(resp)

    if resp.get("cod") == 200:
        # update the weather icon
        weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
        weather_label.configure(image=weather_photo)
        city_label.configure(text=CITY.get())

        # update the temperature
        celsius_label.configure(text=celsius())
        feels_like_celsius_label.configure(text=feels_like_celsius())

        # update other information
        humidity_label.configure(text=humidity())
        pressure_label.configure(text=pressure())
        wind_speed_label.configure(text=wind_speed())
        sky_description_label.configure(text=sky_description())
    elif resp.get("cod") == "404":
        city_not_found_popup()

    # schedule the function to be called again after 2 minutes
    window.after(120000, update_data)


def city_not_found_popup():
    popup = tk.Toplevel()
    popup.title("Hiba!")
    popup.geometry("300x100")
    popup.resizable(False, False)

    message = Label(popup, text="Nem található a város!", font=("Arial", 14), background="white", foreground="black")
    message.place(relx=0.5, rely=0.3, anchor=CENTER)

    tk.Button(popup, text="Ok", command=popup.destroy).place(relx=0.5, rely=0.7, anchor=CENTER)


# schedule the first call to the function
window.after(12000, update_data)

# creating the search button
search_icon = ImageTk.PhotoImage(file="assets/search_icon.png")
Button(image=search_icon, bg="white", fg="white", border=0, text="save", command=update_data) \
    .place(relx=0.63, rely=0.13, anchor=CENTER)

# clock
lbl = Label(window, font=("Arial", 20, 'bold'), background="white", foreground="black")
lbl.place(relx=0.8, rely=0.3, anchor=CENTER)
time()

lbl2 = Label(window, font=("Arial", 20, 'bold'), background="white", foreground="black")
lbl2.place(relx=0.8, rely=0.4, anchor=CENTER)
current_date()

# create the weather icon label and keep a reference to it
weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
weather_label = Label(image=weather_photo, bg="black", fg="white")
weather_label.place(relx=0.2, rely=0.3, anchor=CENTER)

city_label = Label(window, text=CITY.get(), font=("Sans", 16, 'bold'), background="#00A5F9", foreground="white")
city_label.place(relx=0.2, rely=0.54, anchor=CENTER)

"""                     temperature                     """


# create the temperature labels and keep references to them
celsius_label = Label(window, text=celsius(), font=("Arial", 35, 'bold'), bg="black", foreground="#D40C00")
celsius_label.place(relx=0.4, rely=0.3, anchor=CENTER)

feels_like_celsius_label = Label(window, text=feels_like_celsius(), font=("Arial", 16, 'bold'), background="black",
                                 foreground="white")
feels_like_celsius_label.place(relx=0.45, rely=0.4, anchor=CENTER)

"""                     other infos                     """

# create other information labels and keep references to them
humidity_label = Label(window, text=humidity(), font=("Arial", 15, 'bold'), background="#00A5F9", foreground="white")
humidity_label.place(relx=0.2, rely=0.725, anchor=CENTER)

pressure_label = Label(window, text=pressure(), font=("Arial", 15, 'bold'), background="#00A5F9", foreground="#00008B")
pressure_label.place(relx=0.4, rely=0.725, anchor=CENTER)

wind_speed_label = Label(window, text=wind_speed(), font=("Arial", 15, 'bold'), background="#00A5F9",
                         foreground="#00008B")
wind_speed_label.place(relx=0.5, rely=0.725, anchor=CENTER)

sky_description_label = Label(window, text=sky_description(), font=("Arial", 15, 'bold'), background="#00A5F9",
                              foreground="#00008B")
sky_description_label.place(relx=0.74, rely=0.725, anchor=CENTER)

window.mainloop()

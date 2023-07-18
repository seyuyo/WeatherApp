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
    return str(int(resp['main']['temp'])) + "°"


"""
        what the weather feels like in celsius
"""


def feels_like_celsius() -> str:
    return "Hőérzet |" + str(int(resp['main']['feels_like'])) + "°C"


"""
    Minimum and maximum temperature in celsius
"""


def temp_min_celsius() -> str:
    return str(int(resp['main']['temp_min'])) + "°C"


def temp_max_celsius() -> str:
    return str(int(resp['main']['temp_max'])) + "°C"


def temp_min_max_celsius() -> str:
    return str(int(resp['main']['temp_min'])) + "°C / " + str(int(resp['main']['temp_max'])) + "°C"


"""
        converting kelvin to fahrenheit
"""


def fahrenheit() -> str:
    return str(int(resp['main']['temp'] * (9 / 5) + 32)) + "°"


"""
        what the weather feels like in fahrenheit
"""


def feels_like_fahrenheit() -> str:
    return "Hőérzet |" + str(int(resp['main']['feels_like'] * (9 / 5) + 32)) + "°F"


"""
    Minimum and maximum temperature in fahrenheit
"""


def temp_min_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) + 32)) + "°F"


def temp_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) + 32)) + "°F"


def temp_min_max_fahrenheit() -> str:
    return str(int(resp['main']['temp_min'] * (9 / 5) + 32)) + "°F / " + \
        str(int(resp['main']['temp_max'] * (9 / 5) + 32)) + "°F"


"""
        Getting the pollution level in integer and returning the string value in hungarian
"""


def air_pollution() -> str:
    pollution = coordinate_to_city()

    if pollution == 1:
        return "|AQI Kiváló"
    elif pollution == 2:
        return "|AQI Jó"
    elif pollution == 3:
        return "|AQI megfelelő"
    elif pollution == 4:
        return "|AQI Részben rossz"
    elif pollution == 5:
        return "|AQI Rossz"


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


def sky2(index=0):
    weather = data['list'][index]['weather'][0]['main']
    print(weather)
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
    return "Szélsebesség |" + str(round(float(resp['wind']['speed'] * 2.237), 1)) + " mi/h"


""" Time hour:minute:second restarts every second """


def time():
    string = dt.datetime.now().strftime("%H:%M:%S")
    lbl.config(text=string)
    # update every second
    lbl.after(1000, time)


""" Choose the weather icon based on the weather """

def error_not_found() -> str:
    global window
    root = tk.Toplevel(window)
    root.title("Hiba!")
    root.geometry("300x100+800+450")
    root.resizable(False, False)

    error_label = tk.Label(root, text="Nem található ilyen város!", font=("Arial", 14, "bold"), fg="red")
    error_label.pack(pady=10)

    error_button = tk.Button(root, text="Bezárás", font=("Arial", 12), command=root.destroy, bg="black", fg="white")
    error_button.pack(pady=10)

    error_label.after(5000, root.destroy)

def for_weather_icon() -> str:

    clear_conditions = ["Clear", "Derült"]

    cloudy_conditions = ["Clouds", "Few clouds", "Scattered clouds", "Broken clouds", "Overcast clouds", "Felhős"]

    rainy_conditions = ["Rain", "Light rain", "Moderate rain", "Heavy rain", "Very heavy rain", "Extreme rain",
                        "Freezing rain", "Light intensity shower rain", "Shower rain", "Heavy intensity shower rain",
                        "Ragged shower rain", "Esős"]

    snow_conditions = ["Snow", "Light snow", "Heavy snow", "Sleet", "Light shower sleet", "Shower sleet",
                       "Light rain and snow", "Rain and snow", "Light shower snow", "Shower snow",
                       "Heavy shower snow", "Havazás"]

    mist_conditions = ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Dust", "Ash", "Squall", "Tornado", "Ködös"]

    thunderstorm_conditions = ["Thunderstorm", "Thunderstorm with light rain", "Thunderstorm with rain",
                               "Thunderstorm with heavy rain", "Light thunderstorm", "Heavy thunderstorm",
                               "Ragged thunderstorm", "Thunderstorm with light drizzle",
                               "Thunderstorm with drizzle", "Thunderstorm with heavy drizzle", "Viharos"]


    if sky() in clear_conditions:
        return "assets/sunny.png"
    elif sky() in cloudy_conditions:
        return "assets/cloudy.png"
    elif sky() in rainy_conditions:
        return "assets/rainy.png"
    elif sky() in snow_conditions:
        return "assets/snowy.png"
    elif sky() in mist_conditions:
        return "assets/foggy.png"
    elif sky() in thunderstorm_conditions:
        return "assets/thunderstorm.png"


def for_weather_icon2():
    if sky2(0) == "Derült" or sky2(0) == "Clear":
        return "assets/sunny.png"
    elif sky2(0) == "Felhős" or sky2(0) == "Clouds":
        return "assets/cloudy.png"
    elif sky2(0) == "Esős" or sky2(0) == "Rain":
        return "assets/rainy.png"
    elif sky2(0) == "Havazás" or sky2(0) == "Snow":
        return "assets/snowy.png"
    elif sky2(0) == "Ködös" or sky2(0) == "Mist":
        return "assets/foggy.png"
    elif sky2(0) == "Viharos" or sky2(0) == "Thunderstorm":
        return "assets/thunderstorm.png"

def for_weather_icon3():
    if sky2(1) == "Derült" or sky2(1) == "Clear":
        return "assets/sunny.png"
    elif sky2(1) == "Felhős" or sky2(1) == "Clouds":
        return "assets/cloudy.png"
    elif sky2(1) == "Esős" or sky2(1) == "Rain":
        return "assets/rainy.png"
    elif sky2(1) == "Havazás" or sky2(1) == "Snow":
        return "assets/snowy.png"
    elif sky2(1) == "Ködös" or sky2(1) == "Mist":
        return "assets/foggy.png"
    elif sky2(1) == "Viharos" or sky2(1) == "Thunderstorm":
        return "assets/thunderstorm.png"

def for_weather_icon4():
    if sky2(2) == "Derült" or sky2(2) == "Clear":
        return "assets/sunny.png"
    elif sky2(2) == "Felhős" or sky2(2) == "Clouds":
        return "assets/cloudy.png"
    elif sky2(2) == "Esős" or sky2(2) == "Rain":
        return "assets/rainy.png"
    elif sky2(2) == "Havazás" or sky2(2) == "Snow":
        return "assets/snowy.png"
    elif sky2(2) == "Ködös" or sky2(2) == "Mist":
        return "assets/foggy.png"
    elif sky2(2) == "Viharos" or sky2(2) == "Thunderstorm":
        return "assets/thunderstorm.png"


def for_weather_icon5():
    for i in range(4):
        if sky2(3) == "Derült" or sky2(3) == "Clear":
            return "assets/sunny.png"
        elif sky2(3) == "Felhős" or sky2(3) == "Clouds":
            return "assets/cloudy.png"
        elif sky2(3) == "Esős" or sky2(3) == "Rain":
            return "assets/rainy.png"
        elif sky2(3) == "Havazás" or sky2(3) == "Snow":
            return "assets/snowy.png"
        elif sky2(3) == "Ködös" or sky2(3) == "Mist":
            return "assets/foggy.png"
        elif sky2(3) == "Viharos" or sky2(3) == "Thunderstorm":
            return "assets/thunderstorm.png"

""" Compiles the request URL based on the city name """

def exec_city_req():
    if CITY.get() == "":
        CITY.set("Dunaújváros")
        return f"{BASE_URL}q={CITY.get()}&lang=hu&appid={API_KEY}&units=metric"
    else:
        print(CITY.get().capitalize())
        return f"{BASE_URL}q={CITY.get()}&lang=hu&appid={API_KEY}&units=metric"


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

canvas_black = tk.Canvas(window, width=600, height=0.5, border=0, borderwidth=0, highlightthickness=0)
canvas_black.place(x=150, y=300)
canvas_black.configure(background='#878787', border=0)
canvas_black.create_line(0, 0, 600, 0, fill="#878787", width=0)

CITY = tk.StringVar()

# response from the API
resp = requests.get(exec_city_req(), proxies=proxies).json()

print(resp)

""" which unit is active: Celsius """


def active_button_celsius():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label, data

    isCelsius = True
    isFahrenheit = False

    to_celsius_button.configure(background="black", foreground="#878787")

    to_fahrenheit_button.configure(background="#878787", foreground="black")

    celsius_label.configure(text=celsius())

    feels_like_celsius_label.configure(text=feels_like_celsius())

    wind_speed_label.configure(text=wind_speed())

    min_max_celsius.configure(text=temp_min_max_celsius())

    label_data1.configure(text=str(int(data["list"][0]["main"]["temp"])) + "°C")
    label_data2.configure(text=str(int(data["list"][1]["main"]["temp"])) + "°C")
    label_data3.configure(text=str(int(data["list"][2]["main"]["temp"])) + "°C")
    label_data4.configure(text=str(int(data["list"][3]["main"]["temp"])) + "°C")


""" which unit is active: Fahrenheit """


def active_button_fahrenheit():
    global isCelsius, isFahrenheit, to_celsius_button, to_fahrenheit_button, celsius_label, data

    isCelsius = False
    isFahrenheit = True

    to_celsius_button.configure(background="#878787", foreground="black")

    to_fahrenheit_button.configure(background="black", foreground="#878787")

    celsius_label.configure(text=fahrenheit())

    feels_like_celsius_label.configure(text=feels_like_fahrenheit())

    wind_speed_label.configure(text=wind_speed_mph())

    min_max_celsius.configure(text=temp_min_max_fahrenheit())

    label_data1.configure(text=str(int(data["list"][0]["main"]["temp"] * (9 / 5) + 33.8)) + "°F")
    label_data2.configure(text=str(int(data["list"][1]["main"]["temp"] * (9 / 5) + 33.8)) + "°F")
    label_data3.configure(text=str(int(data["list"][2]["main"]["temp"] * (9 / 5) + 33.8)) + "°F")
    label_data4.configure(text=str(int(data["list"][3]["main"]["temp"] * (9 / 5) + 33.8)) + "°F")



def save_city():
    city = CITY.get()
    return city.capitalize()


def update_data():
    # call the API and update the data
    global resp, weather_photo, weather1, weather2, weather3, weather4, data
    param = f"{BASE_URL}q={save_city()}&lang=hu&appid={API_KEY}&units=metric"
    param2 = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY.get()}&exclude=daily,minutely&lang=hu&appid={API_KEY}&units=metric"

    resp = requests.get(param, proxies=proxies).json()
    data = requests.get(param2, proxies=proxies).json()
    print(resp)

    if resp.get("cod") == 200:
        # update the weather icon
        weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
        weather_label.configure(image=weather_photo, background="#878787")
        city_label.configure(text=CITY.get().capitalize())

        weather1 = ImageTk.PhotoImage(file=for_weather_icon2())
        label_weather1.configure(image=weather1, background="#878787")

        weather2 = ImageTk.PhotoImage(file=for_weather_icon3())
        label_weather2.configure(image=weather2, background="#878787")

        weather3 = ImageTk.PhotoImage(file=for_weather_icon4())
        label_weather3.configure(image=weather3, background="#878787")

        weather4 = ImageTk.PhotoImage(file=for_weather_icon5())
        label_weather4.configure(image=weather4, background="#878787")

        # update the temperature
        if isCelsius:
            celsius_label.configure(text=celsius())
            wind_speed_label.configure(text=wind_speed())
            feels_like_celsius_label.configure(text=feels_like_celsius())
            min_max_celsius.configure(text=temp_min_max_celsius())
            label_data1.configure(text=str(int(data["list"][0]["main"]["temp"])) + "°C")
            label_data2.configure(text=str(int(data["list"][1]["main"]["temp"])) + "°C")
            label_data3.configure(text=str(int(data["list"][2]["main"]["temp"])) + "°C")
            label_data4.configure(text=str(int(data["list"][3]["main"]["temp"])) + "°C")
        elif isFahrenheit:
            celsius_label.configure(text=fahrenheit())
            wind_speed_label.configure(text=wind_speed_mph())
            feels_like_celsius_label.configure(text=feels_like_fahrenheit())
            min_max_celsius.configure(text=temp_min_max_fahrenheit())

            label_data1.configure(text=str(int(data["list"][0]["main"]["temp"] * (9/5) + 33.8)) + "°F")
            label_data2.configure(text=str(int(data["list"][1]["main"]["temp"] * (9/5) + 33.8)) + "°F")
            label_data3.configure(text=str(int(data["list"][2]["main"]["temp"] * (9/5) + 33.8)) + "°F")
            label_data4.configure(text=str(int(data["list"][3]["main"]["temp"] * (9/5) + 33.8)) + "°F")


        # update other information
        humidity_label.configure(text=humidity())
        pressure_label.configure(text=pressure())
        sky_label.configure(text=sky())
        sky_label_description.configure(text=sky_description())
    else:
        error_not_found()
        print("City not found", CITY.get().capitalize())

    # schedule the function to be called again after 2 minutes
    window.after(120000, update_data)


# schedule the first call to the function
window.after(12000, update_data)

# CLOCK
lbl = Label(window, font=("Open sans", 20, 'bold'), background="#878787", foreground="black")
lbl.place(relx=0.8, rely=0.3, anchor=CENTER)
time()

# create the weather icon label and keep a reference to it
weather_photo = ImageTk.PhotoImage(file=for_weather_icon())
weather_label = Label(image=weather_photo, bg="#878787", fg="white")
weather_label.place(relx=0.4, rely=0.26, anchor=CENTER)

city_label = Label(window, text=CITY.get(), font=("Open sans", 28, 'bold'), background="#878787", foreground="black")
city_label.place(relx=0.5, rely=0.12, anchor=CENTER)

"""                     temperature                     """

# create the temperature labels and keep references to them

celsius_label = Label(window, text=celsius(), font=("Arial", 32, 'bold'), background="#878787", foreground="black")
celsius_label.place(relx=0.495, rely=0.26, anchor=CENTER)

feels_like_celsius_label = Label(window, text=feels_like_celsius(), font=("Open sans", 15, 'bold'),
                                 background="#878787",
                                 foreground="black")
feels_like_celsius_label.place(relx=0.275, rely=0.45, anchor=CENTER)

"""                     other infos                     """

# create other information labels and keep references to them

humidity_label = Label(window, text=humidity(), font=("Open sans", 15, 'bold'), background="black",
                       foreground="#878787")
humidity_label.place(relx=0.275, rely=0.55, anchor=CENTER)

pressure_label = Label(window, text=pressure(), font=("Open sans", 15, 'bold'), background="#878787",
                       foreground="black")
pressure_label.place(relx=0.52, rely=0.45, anchor=CENTER)

wind_speed_label = Label(window, text=wind_speed(), font=("Open sans", 15, 'bold'), background="black",
                         foreground="#878787")
wind_speed_label.place(relx=0.52, rely=0.55, anchor=CENTER)

sky_label = Label(window, text=sky(), font=("Open sans", 15, 'bold'), background="#878787", foreground="black")
sky_label.place(relx=0.41, rely=0.37, anchor=CENTER)

aqi_label = Label(window, text=air_pollution(), font=("Open sans", 15, 'bold'), background="#878787",
                  foreground="black")
aqi_label.place(relx=0.53, rely=0.37, anchor=CENTER)

sky_label_description = Label(window, text=sky_description(), font=("Open sans", 15, 'bold'), background="#878787",
                              foreground="black")
sky_label_description.place(relx=0.75, rely=0.45, anchor=CENTER)

min_max_celsius = Label(window, text=temp_min_max_celsius(), font=("Open sans", 15, 'bold'), background="black",
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

url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY.get()}&exclude=daily,minutely&lang=hu&appid={API_KEY}&units=metric"
data = requests.get(url, proxies=proxies).json()
print(data)
forecast_data = {}

for forecast in data["list"]:
    timestamp = forecast["dt_txt"]
    temp = forecast["main"]["temp"]
    weather_description = forecast["weather"][0]["description"]
    print(forecast["weather"][0]["main"])
    print(f"{timestamp}: {temp} C, {weather_description}")


canvas = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas.place(relx=0.2, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas.create_polygon(x1 + radius, y1, x2 - radius, y1, x2, y1 + radius, x2, y2 - radius,
                      x2 - radius, y2, x1 + radius, y2, x1, y2 - radius, x1, y1 + radius,
                      outline='#878787', fill='#878787')

canvas2 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas2.place(relx=0.4, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas2.create_polygon(x1 + radius, y1, x2 - radius, y1, x2, y1 + radius, x2, y2 - radius,
                       x2 - radius, y2, x1 + radius, y2, x1, y2 - radius, x1, y1 + radius,
                       outline='#878787', fill='#878787')

canvas3 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas3.place(relx=0.6, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas3.create_polygon(x1 + radius, y1, x2 - radius, y1, x2, y1 + radius, x2, y2 - radius,
                       x2 - radius, y2, x1 + radius, y2, x1, y2 - radius, x1, y1 + radius,
                       outline='#878787', fill='#878787')

canvas4 = Canvas(window, width=150, height=150, background="black", highlightthickness=0)
canvas4.place(relx=0.8, rely=0.8, anchor=CENTER, x=0, y=0)

# Lekerekített négyzet rajzolása
x1, y1 = 0, 0
x2, y2 = 150, 150
radius = 15

canvas4.create_polygon(x1 + radius, y1, x2 - radius, y1, x2, y1 + radius, x2, y2 - radius,
                       x2 - radius, y2, x1 + radius, y2, x1, y2 - radius, x1, y1 + radius,
                       outline='#878787', fill='#878787')

date_txt = data["list"][0]["dt_txt"]
date = date_txt.split(" ")

label_date = Label(window, text=date[0], font=("Open sans", 20, 'bold'), background="#878787",
                   foreground="black")
label_date.place(relx=0.18, rely=0.3, anchor=CENTER)

label_time1 = Label(window, text=data["list"][0]["dt_txt"].split(" ")[1], font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_time1.place(relx=0.2, rely=0.7, anchor=CENTER)

label_time2 = Label(window, text=data["list"][1]["dt_txt"].split(" ")[1], font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_time2.place(relx=0.4, rely=0.7, anchor=CENTER)

label_time3 = Label(window, text=data["list"][2]["dt_txt"].split(" ")[1], font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_time3.place(relx=0.6, rely=0.7, anchor=CENTER)

label_time4 = Label(window, text=data["list"][3]["dt_txt"].split(" ")[1], font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_time4.place(relx=0.8, rely=0.7, anchor=CENTER)

temperature = data["list"][0]["main"]["temp"]
temperature = int(temperature)
temperature = str(temperature) + "°C"

label_data1 = Label(window, text=str(int(data["list"][0]["main"]["temp"])) + "°C", font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_data1.place(relx=0.2, rely=0.77, anchor=CENTER)

label_data2 = Label(window, text=str(int(data["list"][1]["main"]["temp"])) + "°C", font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_data2.place(relx=0.4, rely=0.77, anchor=CENTER)

label_data3 = Label(window, text=str(int(data["list"][2]["main"]["temp"])) + "°C", font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_data3.place(relx=0.6, rely=0.77, anchor=CENTER)

label_data4 = Label(window, text=str(int(data["list"][3]["main"]["temp"])) + "°C", font=("Open sans", 16, 'bold'),
                    background="#878787", foreground="black")
label_data4.place(relx=0.8, rely=0.77, anchor=CENTER)

weather1 = ImageTk.PhotoImage(file=for_weather_icon2())
label_weather1 = Label(window, image=weather1, background="#878787")
label_weather1.place(relx=0.2, rely=0.86, anchor=CENTER)

weather2 = ImageTk.PhotoImage(file=for_weather_icon3())
label_weather2 = Label(window, image=weather2, background="#878787")
label_weather2.place(relx=0.4, rely=0.86, anchor=CENTER)

weather3 = ImageTk.PhotoImage(file=for_weather_icon4())
label_weather3 = Label(window, image=weather3, background="#878787")
label_weather3.place(relx=0.6, rely=0.86, anchor=CENTER)

weather4 = ImageTk.PhotoImage(file=for_weather_icon5())
label_weather4 = Label(window, image=weather4, background="#878787")
label_weather4.place(relx=0.8, rely=0.86, anchor=CENTER)

window.mainloop()

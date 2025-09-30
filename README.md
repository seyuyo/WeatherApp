# WeatherApp

Egy egyszerű, de fejlődőképes időjárás-alkalmazás, amely lehetővé teszi a felhasználók számára, hogy városok szerint lekérjék az aktuális időjárást.  

## Tartalomjegyzék

- [Jellemzők](#jellemzők)  
- [Működés](#működés)  
- [Technológiák](#technológiák)  
- [Telepítés és futtatás](#telepítés-és-futtatás)  
- [API kulcs](#api-kulcs)  
- [Használat](#használat)  
- [Fejlesztési irányok](#fejlesztési-irányok)   

---

## Jellemzők

- Város keresése név alapján  
- Aktuális időjárási adatok megjelenítése  
- Több város mentése kedvencként  
- Egyszerű, letisztult UI  
- (Bővíthető: 5-napos előrejelzés, grafikonok, riasztások)  

## Működés

1. A felhasználó beír egy városnevet a keresőmezőbe.  
2. A rendszer az OpenWeatherMap vagy más időjárási API felé küld HTTP kérésben (GET).  
3. Az API válaszként JSON formátumban küldi a város aktuális adatait.  
4. Az alkalmazás kiolvassa a JSON mezőket (pl. hőmérséklet, páratartalom, leírás) és megjeleníti azokat a felhasználónak.  
5. A kedvenc városokat elmenti (pl. helyi adatbázisban vagy fájlban), hogy gyorsan visszakereshetők legyenek.  

<img width="1440" height="835" alt="image" src="https://github.com/user-attachments/assets/a97e289e-70f5-4eca-8398-6493d77df5c7" />


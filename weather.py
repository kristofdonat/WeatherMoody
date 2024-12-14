import requests

def get_weather(city_name, api_key):
    """
    Lekérdezi az aktuális időjárást az OpenWeatherMap API használatával.
    
    :param city_name: A település neve (string).
    :param api_key: Az OpenWeatherMap API kulcsa (string).
    :return: Az aktuális időjárás adatai (dictionary), vagy hibaüzenet.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params, verify=False)
        response.raise_for_status()  # Hibakezelés: dob egy kivételt, ha a státuszkód nem 200
        weather_data = response.json()
        return {
            "location": weather_data.get("name"),
            "temperature": weather_data["main"]["temp"],
            "weather": weather_data["weather"][0]["description"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Hiba történt az időjárás lekérdezésekor: {e}"}
    except KeyError:
        return {"error": "Hiba történt az API válaszának feldolgozásakor."}

def load_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        raise Exception(f"API key file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading API key: {e}")

api_key_file = 'weatherapikey.key'
api_key = load_api_key(api_key_file)
city_name = "Gyor"
weather_info = get_weather(city_name, api_key)
print(weather_info)

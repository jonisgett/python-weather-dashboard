import requests
import json
from dotenv import load_dotenv
import os

class WeatherDashboard:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.favorite_cities = []
        self.load_favorites()

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as file:
                self.favorite_cities = json.load(file)
                self.favorite_cities.sort()
        except FileNotFoundError:
            pass

    def show_favorite_cities(self):
        sorted_fav_cities = sorted(self.favorite_cities)
        for i, city in enumerate(sorted_fav_cities, start=1):
            print(f"{i}: {city}")

    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        #check to see if it's a valid city and something comes back:
        if response.status_code != 200:
            return None
        
        data = response.json()
        weather_city = {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_city
    
    def print_cleaned(self, city, weather_city):
        # print out results nicely
        print(f"{city} weather:")
        print(f"Temperature: {weather_city['temp']}°C")
        print(f"Feels like: {weather_city['feels_like']}°C")
        print(f"Conditions: {weather_city['description']}")
        print(f"Humidity: {weather_city['humidity']}%")
        print(f"Wind: {weather_city['wind_speed']}m/s")

    def add_fav_city(self, city):
        city_weather = self.get_weather(city)
        if city_weather:
            if city not in self.favorite_cities:
                self.favorite_cities.append(city)
            else:
                print(f"{city} already exists in Favorites.")
        else:
            print(f"{city} is not valid and can't be added.")

    def remove_fav_city(self, city):
        self.favorite_cities.remove(city)

    def save_favorites(self):
        with open('favorites.json', 'w') as file:
            json.dump(self.favorite_cities, file, indent=2)

def show_menu():
    print("===Weather Dashboard")
    print("1. View Weather for City")
    print("2. View Favorite Cities")
    print("3. Add City to Favorites")
    print("4. Remove City from Favorites")
    print("5. Quit")    

def get_menu_choice():
    while True:
        menu_choice = input("Please choose 1-5 from the menu: ")
        try:
            int_menu_choice = int(menu_choice)
            if int_menu_choice in range(1,6):
                break
            else:
                print("Invalid input.  A number from 1 to 5 is required")
        except ValueError:
            print("Invalid value.  A number from 1 to 5 is required.")
    return int_menu_choice  

def main():
    weather_dashboard = WeatherDashboard()

    while True:
        show_menu()
        menu_choice = get_menu_choice()

        if menu_choice == 1:
            input_city = input("Please enter a valid city: ")
            weather_city = weather_dashboard.get_weather(input_city)
            if weather_city:
                weather_dashboard.print_cleaned(input_city, weather_city)
            else:
                print(f"Could not find weather for {input_city}")
        elif menu_choice == 2:
            weather_dashboard.show_favorite_cities()
        elif menu_choice == 3:
            city = input("Enter city to add: ").strip()
            weather_dashboard.add_fav_city(city)
            weather_dashboard.save_favorites()
        elif menu_choice == 4:
            if not weather_dashboard.favorite_cities:
                print(f"No favorites yet!")
            else:
                weather_dashboard.show_favorite_cities()
                user_city = input("Please enter city to remove: ")
                if user_city in weather_dashboard.favorite_cities:
                    weather_dashboard.remove_fav_city(user_city)
                    weather_dashboard.save_favorites()
                else:
                    print(f"{user_city} is not in the Favorites list.")
        elif menu_choice == 5:
            print("Goodbye....")
            break

if __name__ == "__main__":
    main()
import json
import random
from dataclasses import dataclass, field
from typing import List, Set

class JsonFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден")
            return None
        except json.JSONDecodeError:
            print(f"Ошибка расшифровки JSON данных из файла {self.file_path}")
            return None

    def write_data(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка записи в {self.file_path}: {e}")

@dataclass
class City:
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = field(default=False)

    def __init__(self, name, population, subject, district, coords, is_used=False, **kwargs):
        self.name = name
        self.population = population
        self.subject = subject
        self.district = district
        self.latitude = float(coords['lat'])
        self.longitude = float(coords['lon'])
        self.is_used = is_used

class CitiesSerializer:
    def __init__(self, city_data: List[dict]):
        self.cities = []
        for city in city_data:
            try:
                self.cities.append(City(**city))
            except TypeError as e:
                print(f"Ошибка при создании объекта City для данных: {city}")
                print(f"Ошибка: {e}")

    def get_all_cities(self) -> List[City]:
        return self.cities

class CityGame:
    def __init__(self, cities_serializer):
        self.cities_serializer = cities_serializer
        self.cities_set = {city.name for city in cities_serializer.get_all_cities()}
        self.bad_letters = self.calculate_bad_letters()
        self.computer_city = ''

    def calculate_bad_letters(self) -> Set[str]:
        bad_letters = set()
        sym_lower_set = {city.name[-1].lower() for city in self.cities_serializer.get_all_cities()}
        cities_set = {city.name for city in self.cities_serializer.get_all_cities()}
        iter_count = 0

        for letter in sym_lower_set:
            for city in cities_set:
                first_letter = city[0]
                iter_count += 1
                if letter.lower() == first_letter.lower():
                    break
            else:
                bad_letters.add(letter)

        print(bad_letters)
        print(iter_count)
        return bad_letters

    def start_game(self):
        print("Игра началась!")
        self.computer_turn()

    def human_turn(self, city_input: str):
        if city_input not in self.cities_set:
            print('Такого города нет. Человек проиграл.')
            return False

        if self.computer_city:
            if city_input[0].lower() != self.computer_city[-1].lower():
                print('Невыполнение правил игры. Человек проиграл.')
                return False

        self.cities_set.remove(city_input)
        self.computer_turn(city_input)
        return True

    def computer_turn(self, human_city: str = ''):
        if not human_city:
            # Если human_city пустой, выбираем случайный город
            self.computer_city = random.choice(list(self.cities_set))
            print('Компьютер начал игру с города:', self.computer_city)
            self.cities_set.remove(self.computer_city)
            return

        for city in self.cities_set:
            if city[0].lower() == human_city[-1].lower():
                if city[-1].lower() in self.bad_letters:
                    continue
                self.computer_city = city
                print('Компьютер назвал город:', self.computer_city)
                self.cities_set.remove(self.computer_city)
                return
        print('Компьютер проиграл.')

    def check_game_over(self):
        if not self.cities_set:
            print('Игра закончена. Победил человек.')
            return True
        return False

    def save_game_state(self):
        # Метод для сохранения состояния игры, если необходимо
        pass

class GameManager:
    def __init__(self, json_file: JsonFile, cities_serializer: CitiesSerializer, city_game: CityGame):
        self.json_file = json_file
        self.cities_serializer = cities_serializer
        self.city_game = city_game

    def __call__(self):
        self.run_game()

    def run_game(self):
        self.city_game.start_game()
        while True:
            human_city = input('Введите город: ')
            if not self.city_game.human_turn(human_city):
                break
            if self.city_game.check_game_over():
                break
        self.display_game_result()

    def display_game_result(self):
        print("Игра завершена.")

if __name__ == "__main__":
    # Создание экземпляра JsonFile
    json_file = JsonFile('cities.json')

    # Чтение данных из JSON файла
    city_data = json_file.read_data()

    if city_data is not None:
        # Создание экземпляра CitiesSerializer
        cities_serializer = CitiesSerializer(city_data)

        # Создание экземпляра CityGame
        city_game = CityGame(cities_serializer)

        # Создание экземпляра GameManager
        game_manager = GameManager(json_file, cities_serializer, city_game)

        # Запуск игры
        game_manager()
    else:
        print("Не удалось загрузить данные из файла. Игра не может быть запущена.")

import json
import random
from dataclasses import dataclass, field
from typing import List, Set
import tkinter as tk
from tkinter import messagebox

class JsonFile:
    """
    Класс для обработки JSON файла.
    """

    def __init__(self, file_path: str):
        """
        Инициализатор класса JsonFile.

        :param file_path: Путь к JSON файлу.
        """
        self.file_path = file_path

    def read_data(self):
        """
        Функция для чтения данных из JSON файла.

        :return: Данные из JSON файла или None в случае ошибки.
        """
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
        """
        Функция для записи данных в JSON файл.

        :param data: Данные для записи в JSON файл.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка записи в {self.file_path}: {e}")

@dataclass
class City:
    """
    Дата-класс для хранения информации о городах в игре.
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = field(default=False)

    def __init__(self, name: str, population: int, subject: str, district: str, coords: dict, is_used: bool = False, **kwargs):
        """
        Инициализатор класса City.

        :param name: Название города.
        :param population: Население города.
        :param subject: Субъект федерации.
        :param district: Район.
        :param coords: Координаты города (широта и долгота).
        :param is_used: Флаг, указывающий, использовался ли город в игре.
        """
        self.name = name
        self.population = population
        self.subject = subject
        self.district = district
        self.latitude = float(coords['lat'])
        self.longitude = float(coords['lon'])
        self.is_used = is_used

class CitiesSerializer:
    """
    Класс для сериализации данных о городах.
    """

    def __init__(self, city_data: List[dict]):
        """
        Инициализатор класса CitiesSerializer.

        :param city_data: Список словарей с данными о городах.
        """
        self.cities = []
        for city in city_data:
            try:
                self.cities.append(City(**city))
            except TypeError as e:
                print(f"Ошибка при создании объекта City для данных: {city}")
                print(f"Ошибка: {e}")

    def get_all_cities(self) -> List[City]:
        """
        Возвращает список всех городов.

        :return: Список объектов City.
        """
        return self.cities

class CityGame:
    """
    Класс для управления игрой "Города".
    """

    def __init__(self, cities_serializer: CitiesSerializer):
        """
        Инициализатор класса CityGame.

        :param cities_serializer: Сериализатор данных о городах.
        """
        self.cities_serializer = cities_serializer
        self.cities_set = {city.name for city in cities_serializer.get_all_cities()}
        self.bad_letters = self.calculate_bad_letters()
        self.computer_city = ''
        self.last_letter = ''

    def calculate_bad_letters(self) -> Set[str]:
        """
        Вычисляет набор "плохих" букв, на которые нельзя заканчивать город.

        :return: Набор "плохих" букв.
        """
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
        """
        Начинает игру.
        """
        print("Игра началась!")
        self.computer_turn()

    def human_turn(self, city_input: str) -> bool:
        """
        Обрабатывает ход человека.

        :param city_input: Название города, введенное человеком.
        :return: True, если ход успешен, иначе False.
        """
        if city_input not in self.cities_set:
            print('Такого города нет. Человек проиграл.')
            return False

        if self.computer_city:
            if city_input[0].lower() != self.last_letter.lower():
                print('Невыполнение правил игры. Человек проиграл.')
                return False

        self.cities_set.remove(city_input)
        self.computer_turn(city_input)
        return True

    def computer_turn(self, human_city: str = ''):
        """
        Обрабатывает ход компьютера.

        :param human_city: Название города, введенное человеком.
        """
        if not human_city:
            # Если human_city пустой, выбираем случайный город
            self.computer_city = random.choice(list(self.cities_set))
            print('Компьютер начал игру с города:', self.computer_city)
            self.cities_set.remove(self.computer_city)
            self.last_letter = self.computer_city[-1]
            return

        for city in self.cities_set:
            if city[0].lower() == human_city[-1].lower():
                self.computer_city = city
                self.last_letter = city[-1]
                if self.last_letter.lower() in self.bad_letters:
                    self.last_letter = city[-2]
                print('Компьютер назвал город:', self.computer_city)
                self.cities_set.remove(self.computer_city)
                return
        print('Компьютер проиграл.')

    def check_game_over(self) -> bool:
        """
        Проверяет, закончена ли игра.

        :return: True, если игра закончена, иначе False.
        """
        if not self.cities_set:
            print('Игра закончена. Победил человек.')
            return True
        return False

    def save_game_state(self):
        """
        Метод для сохранения состояния игры, если необходимо.
        """
        pass

class GameManager:
    """
    Класс для управления игровым процессом.
    """

    def __init__(self, json_file: JsonFile, cities_serializer: CitiesSerializer, city_game: CityGame):
        """
        Инициализатор класса GameManager.

        :param json_file: Объект JsonFile для работы с JSON файлом.
        :param cities_serializer: Сериализатор данных о городах.
        :param city_game: Объект CityGame для управления игрой.
        """
        self.json_file = json_file
        self.cities_serializer = cities_serializer
        self.city_game = city_game

    def __call__(self):
        """
        Запускает игру.
        """
        self.run_game()

    def run_game(self):
        """
        Основной цикл игры.
        """
        self.city_game.start_game()
        while True:
            human_city = input('Введите город: ')
            if not self.city_game.human_turn(human_city):
                break
            if self.city_game.check_game_over():
                break
        self.display_game_result()

    def display_game_result(self):
        """
        Отображает результат игры.
        """
        print("Игра завершена.")

class GameGUI:
    """
    Класс для графического интерфейса игры.
    """

    def __init__(self, root, city_game: CityGame):
        """
        Инициализатор класса GameGUI.

        :param root: Основное окно tkinter.
        :param city_game: Объект CityGame для управления игрой.
        """
        self.root = root
        self.city_game = city_game
        self.create_widgets()

    def create_widgets(self):
        """
        Создает виджеты для графического интерфейса.
        """
        self.label = tk.Label(self.root, text="Введите город:")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.submit_button = tk.Button(self.root, text="Отправить", command=self.human_turn)
        self.submit_button.pack()

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

    def human_turn(self):
        """
        Обрабатывает ход человека через графический интерфейс.
        """
        human_city = self.entry.get()
        if not self.city_game.human_turn(human_city):
            messagebox.showinfo("Игра завершена", "Человек проиграл.")
            self.root.quit()
        else:
            self.result_text.insert(tk.END, f"Человек: {human_city}\n")
            self.result_text.insert(tk.END, f"Компьютер: {self.city_game.computer_city}\n")
            if self.city_game.check_game_over():
                messagebox.showinfo("Игра завершена", "Победил человек.")
                self.root.quit()

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

        # Создание основного окна tkinter
        root = tk.Tk()
        root.title("Игра в города")

        # Создание экземпляра GameGUI
        game_gui = GameGUI(root, city_game)

        # Запуск основного цикла tkinter
        root.mainloop()
    else:
        print("Не удалось загрузить данные из файла. Игра не может быть запущена.")

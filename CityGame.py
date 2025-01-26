import json
from cities import cities_list
from dataclasses import dataclass, field
from typing import List

# Мы можем перепаковать города в сет
cities_set = {city['name'] for city in cities_list}

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
            print(f"ошибка расшифровки JSON данных из файла {self.file_path}")
            return None
    def write_data(self):
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

class CitiesSerializer:
    def __init__(self, city_data: List[dict]):
        self.cities = [City(**city) for city in city_data]
    def get_all_city(self) -> List[city]:
        return self.cities

 






# Собираем сет "плохих букв"
bad_letters = set()
iter_count = 0
# Внешний цикл для обхода последних букв
for letter in sym_lower_set:
    # Вложенный цикл для обхода первых букв
    for city_2 in cities_set:
        first_letter = city_2[0]
        iter_count += 1
        if letter.lower() == first_letter.lower():
            # Что происходит, если они равны? Это хорошая буква
            break
    else:
        # Если мы обошли весь сет и ни одно слово не начинается с нашей буквы - букву заносим как "плохую"
        bad_letters.add(letter)

print(bad_letters)
print(iter_count)

# 3. Мы можем начать писать игру
computer_city = ''
index = -1

while True:
    # Тут 
    # Ход человека
    human_city = input('Введите город: ')

    # Проверяем, что город есть в сете
    if human_city not in cities_set:
        print('Такого города нет. Человек проиграл.')
        break

    # Проверяем, что город соотсветствует правилам игры.
    # Если компьютер называл город:
    if computer_city:
        # Проверяем, что город начинается на последнюю букву предыдущего
        if human_city[0].lower() != computer_city[-1].lower():
            print('Невыполнение правил игры. Человек проиграл.')
            break
    
    # Удаляем город из сета
    cities_set.remove(human_city)

    # Ход компьютера

    # Тут мы можем пересчитать "Плохие буквы"

    # Обходим сет и ищем подходящий город
    for city in cities_set:
        if city[0].lower() == human_city[-1].lower():
            # Проверка на плохие буквы
            if city[-1].lower() in bad_letters:
                continue
            # Если все хорошо, то запоминаем город
            computer_city = city
            print('Компьютер назвал город:', computer_city)
            # Удаляем город из сета
            cities_set.remove(computer_city)
            break
    else:
        print('Компьютер проиграл.')
        break

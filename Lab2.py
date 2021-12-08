import sys
import re
import json
import argparse
from tqdm import tqdm
from typing import List

class Information:
    '''
           Объект класса Information содержит запись с информацией о пользователе.
           Attributes
           ----------
             telephone : str
               телефон пользователя
             height : str
               рост пользователя
             snils : str
               идентефикатор пользователя
             passport_series : str
               серия паспорта пользователя
             university : str
               университет пользователя
             age : str
               возраст пользователя
             academic_degree : str
               степень образования
             worldview : str
               мировоззрение пользователя
             address : str
               адрес пользователя
        '''

    telephone: str
    height: str
    snils: str
    passport_series: str
    university: str
    age: str
    academic_degree: str
    worldview: str
    address: str

    def  __init__(self, dic: dict):
        self.telephone = dic['telephone']
        self.height = dic['height']
        self.snils = dic['snils']
        self.passport_series = dic['passport_series']
        self.university = dic['university']
        self.age = dic['age']
        self.academic_degree = dic['academic_degree']
        self.worldview = dic['worldview']
        self.address = dic['address']

class InformationEncoder(json.JSONEncoder):
    def default(self,obj):
        return obj.__dict__


class Validator:
    '''
            Объект класса Validator является валидатором записей.
            Проверяет записи на корректность.
            Attributes
            ----------
              notes : List[Entry]
                Список записей
    '''

    notes: List[Information]

    def __init__(self, notes: List[Information]):
        self.notes = []
        for i in notes:
            self.notes.append(Information(i))

    def parse_note(self, notes: Information) -> List[str]:

        '''
                        Осуещствляет проверку корректности одной записи
                        Returns
                        -------
                          List[str]:
                            Список неверных ключей в записи
        '''
        incorrect_keys = []
        if self.check_telephone(notes.telephone) == 0:
            incorrect_keys.append('telephone')
        elif self.check_height(notes.height) == 0:
            incorrect_keys.append('height')
        elif self.check_snils(notes.snils) == 0:
            incorrect_keys.append('snils')
        elif self.check_passport_series(notes.passport_series) == 0:
            incorrect_keys.append('passport_series')
        elif self.check_university(notes.university) == 0:
            incorrect_keys.append('university')
        elif self.check_age(notes.age) == 0:
            incorrect_keys.append('age')
        elif self.check_academic_degree(notes.academic_degree) == 0:
            incorrect_keys.append('academic_degree')
        elif self.check_worldview(notes.worldview) == 0:
            incorrect_keys.append('worldview')
        elif self.check_address(notes.address) == 0:
            incorrect_keys.append('address')

        return incorrect_keys

    def parse(self) -> (List[List[str]], List[Information]):

        '''
                Осуществляет проверку корректности записей
                Returns
                -------
                  (List[List[str]], List[Entry]):
                    Пара: cписок списков неверных записей по названиям ключей и список верных записей
        '''

        incorrect_n = []
        correct_n = []
        for i in self.notes:
            incorrect_keys = self.parse_note(i)
            if len(incorrect_keys) != 0:
                incorrect_n.append(incorrect_keys)
            else:
                correct_n.append(i)
        #print(incorrect_n)
        return (incorrect_n, correct_n)


    def check_telephone(self, telephone: str) -> bool:
        """"Функция, которая провереряет номер Телефона на валидность"""
        pattern = "^\+7\-\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$"
        if re.match(pattern, telephone):
            return True
        return False


    def check_height(self, height:str) -> bool:
        """""Функция, которая провереряет Роста на валидность"""

        pattern = "^[0-2]\.([0-9]{2})$"
        if re.match(pattern, str(height)):
            return True
        return False


    def check_snils(self, snils:str) -> bool:
        """"Функция, которая провереряет СНИЛСа на валидность"""

        pattern = "^\\d{11}$"
        if re.match(pattern, snils):
            return True
        return False


    def check_passport_series(self, passport:str) -> bool:
        """""Функция, которая провереряет Серии паспортов на валидность"""

        pattern = "^(\d{2})+\s+(\d{2})$"
        if re.match(pattern, str(passport)):
            return True
        return False


    def check_university(self, university:str) -> bool:
        """Функция, которая провереряет названия университетов на валидность"""

        pattern = "^.*([У|у]нивер|[А|а]кадем|[T|т]ех|[И|и]нститут|им\.|[И-и]сслед|[А-Я]{2,}).*$"
        # ^([У|у]ниверситет|[А|а]кадем|[П|п]олитех|[И|и]нститут|им.|([А-Я]{3,}))+(\s|[а-я])$
        if re.match(pattern, university):
            return True
        return False


    def check_age(self, age:str) -> bool:
        """"Функция, которая провереряет возрастов людей на валидность"""

        try:
            age_1 = int(age)
        except ValueError:
            return False
        return 14 <= age_1 < 100

    def check_academic_degree(self,academic_degree:str) -> bool:
        """"Функция, которая провереряет академические степени на валидность"""

        pattern = "Бакалавр|Кандидат наук|Специалист|Магистр|Доктор наук"
        if re.match(pattern, academic_degree):
            return True
        return False


    def check_worldview(self,worldview:str ) -> bool:
        """"Функция, которая провереряет вероисповедания на валидность"""

        pattern = "^.*[П|А|К|С|Б|И]*(?:изм|анство)$"
        if re.match(pattern, worldview):
            return True
        return False


    def check_address(self, address:str) -> bool:
        """""Функция, которая провереряет адресса на валидность"""

        pattern = "^[\w\s\.\d-]* \d+$"
        if re.match(pattern,address):
            return True
        return False

def summary(result: List[List[str]], filename: str = ''):
    '''
          Предоставляет итоговую информацию об ошибках в записях
          Parameters
          ----------
            result : List[List[str]]
              Список списков неверных записей по названиям ключей
    '''
    all_errors_count = 0
    errors_count = {
        "telephone": 0,
        "height": 0,
        "snils": 0,
        "passport_series": 0,
        "university": 0,
        "age": 0,
        "academic_degree": 0,
        "worldview": 0,
        "address": 0,
    }
    for i in result:
        all_errors_count += 1
        for j in i:
            errors_count[j] += 1

    if filename == '':
        print('\n Ошибок в файле %d\n' % all_errors_count)
        print('Ошибки по типам: ')
        for key in errors_count.keys():
            print(key, errors_count[key], sep=' ')

    else:
        with open(filename, 'w') as file:
            file.write('Ошибок в файле  %d\n' % all_errors_count)
            for key in errors_count.keys():
                file.write(key + '\t' + str(errors_count[key]) + '\n')


def save_in_json(data: List[Information] , filename: str):
    with open(filename,'w',encoding='windows-1251') as output_file:
        json.dump(data,output_file,cls=InformationEncoder,ensure_ascii=False,indent=4)


if len(sys.argv) != 1:
    parser = argparse.ArgumentParser(description='Make users\' valid information.')
    parser.add_argument('-input_file', nargs=1, type=str, default="20.txt")
    parser.add_argument('-output_file', nargs=1, type=str, default="result.txt")
    args = parser.parse_args()

    input_file = args.input_file[0]
    output_file = args.output_file[0]
else:
    input_file = '4.txt'
    output_file = 'result.txt'

validator = Validator([])

with tqdm(range(100), colour='blue', ncols=100) as progressbar:
    data = json.load(open(input_file, encoding='windows-1251'))
    progressbar.update(25)
    validator = Validator(data)
    progressbar.update(35)
    invalid,valid = validator.parse()
    progressbar.update(70)
    """
    print('')
    progressbar.update(90)
    """
    summary(invalid, output_file)
    save_in_json(valid, 'correct_data.txt')
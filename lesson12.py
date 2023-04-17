# Создайте класс студента.
# ○ Используя дескрипторы проверяйте ФИО на первую 
#   заглавную букву и наличие только букв.
# ○ Названия предметов должны загружаться из 
#   файла CSV при создании экземпляра.
#   Другие предметы в экземпляре недопустимы.
# ○ Для каждого предмета можно хранить оценки 
#   (от 2 до 5) и результаты тестов (от 0 до 100).
# ○ Также экземпляр должен сообщать средний балл по 
#   тестам для каждого предмета и по оценкам всех 
#   предметов вместе взятых.

import math
import csv

MIN_SCORE = 2
MAX_SCORE = 5
MIN_TEST_RESULT = 0
MAX_TEST_RESULT = 100

__all__ = [
    'Student'
]


class SNPDescriptor:
    """Проверяет ФИО на первую заглавную букву и наличие только букв."""

    def __init__(self, name):
        self.name = name

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, name):
        self.validate(name)
        setattr(instance, self.param_name, name)

    def validate(self, name):
        if not name.isalpha():
            raise TypeError(f'Фамилия, имя и отчество должны состоять только из букв')
        if self.name is not None and not name.istitle():
            raise ValueError(f'Фамилия, имя и отчество должны начинаться с заглавной буквы')


class Student:
    # валидация
    name = SNPDescriptor('')
    surname = SNPDescriptor('')
    patronymic = SNPDescriptor('')

    def __init__(self, surname: str, name: str, patronymic: str, age: int,
                 grade: int):

        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.age = age
        self.grade = grade

        self.subjects = []
        self.subject_scores = {}
        self.subject_tests = {}
        self.load_subjects()

    def __repr__(self):
        return (f'Студент: {self.surname} {self.name} {self.patronymic}\nВозраст {self.age}\nОценка {self.grade}')

    def load_subjects(self):
        with open('grade.csv', 'r', encoding='utf-8', newline='') as f_csv:
            csv_read = csv.reader(f_csv)
            for i, line in enumerate(csv_read):
                if i != 0:
                    self.subjects.append(line[1])

        for _subject in self.subjects:
            self.subject_scores[_subject] = []
            self.subject_tests[_subject] = []

    def check_subject(self, subject: str) -> bool:
        return True if subject in self.subjects else False

    @staticmethod
    def check_score(score: int) -> bool:
        return True if MIN_SCORE <= score <= MAX_SCORE else False

    @staticmethod
    def check_test(test: int) -> bool:
        return True if MIN_TEST_RESULT <= test <= MAX_TEST_RESULT else False

    def add_score(self, subject: str, score: int) -> None:
        if not self.check_subject(subject):
            raise ValueError(f'Неверное значение предмета: {subject}')
        if not self.check_score(score):
            raise ValueError(f'Неверное значение оценки: {score}')
        self.subject_scores[f'{subject}'].append(score)

    def add_test(self, subject: str, test: int) -> None:
        if not self.check_subject(subject):
            raise ValueError(f'Неверное значение предмета: {subject}')
        if not self.check_test(test):
            raise ValueError(f'Неверное значение оценки: {test}')
        self.subject_tests[f'{subject}'].append(test)

    def get_average_test(self, subject: str) -> int:
        """Функция возвращает средний балл по тестам для каждого предмета"""
        if not self.check_subject(subject):
            raise ValueError(f'Invalid name of the subject: {subject}')
        return math.ceil(sum(self.subject_tests[f'{subject}']) / len(
            self.subject_tests[f'{subject}']))

    def get_average_score(self) -> int:
        """Функция возвращает средний балл по оценкам для всех предметов"""
        sum_score = 0
        num_score = 0
        for subject in self.subjects:
            sum_score += sum(self.subject_scores[f'{subject}'])
            num_score += len(self.subject_scores[f'{subject}'])
        return math.ceil(sum_score / num_score)
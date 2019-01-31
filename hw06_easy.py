# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.

# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.
import sys
import math


class Triangle:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        try:
            self.x1 = int(x1)
            self.y1 = int(y1)
            self.x2 = int(x2)
            self.y2 = int(y2)
            self.x3 = int(x3)
            self.y3 = int(y3)
        except ValueError:
            print("Ошибка. Введите координаты в виде чисел.")
            sys.exit()
        self.ab = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.ac = math.sqrt((self.x3 - self.x1) ** 2 + (self.y3 - self.y1) ** 2)
        self.bc = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)

    # Square - Площадь
    def square(self):
        sq = 0.5 * abs((self.x1 - self.x3) * (self.y2 - self.y3) - (self.x2 - self.x3) * (self.y1 - self.y3))
        return sq

    # Heigh - Высота
    def heigh(self):
        return 2 * self.square() / self.ac

    # Perimeter - Периметр
    def perimeter(self):
        return self.ab + self.ac + self.bc

    def param(self, num):
        print('\nПараметры треугольника № {} с координатами ({}, {}), ({}, {}), ({}, {}):\
              '.format(num, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, ))
        print('Площадь  =', self.square())
        print('Периметр =', self.perimeter())
        print('Высота =', self.heigh())


triangle1 = Triangle(1, 1, 6, 7, 8, 4)
triangle2 = Triangle(-2, -2, -4, -5, -6, -3)
triangle3 = Triangle(0, 0, 8, 2, -2, 6)

triangle1.param(1)
triangle2.param(2)
triangle3.param(3)

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.


# Класс Трапеция
class Trapezium:
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            self.x1 = int(x1)
            self.y1 = int(y1)
            self.x2 = int(x2)
            self.y2 = int(y2)
            self.x3 = int(x3)
            self.y3 = int(y3)
            self.x4 = int(x4)
            self.y4 = int(y4)
        except ValueError:
            print("Ошибка. Введите координаты в виде чисел.")
            sys.exit()
        # Определяем длины сторон
        self.ab = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.bc = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)
        self.cd = math.sqrt((self.x4 - self.x3) ** 2 + (self.y4 - self.y3) ** 2)
        self.ad = math.sqrt((self.x4 - self.x1) ** 2 + (self.y4 - self.y1) ** 2)
        # Определяем диагонали
        self.ac = math.sqrt((self.x3 - self.x1) ** 2 + (self.y3 - self.y1) ** 2)
        self.bd = math.sqrt((self.x4 - self.x2) ** 2 + (self.y4 - self.y2) ** 2)
        # Определяем меньшее и большее основание
        if self.bc < self.ad:
            self.small_base = self.bc
            self.larger_base = self.ad
        else:
            self.small_base = self.ad
            self.larger_base = self.bc

    def heigh(self):
        a = self.small_base
        b = self.larger_base
        c = self.ab ** 2
        d = self.cd ** 2

        h = math.sqrt(c - 1/4 * ((c - d) / (b - a) + b - a) ** 2)
        return h

    def square(self):
        return ((self.small_base + self.larger_base) / 2) * self.heigh()

    def perimeter(self):
        return self.ab + self.bc + self.cd + self.ad

    def equal_part(self):
        if self.ac == self.bd:
            return "Да"
        else:
            return "Нет"

    def param(self, num):
        print('\nПараметры трапеции № {} с координатами ({}, {}), ({}, {}), ({}, {}), ({}, {}):\
              '.format(num, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4))
        print('Площадь  =', self.square())
        print('Периметр =', self.perimeter())
        print('Высота =', self.heigh())
        print('Длины сторон:\n'
              'Малое основание = {}\n'
              'Большее основание = {}\n'
              'Боковая сторона AB = {}\n'
              'Боковая сторона CD = {}'.format(self.small_base, self.larger_base, self.ab, self.cd))
        print('Признак равнобедренности = ', self.equal_part())


trapezium1 = Trapezium(1, 1, 5, 7, 8, 7, 10, 1)
trapezium2 = Trapezium(1, 1, 3, 7, 8, 7, 10, 1)

trapezium1.param(1)
trapezium2.param(2)

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;

class Trapezium:
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            self.x1 = int(x1)
            self.y1 = int(y1)
            self.x2 = int(x2)
            self.y2 = int(y2)
            self.x3 = int(x3)
            self.y3 = int(y3)
            self.x4 = int(x4)
            self.y4 = int(y4)
        except ValueError:
            print("Ошибка. Введите координаты в виде чисел.")
            sys.exit()
        # Определяем длины сторон
        self.ab = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.bc = math.sqrt((self.x3 - self.x2) ** 2 + (self.y3 - self.y2) ** 2)
        self.cd = math.sqrt((self.x4 - self.x3) ** 2 + (self.y4 - self.y3) ** 2)
        self.ad = math.sqrt((self.x4 - self.x1) ** 2 + (self.y4 - self.y1) ** 2)
        # Определяем диагонали
        self.ac = math.sqrt((self.x3 - self.x1) ** 2 + (self.y3 - self.y1) ** 2)
        self.bd = math.sqrt((self.x4 - self.x2) ** 2 + (self.y4 - self.y2) ** 2)
        # Определяем меньшее и большее основание
        if self.bc < self.ad:
            self.small_base = self.bc
            self.larger_base = self.ad
        else:
            self.small_base = self.ad
            self.larger_base = self.bc

    def heigh(self):
        a = self.small_base
        b = self.larger_base
        c = self.ab ** 2
        d = self.cd ** 2

        h = math.sqrt(c - 1/4 * ((c - d) / (b - a) + b - a) ** 2)
        return h

    def square(self):
        return ((self.small_base + self.larger_base) / 2) * self.heigh()

    def perimeter(self):
        return self.ab + self.bc + self.cd + self.ad

    def equal_part(self):
        if self.ac == self.bd:
            return "Да"
        else:
            return "Нет"

    def param(self, num):
        print('\nПараметры трапеции № {} с координатами ({}, {}), ({}, {}), ({}, {}), ({}, {}):\
              '.format(num, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4))
        print('Площадь  =', self.square())
        print('Периметр =', self.perimeter())
        print('Высота =', self.heigh())
        print('Длины сторон:\n'
              'Малое основание = {}\n'
              'Большее основание = {}\n'
              'Боковая сторона AB = {}\n'
              'Боковая сторона CD = {}'.format(self.small_base, self.larger_base, self.ab, self.cd))
        print('Признак равнобедренности = ', self.equal_part())


trapezium1 = Trapezium(1, 1, 5, 7, 8, 7, 10, 1)
trapezium2 = Trapezium(1, 1, 3, 7, 8, 7, 10, 1)

trapezium1.param(1)
trapezium2.param(2)
# вычисления: длины сторон, периметр, площадь.

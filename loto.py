'''
== Лото ==
Правила игры в лото.
Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.
Количество бочонков — 90 штук (с цифрами от 1 до 90).
Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------
В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 
Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.
Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.
Пример одного хода:
Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)
Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.
Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html
'''

import random


# Класс бочонка
class Barrel:
    # Задаем длину списка при создании бочонка (по умолчанию = 90)
    def __init__(self, length=90):
        self.lst = [x for x in range(1, length + 1)]
        self.number = '-'
        self.last_number = '-'

    # def delete_item(self):
    #     try:
    #         idx = random.randrange(0, len(self.lst))
    #         self.lst.pop(idx)
    #         return self.lst
    #     except ValueError:
    #         return "Список уже пуст. Не мучайте его."

    # Метод выбора нового бочонка. Возвращает "число" и удаляет его из мешочка с бочонками.
    def get_barrel(self):
        self.last_number = self.number
        try:
            idx = random.randrange(0, len(self.lst))  # Случайный выбор бочонка
            num = self.lst[idx]
            self.lst.pop(idx)
            self.number = num
            return num
        except ValueError:
            return "Список уже пуст. Не мучайте его."

    # Печатаем новый бочонок
    def print_new(self):
        print('Новый бочонок: {} (Предыдущий бочонок: {}. Осталось бочонков: {})'
              .format(self.get_barrel(), self.last_number, len(self.lst)))


# Класс карточки игрока
class Cart:
    # Задаем длину списка при создании карточки (по умолчанию = 90)
    def __init__(self, length=90):
        self.lst = [x for x in range(1, length + 1)]
        self.fifteen = []
        self.health = 15  # Длина списка билетов
        self._get_fifteen_items()
        self.original_line = [x for x in range(9)]
        self.lines = self._sort_random(self.original_line.copy())

    #
    def _my_func(self, x):
        return int(x)

    # Метод создания списка из случайных 15 элементов
    def _get_fifteen_items(self):
        try:
            five = []
            copy_list = self.lst.copy()
            for x in range(1, 4):
                for y in range(1, 6):
                    idx = random.randrange(0, len(copy_list))
                    five.append(copy_list[idx])
                    copy_list.pop(idx)
                five.sort()
                self.fifteen.append(five.copy())
                five.clear()
            return self.fifteen
        except ValueError:
            return "Список меньше чем вы думаете. Не мучайте его."

    # Метод рандомной сортировки для строки
    def _sort_random(self, lst):
        lines = []
        for x in range(3):
            for _ in range(10):
                x1 = random.randint(0, 8)
                x2 = random.randint(0, 8)
                if x1 != x2:
                    lst[x1], lst[x2] = lst[x2], lst[x1]
            lines.append(lst.copy())
        return lines

    # Метод проверки наличия цифры на карточке,
    # а также зачеркивания, если такой атрибут передан (delete)
    def cross_out(self, num, delete=False):
        try:
            for x in range(0, 3):
                for y in range(0, 5):
                    if num == self.fifteen[x][y]:
                        if delete:
                            self.health -= 1
                            self.fifteen[x][y] = ' -'
                            return True
                        return True
            return False
        except ValueError:
            pass
        return "Список меньше чем вы думаете. Не мучайте его."

    # Метод вывода принадлежности карточки игрока
    def _print_name_cart(self):
        print('---------- Ваша карточка ----------')

    # Метод вывода карточки игрока
    def print_cart(self):
        self._print_name_cart()
        # прогоняем на печать три строки карточки
        for x in range(3):
            line = ''
            y = 0
            for j, el in enumerate(self.lines[x]):
                if el == 5 or el == 6 or el == 7 or el == 8:
                    line += ''.rjust(2)
                else:
                    line += str(self.fifteen[x][y]).rjust(2)
                    y += 1
                if j < len(self.lines[x]) - 1:
                    line += ''.rjust(2)
            print(line)
        print('-----------------------------------')


# Класс карточки компьютера с уникальным методом
class CartComp(Cart):
    # Переоределяем метод вывода принадлежности карточки компьютера
    def _print_name_cart(self):
        print('------- Карточка компьютера--------')


# Класс запуска Игры
class Game:
    def __init__(self, human, comp):
        self.human = human
        self.comp = comp
        # self.barrel = barrel
        self.last_gamer = comp

    # Ход компьютера в отдельном методе
    def go_comp(self):
        # Если игрок не проиграл, то следующий ход за компьютером
        # Проверяем на наличие цифры в карточке
        if self.comp.cross_out(barrel.number, True):
            self.check_cart()
            print('Компьютер зачеркнул цифру. Следующий ход ваш.')
            self.print_game()
            if self.game_over():
                return True
            else:
                return False
        else:
            self.check_cart()
            print('Компьютер пропустил ход. Следующий ход ваш.')
            self.print_game()
            if self.game_over():
                return True
            else:
                return False

    # Ход компьютера в отдельном методе
    def _auto_go_human(self):
        # Автоход для проверки победителя игры
        # Проверяем на наличие цифры в карточке
        if self.human.cross_out(barrel.number, True):
            self.check_cart()
            print('Вы зачеркнули цифру. Следующий ход компьютера.')
            self.print_game()
            if self.game_over():
                return True
            else:
                return False
        else:
            self.check_cart()
            print('Вы пропустили ход. Следующий ход компьютера.')
            self.print_game()
            if self.game_over():
                return True
            else:
                return False

    # Проверка чужой карточки н наличие цифры из бочонка
    def check_cart(self):
        # Проверяем и зачеркиваем при наличии цифры
        if self.last_gamer.cross_out(barrel.number, True):
            pass
        # Переопределяем предыдущего игрока
        if self.last_gamer == self.comp:
            self.last_gamer = self.human
        else:
            self.last_gamer = self.comp

    def game_over(self):
        if self.human.health == 0:
            print('Вы победили!')
            return True
        elif self.comp.health == 0:
            print('Компьютер победил!')
            return True
        else:
            return False

    def print_game(self):
        print('\nУ вас осталось {} цифр в билете. У компьютера осталось {} цифр в билете'
              .format(self.human.health, self.comp.health))
        barrel.print_new()
        self.human.print_cart()
        self.comp.print_cart()

    def start(self):
        self.print_game()
        while True:
            try:
                key = input('Зачеркнуть цифру? (y/n). Выход (q) ')
                if key == 'y':
                    if self.human.cross_out(barrel.number, True):
                        self.check_cart()
                        self.print_game()
                        if self.game_over():
                            break
                        if self.go_comp():
                            break
                    else:
                        print("Игра окончена. Вы прогирали!")
                        break
                elif key == 'n':
                    if self.human.cross_out(barrel.number):
                        print("Игра окончена. Вы прогирали!")
                        break
                    else:
                        self.check_cart()
                        self.print_game()
                        if self.game_over():
                            break
                        if self.go_comp():
                            break
                elif key == 'q':
                    print("Досрочное завершеие игры")
                    break
                else:
                    print('Сделай выбор тряпка!')
            except Exception as cls:
                print('Ошибка: ', cls)

    # Метод для проверки окончания игры в атоматическом режиме
    def auto_start(self):
        self.print_game()
        while True:
            if self._auto_go_human():
                break
            if self.go_comp():
                break


# Определяем экземпляры классов
barrel = Barrel()
my_cart = Cart()
cart_comp = CartComp()
game = Game(my_cart, cart_comp)

# Запускаем игру
while True:
    try:
        mode = int(input('В каком режиме запустить игру?\n'
                         '[1] - ручной режим\n'
                         '[2] - автоматический режим\n'
                         '[3] - выход\n'
                         '-->> '))
        if mode == 1:
            game.start()  # Запуск в ручном режиме
            break
        elif mode == 2:
            game.auto_start()  # Запуск в автоматическом режиме
            break
        elif mode == 3:
            break
        else:
            print('Неизвестный выбор')
    except ValueError:
        print('Введите именно число')

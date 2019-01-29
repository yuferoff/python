import os
import hw05_easy as hw5e

# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

def menu():
    x = -1
    while x < 0 or 4 < x:
        print("1 - перейти в папку.")
        print("2 - просмотреть содержимое текущей папки.")
        print("3 - удалить папку.")
        print("4 - создать папку.")
        print("0 - завершить работу.")
        try:
            x = int(input(": "))
        except ValueError:
            x = -1
    return x

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py

choice = -1
while choice != 0:
    choice = menu()
    if choice == 0:
        exit(0)
    elif choice == 2:
        print('\n'.join(hw5e.folder_contents(os.curdir))+'\n')
    else:
        folder_name = input("Введите имя каталога: ")
        bad_end = "нечто"
        try:
            if choice == 3:
                bad_end = "удалить."
                hw5e.rmfolder(os.curdir, folder_name)
                print("Успешно удалено.\n")
            elif choice == 4:
                bad_end = "создать."
                hw5e.mkfolder(os.curdir, folder_name)
                print("Успешно создано.\n")
            elif choice == 1:
                bad_end = "перейти."
                hw5e.chfolder(os.curdir, folder_name)
                print("Успешно перешёл.\n")
        except OSError as ose:
            print("Невозможно {}: {}".format(bad_end, ose))

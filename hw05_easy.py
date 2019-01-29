import shutil
import os
import sys
import os.path

# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

def make_dirs ():
    quantity_dirs = range(1,10)
    for i in quantity_dirs:
        i= str(i)
        try:
           os.makedirs('dir_'+i)
        except FileExistsError:
            print('dir_{} - уже существует'.format(i))

def remove_dirs ():
    quantity_dirs = range(1, 10)
    for i in quantity_dirs:
        i = str(i)
        try:
            os.removedirs('dir_'+i)
        except FileNotFoundError:
            print('dir_{} - папки не существует'.format(i))
make_dirs()
remove_dirs()

# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.

for i in os.listdir('.'):
    if os.path.isdir(i):
        print(i)
        
    
# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.

file_name = __file__.split('/')[-1:][0]

newfile = file_name + '.copy'
shutil.copy(file_name, newfile)
print('Файл {} был успешно создан.'.format(newfile))

###

def rmfolder(path, folder):
    os.rmdir(os.path.join(path, folder))


def mkfolder(path, folder):
    os.mkdir(os.path.join(path, folder))


def folder_contents(folder):
    arr = ['<.>', '<..>']
    arr.extend(sorted(list(map(lambda x: "<" + x + ">" if os.path.isdir(x) else x,
                               os.listdir(folder)))))
    return arr


def chfolder(path, folder):
    os.chdir(os.path.join(path, folder))

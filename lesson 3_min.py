import os

# task 2
# Написати скрипт який виведе список файлів та директорій поточній директорії
list_dir = os.listdir()
print(list_dir)

# task 3
# Написати скрипт який виведе список файлів та директорій за заданим шляхом
patch = r'C:\Program Files' # input the
list_dir = os.listdir(patch)
print(list_dir)


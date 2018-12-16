import re

# #Написати програму яка запитує у користувача ім'я та отримавши повну
# відповідь вітається з користувачем використовуючи його ім'я.
# Приклад відповіді: “my name is Taras” або “Taras is my name”

raw_data = ['my name is Taras', 'Taras is my name', 'tGGG']

for i in range(len(raw_data)):
    rez = re.search(r"\b[A-Z]{1}[a-z]*", raw_data[i])
    if rez != None:
        print(rez.group(), 'in sample # ', i)


# Написати програму яка запитує у користувача його email адресу, та
# перевіряє чи це коректна адреса. Тобто чи задана стрічка відповідає
# вимогам електронної адреси.


raw_data = ['ttt.@', 'Taras_r111@name.com', 'Taras@name.com.ua', 'ghw2m.hi1t.678f', 'ge?\/@fg.=n/b.n@']

for i in range(len(raw_data)):
    rez = re.search(r"(([\w_.]+)@([a-z1-9._]+))", raw_data[i])
    if rez != None:
        print('E-mail is ', rez.group())

# Написати програму яка запитує у користувача телефонний номер та
# перевіряє чи заданий формат є вірним. Формат: (xxx) xxx - xxxx

raw_data = ['(xxx) xxx - xxxx', '(024) 587 - 5878', '5(670)-ght-55', '(234) 654 - 5677']

for i in range(len(raw_data)):
    rez = re.search(r"[(]([0-9]{3})[)]( )([0-9]{3})( )-( )([0-9]{4})", raw_data[i])
    if rez != None:
        print('Correct phone number is ', rez.group())

# Написати програму яка у заданому файлі знаходить тег <title> та виводить
# # текст що знаходиться в ньому

with open('test_for_lesson5.txt', 'r', encoding='utf-8') as f:
    site_data = f.read()
    start = re.search(r"<title>", site_data).end()
    end = re.search(r"</title>", site_data).start()
    print(site_data[start:end])
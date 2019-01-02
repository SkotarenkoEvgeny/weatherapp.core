import time

# 1 Реалізувати декоратор, який сповільнює виконання функції на 1 сек

def one_sec_decor(funk):
    def wrapper():
        print('sleep 1 sec')
        time.sleep(1)
        print('wake up')
        return funk()
    return wrapper

@one_sec_decor
def funk():
    print("I'm here")

funk()

def some_sec_decorator(funk):
    sec = int(input('Input some sec, whitch you will wait '))
    def wrapper(*args, **kwargs):
        print('sleep {} sec'.format(sec))
        time.sleep(sec)
        print('wake up')
        return funk
    return wrapper

@some_sec_decorator
def funk_2():
    print('This is task 2')

funk_2()

# 3 Реалізувати декоратор який вимірює час виконання функції

def timer(funk):
    def wrapper():
        start_time = time.clock()
        print('Start timer')
        funk()
        rez = time.clock() - start_time
        print('Time working funktion is', rez)
    return wrapper

@timer
@some_sec_decorator
def funk_3():
    print('This is task 3')
funk_3()

# 4 Реалізувати декоратор який виводить усі аргументи отримані функцією перед
#  тим як вона буде виконана.

def args_counter(funk):
    def wrapper(*args):
        for i in args:
            print(i)
        return funk(*args)
    return wrapper

@args_counter
def f(*args):
    sum = 0
    for i in args:
        sum += i
    return sum

fr = f(2, 3, 4)
print(fr)
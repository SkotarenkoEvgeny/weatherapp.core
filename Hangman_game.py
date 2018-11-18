import random

'''
Написати Hangman гру. Ця гра полягає в тому, що потрібно відгадати слово яке
программа загадала (вибрала з якогось набору слів) Є 6 спроб.
Наприклад (FACTORY):
>>> Welcome to Hangman!
>>> Guess your letter: S
Incorrect!
>>> Guess your letter: F
F _ _ _ _ _ _
>>> Guess your letter: Y
F _ _ _ _ _ Y
'''

list_of_guessed_words = ['FACTORY', 'REFINERY', 'CAPITAL']
guessed_word = list_of_guessed_words[random.randint(0, len(list_of_guessed_words) - 1)]
number_of_letters = len(guessed_word)
attempt = 6
hiden_word = ['_' for i in range(len(guessed_word))]
print('Welcome to Hangman!')
print('The guessable word have {} letters. You have 6 attempts'.format(number_of_letters))
while attempt > 0 and number_of_letters > 0:
    question = input('If you know, that is a word, input him now. If you dont know, press "enter" ')
    flag = False
    if question == guessed_word:
        number_of_letters == 0
        break
    else:
        letter = input('Guess your letter: ').upper()
        for i in range(len(guessed_word)):
            if letter == guessed_word[i]:
                hiden_word[i] = letter
                number_of_letters -= 1
                flag = True
    if flag == False:
        print('Incorrect!')
    attempt -= 1
    print(' '.join(hiden_word))
if attempt == 0 and number_of_letters > 0:
    print('You lose!')
else:
    print('You win!')

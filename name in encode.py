#printing name in encode

#name = input('Input your name ')
name = 'http://rp5.ua/РџРѕРіРѕРґР°_РІ_СЃРІС–С‚С–'
name_encode = name.encode('utf-8')
print('Unicode\n')
print('Encode', name_encode, "\n")
print('Decode', name_encode.decode('utf-8'))

'''
Написати програму для перетворення імені користувача у unicode code points
Наприклад: Тарас → '422430440430441'
'''

print('hexadecimal\n')
print(''.join(format(ord(x), 'x') for x in name), "\n")


'''
Написати програму для перетворення імені користувача в бінарне представлення.
Наприклад:
Тарас → '1000010001010000110000100010000001000011000010001000001'
'''

print('binary\n')
print(''.join(format(ord(x), 'b') for x in name), "\n")
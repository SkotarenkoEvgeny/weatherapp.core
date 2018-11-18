#printing name in encode

name = input('Input your name ')
name_encode = name.encode('utf-8')
print(name_encode)
print(name_encode.decode(encoding='utf-8'))
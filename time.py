""" import datetime

a = datetime.datetime(2020, 5, 17)
x = datetime.datetime.now()

distance = (x - a)
print(distance)
print(round(distance.seconds/3600, 2), "hours")

 """

a_binary_string = "01101000 01110100 01110100 01110000 01110011 00111010 00101111 00101111 01111001 01101111 01110101 01110100 01110101 00101110 01100010 01100101 00101111 01100100 01010001 01110111 00110100 01110111 00111001 01010111 01100111 01011000 01100011 01010001"


binary_values = a_binary_string.split()

ascii_string = ""

for binary_value in binary_values:

    an_integer = int(binary_value, 2)
    ascii_character = chr(an_integer)
    ascii_string += ascii_character

print(ascii_string)

num = 100000
num = str(num)
print(f"{num:,}")


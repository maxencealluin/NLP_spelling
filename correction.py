import sys
import re
import unidecode

def replace_mult(word, target, replacement):
    for char in target:
        word = word.replace(char, replacement)
    return word
    
def soundex(word):
    word = str.upper(word)
    word = replace_mult(word, '-\\', '')
    word = replace_mult(word, "0123456789", "")
    word = unidecode.unidecode(word)
    first = word[0]
    code = ''.join(c for c in word[1:] if c not in "AEIOUYHW")
    code = replace_mult(code, "BP", "1")
    code = replace_mult(code, "CKQ", "2")
    code = replace_mult(code, "DT", "3")
    code = replace_mult(code, "L", "4")
    code = replace_mult(code, "MN", "5")
    code = replace_mult(code, "R", "6")
    code = replace_mult(code, "GJ", "7")
    code = replace_mult(code, "SXZ", "8")
    code = replace_mult(code, "FV", "9")
    code =  first + code
    code = re.sub(r'(\d)\1+', r'\1', code)
    return code

if len(sys.argv) <= 1:
    print("Veuillez passer une phrase en argument.")
    exit()

dictionary = {}
with open("dict-u8.txt", 'r') as file:
    for row in file:
        try:
            dictionary[soundex(row)[:-1]].append(row[:-1])
        except KeyError:
            dictionary[soundex(row)[:-1]] = [row[:-1]]
        # print(soundex(row), end ='')

# print(dictionary)

for word in str.split(sys.argv[1]):
    print(soundex(word))
    print(dictionary[soundex(word)])

# print(data)
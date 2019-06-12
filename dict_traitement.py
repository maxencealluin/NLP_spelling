from lxml import etree
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')

words = set()
tree = etree.parse("dict-u8.xml")
for entry in tree.xpath("/dico/entry/inflected/form"):
	if ' ' not in entry.text: #and entry.text not in words:
		words.add(str.lower(entry.text))
		# print(i)
words = sorted(words, key = locale.strxfrm)

with open("dict-u8.txt", 'w') as file:
	for word in words:
		file.write(word)
		file.write("\n")
	file.close()

# print(data)

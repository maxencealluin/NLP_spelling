import sys
import re
import unidecode

def replace_mult(word, target, replacement):
	for char in target:
		word = word.replace(char, replacement)
	return word

def replace_prefix(word, target, replacement):
	if word[:len(target)] == target:
		return word.replace(target, replacement, 1)
	else:
		return word

def preprocess(word):
	word = str.upper(word)
	word = replace_mult(word, ' -\\', '')
	word = replace_mult(word, "0123456789\n", "")
	word = unidecode.unidecode(word)
	return word

#Transforms words into a phonetic code
def soundex(word):
	word = preprocess(word)
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


#Soundex2, not used by default because results seem less consistent than soundex 1
def soundex2(word):
	word = preprocess(word)
	code = word
	code = code.replace("GUI", "KI")
	code = code.replace("GUE", "KE")
	code = code.replace("GA", "KA")
	code = code.replace("GO", "KO")
	code = code.replace("GU", "K")
	code = code.replace("CA", "KA")
	code = code.replace("CO", "KO")
	code = code.replace("CU", "KU")
	code = code.replace("Q", "K")
	code = code.replace("CCP", "K")
	code = code.replace("CK", "K")
	code = code.replace("CK", "K")
	if code[0] != 'A':
		code = replace_mult(code, "EIOU", "A")
	code = replace_prefix(code, "MAC", "MCC")
	code = replace_prefix(code, "ASA", "AZA")
	code = replace_prefix(code, "KN", "NN")
	code = replace_prefix(code, "PF", "FF")
	code = replace_prefix(code, "SCH", "SSS")
	code = replace_prefix(code, "PH", "FF")
	i = 0
	while i < len(code):
		if code[i] == 'H':
			if i == 0 or (i > 0 and code[i - 1] != 'C' and code[i - 1] != 'S'):
				code = code[:i] + code[i:].replace('H', '', 1)
				i = -1
		i += 1
	i = 0
	while i < len(code):
		if code[i] == 'Y':
			if i == 0 or (i > 0 and code[i - 1] != 'A'):
				code = code[:i] + code[i:].replace('Y', '', 1)
				i = -1
		i += 1
	if len(code) == 0:
		return '0000'
	if code[-1] in "ATDS":
		code = code[:-1]
	if len(code) > 1:
		code = code[0] + code[1:].replace('A', '')
	code = re.sub(r'(\d)\1+', r'\1', code)
	return code[:4].ljust(4, '0')

#custom comparison to favor accents
def compare_chars(c1, c2):
	if c1 in "aàâä" and c2 in "aàâä":
		return 0.5
	elif c1 in "çc" and c2 in "çc":
		return 0.5
	elif c1 in "eéèëê" and c2 in "eéèëê":
		return 0.5
	elif c1 in "oóòôö" and c2 in "oóòôö":
		return 0.5
	elif c1 in "uúùûü" and c2 in "uúùûü":
		return 0.5
	else:
		return 1

# Calculating edit distance between two words
def levenshtein(word1, word2):
	matrix = []
	n = len(word1)
	m = len(word2)
	matrix.append([i for i in range(n + 1)])
	for i in range(1, (m + 1)):
		matrix.append([0] * (n + 1))
		matrix[i][0] = i
	for j in range(1, m + 1):
		for i in range(1, n + 1):
			if word1[i - 1] != word2[j - 1]:
				cost = compare_chars(word1[i - 1], word2[j - 1])
			else:
				cost = 0
			matrix[j][i] = min(matrix[j - 1][i] + 1,
								matrix[j][i - 1] + 1,
								matrix[j - 1][i - 1] + cost)
	dist = 0
	return int(matrix[m][n] * 10)

# levenshtein(sys.argv[1], sys.argv[2])
# print(levenshtein(r"déçu", "decu"))
# print(levenshtein("decu", "docu"))
# print(soundex("mange"))
# print(soundex("manje"))
#
# print(soundex("pomme"))
# print(soundex("popmme"))

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print("Veuillez passer une phrase en argument.")
		exit()

	#Building soudex dictionary
	dictionary = {}
	with open("dict-u8.txt", 'r') as file:
		for row in file:
			try:
				dictionary[soundex(row)].append(row[:-1])
			except KeyError:
				dictionary[soundex(row)] = [row[:-1]]

	#Splitting sentence and matching with corresponding soundex in dictionary
	sentence = replace_mult(sys.argv[1], ",.;:/\'", ' ')
	results = []
	for word in str.split(sentence):
		code = soundex(word)
		try:
			if word not in dictionary[code]:
				dists = {}
				minimum = levenshtein(word, dictionary[code][0])
				for dict_word in dictionary[code]:
					try:
						dists[str(levenshtein(word, dict_word))].append(dict_word)
					except:
						dists[str(levenshtein(word, dict_word))] = [dict_word]
				min_key = min(int(nb) for nb in dists.keys())
				out = dists[str(min_key)]
				if len(out) == 1:
					results.append(out[0])
				else:
					results.append(out)
			else:
				results.append(word)
		except:
			results.append(word)

	#If multiple results for one word, matches the one with higher frequency
	for j, words in enumerate(results):
		if isinstance(words, list):
			print(words)
			max_freq = 0
			idx = 0
			for i, word in enumerate(words):
				with open("frequency_tables.txt", 'r') as file:
					for line in file:
						split = line.replace('\n', '').split('\t')
						if split[1] == word:
							if int(split[0]) > max_freq:
								max_freq = int(split[0])
								idx = i
							break
			results[j] = words[idx]

	print(results)

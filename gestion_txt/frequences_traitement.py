import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')

# Traite le fichier tableFrequencesWikipedia en supprimant les entrees invalides
# Et enregistre le tout dans un nouveau fichier pour traitement par l'algorithme de correction

with open("../tableFrequencesWikipediaFR2008-06-18.txt", 'rb') as r_file:
	with open("../frequency_tables.txt", 'w') as w_file:
		for line in r_file:
			try:
				split = line.decode('ISO-8859-1').split('\t')
				if any(c in "0123456789!_~þ:,)(?<>#·;»«[]$%&^{}°.\'\"+-*/=\\" for c in split[1]):
					continue
				if len(split[1]) <= 1:
					continue
				if split[0] == '6':
					break;
				w_file.write(split[0] + "\t" + split[1])
			except:
				print("fail")

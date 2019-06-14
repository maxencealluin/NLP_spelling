# NLP_spelling

Prototype de correction de fautes réalisé en python3.

Algorithme: 
* En cas d'entrée d'un mot non existant dans le dictionnaire, tranformation du mot par l'algorithme phonetique SOUNDEX
* Identification de la liste de mots partageant le meme code phonétique.
* Les mots partageant le même code phonétique sont ensuite classés selon la distance de Damerau–Levenshtein.
* Si il reste plusieurs mots candidats, le mot le plus fréquent est retenu.

## Usage:<br/>
`python correction.py <phrase> [-v]`

Le resultat est renvoyé sous forme de liste de mots.
L'option -v permets de montrer la liste de mots final dans le cas où il reste plusieurs candidats à la dernière étape

from modules.word_select import wordSelect
from modules.letter_link import letterLink

words = wordSelect()

grid,directionsdown,directionsacross = letterLink(words)

print("\n\n",grid)
print(directionsdown)
print(directionsacross)

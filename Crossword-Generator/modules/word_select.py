import csv
import random


def word_select(difficulty):
    words = []
    lines = []
    with open('wordsSorted.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            if row[2] == difficulty:
                lines.append(row)

    for i in range(10):
        x = random.randint(1, len(lines))
        y = [lines[x][0], lines[x][1]]
        words.append(y)

    return words

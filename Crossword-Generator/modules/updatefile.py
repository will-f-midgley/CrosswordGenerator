import csv


def stattrack(difficulty, timetaken, wordsanswered, lettersanswered):
    stats = []
    with open('scores.csv', newline='') as csvfile:
        reader = (csv.reader(csvfile.readlines()))
        for line in reader:
            stats.append(line)
        stats[0][1] = int(stats[0][1]) + int(timetaken)     #Total Time
        stats[2][1] = int(stats[2][1]) + wordsanswered      #Total Words
        stats[3][1] = int(stats[3][1]) + lettersanswered    #Total Letters
        stats[4][1] = int(stats[4][1]) + 1                  #Total Completions
        stats[4 + int(difficulty)][1] = int(stats[4 + int(difficulty)][1]) + 1  #Respective difficulty completions
        stats[1][1] = int(int(stats[0][1]) / int(stats[4][1]))                  #Average time
        if timetaken < int(stats[8 + int(difficulty)][1]) or int(stats[8 + int(difficulty)][1]) == -1:
            stats[8 + int(difficulty)][1] = int(timetaken)  #Respective difficulty fastest completion

    with open('scores.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in stats:
            writer.writerow(i)
        csvfile.close()

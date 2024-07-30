import csv


def first_time_setup():  # Setup stattrack values, unlocks, etc
    with open('scores.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Total Time", 0])
        writer.writerow(["Average Time", 0])
        writer.writerow(["Total Words", 0])
        writer.writerow(["Total Letters", 0])
        writer.writerow(["Total Crosswords", 0])
        writer.writerow(["Easy Completions", 0])
        writer.writerow(["Medium Completions", 0])
        writer.writerow(["Hard Completions", 0])
        writer.writerow(["Extreme Completions", 0])
        writer.writerow(["Fastest Easy", -1])
        writer.writerow(["Fastest Medium", -1])
        writer.writerow(["Fastest Hard", -1])
        writer.writerow(["Fastest Extreme", -1])
        csvfile.close()


def on_start():
    try:
        with open('scores.csv', 'r', newline='') as csvfile:
            pass
    except:
        first_time_setup()

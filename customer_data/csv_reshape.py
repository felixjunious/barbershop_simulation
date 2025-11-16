import csv

with open("names.csv", "r") as f:
    reader = csv.reader(f)
    row = next(reader)

with open("names_reshaped.csv", "w", newline="") as f:
    wrtr = csv.writer(f)
    for name in row:
        wrtr.writerow([name])
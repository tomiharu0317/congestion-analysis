import csv

def write_to_csv(key, value, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([key, value])

def retrieve_value_from_csv(key, filename):
    value = 0

    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == key:
                value = row[1]

    return value

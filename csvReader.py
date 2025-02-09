import csv
import sys

def read_csv_file(file):
    with open(file, newline='') as csv_file:
        line_reader = csv.reader(csv_file, delimiter=';', quotechar='|')

        for row in line_reader:
            print(', '.join(row))

if __name__ == "__main__":
    file_name = str(sys.argv[1])

    read_csv_file(file_name)
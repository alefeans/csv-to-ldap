import sys
import csv
import string
import random


def parse_csv(file):
    try:
        with open(file, 'r') as csv_file:
            for items in csv.DictReader(csv_file):
                yield items
    except Exception as e:
        print('ERROR - {}'.format(e))
        sys.exit()


def random_password():
        return ''.join(random.choice(string.ascii_letters) for m in range(12))

import sys
import csv
import string
import random


def parse_csv(file):
    """
    With the 'yield' statement, the size of the .csv
    doesn't matter because the objects will be 
    generated on demand.
    """
    try:
        with open(file, 'r') as csv_file:
            for items in csv.DictReader(csv_file):
                yield items
    except Exception as e:
        print('ERROR - {}'.format(e))
        sys.exit()


def random_password():
    """
    Returns a 12 characters randomic string.
    """
        return ''.join(random.choice(string.ascii_letters) for m in range(12))

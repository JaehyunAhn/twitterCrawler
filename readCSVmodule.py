# -*- coding: utf-8 -*-
import csv

def readCSVfile(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    for row in reader:
        print(row)

if __name__ == "__main__":
    print('hello csv')
    readCSVfile('사랑nouns.csv')
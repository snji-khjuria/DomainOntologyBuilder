import csv
def readProductTitlePatterns(titlePatternLocation):
    output = []
    file = open(titlePatternLocation, "r")
    reader = csv.reader(file, delimiter="\t")
    for line in reader:
        output.append((line[0], line[1], line[2]))

    return output[1:]


def readProductSpecsPatterns(specsPatternLocation):
    file = open(specsPatternLocation, "r")
    output = []
    reader = csv.reader(file, delimiter="\t")
    for line in reader:
        output.append((line[0], line[1], line[2], line[3]))
    return output[1:]


def readTablePatterns(tablePatterns):
    file = open(tablePatterns, "r")
    reader = csv.reader(file, delimiter="\t")
    output = []
    for line in reader:
        output.append((line[0], line[1], line[2], line[3]))
    return output[1:]

import Patterns

def readPatterns(patternLocation):
    titlePatternsLocation = patternLocation + "/titlePatterns.tsv"
    specsPatternLocation  = patternLocation + "/specsPatterns.tsv"
    tablePatternsLocation = patternLocation + "/tablePatterns.tsv"
    # print("Title patterns are:- ")
    titlePatterns = readProductTitlePatterns(titlePatternsLocation)
    # print("Specs patterns are:- ")
    specsPatterns = readProductSpecsPatterns(specsPatternLocation)
    # print("Table patterns location:- ")
    tablePatterns = readTablePatterns(tablePatternsLocation)
    return Patterns.Patterns(titlePatterns, specsPatterns, tablePatterns)
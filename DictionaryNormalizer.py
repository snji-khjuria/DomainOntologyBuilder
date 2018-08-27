import configparser


myConfigParser = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName    = "DictionaryNormalizer"


configSection = myConfigParser[sectionName]


attributesLocationConfig   = "attributesLocation"
attributesPageStatsConfig  = "attributesPageStatsLocation"
outputLocationConfig       = "dictNormalizationResults"
attributesLocation          = configSection[attributesLocationConfig]
attributesPageStatsLocation = configSection[attributesPageStatsConfig]
outputLocation = configSection[outputLocationConfig]


import os.path
def readAllFileNames(folderLocation):
    # print(folderLocation)
    # print(os.listdir(folderLocation))
    return [f for f in os.listdir(folderLocation) if os.path.isfile(folderLocation + "/" + f)]

def readFileContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        for line in file:
            line = line.strip()  # or some other preprocessing
            lines.append(line)  # storing everything in memory!
    return lines



def createAttributeDictionaries(attributes, fileLocation):
    d = {}
    for attribute in attributes:
        fullFileLocation = fileLocation + "/" + attribute
        d[attribute]     = readFileContentInList(fullFileLocation)
    return d

def findIntersection(a1, a2):
    lowera1 = a1.lower()
    lowera2 = a2.lower()
    if lowera1==lowera2:
        return True

    return True

def isSimilarAttributeByName(attributes):
    output = []
    for firstIndex in range(0, len(attributes)):
        firstAttribute = attributes[firstIndex]
        for secondIndex in range(firstIndex+1, len(attributes)):
            secondAttribute = attributes[secondIndex]
            status          = findIntersection(firstAttribute, secondAttribute)
            if status==True:
                output.append((firstAttribute, secondAttribute))
    return output

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getModifiedCommonSet(commonSet):
    output = []
    for item in commonSet:
        if not is_number(item):
            if not item.lower()=="yes" and not item.lower()=="no":
                output.append(item)
    return output

def checkIntersectionStatus(a1, a1Content, a2, a2Content):
    set1      = set(a1Content)
    set2      = set(a2Content)
    commonSet = set1 & set2
    commonSet = getModifiedCommonSet(commonSet)
    commonSetSize = len(commonSet)
    return commonSetSize>8

def findAttributeIntersection(attributes, myDictionary):
    output = []
    for index1 in range(0, len(attributes)):
        a1            = attributes[index1]
        a1Content     = myDictionary[a1]
        for index2 in range(index1+1, len(attributes)):
            a2        = attributes[index2]
            a2Content = myDictionary[a2]
            status    = checkIntersectionStatus(a1, a1Content, a2, a2Content)
            if status == True:
                output.append((a1, a2))
    return output



def getModifiedCommonSet2(commonSet):
    output = []
    for item in commonSet:
        if not item.lower()=="yes" and not item.lower()=="no":
            output.append(item)
    return output

def checkIntersectionStatusCorrelation(a1, a1Content, a1Stats, a2, a2Content, a2Stats):
    set1           = set(a1Content)
    set2           = set(a2Content)
    commonSet      = set1 & set2
    commonSet      = getModifiedCommonSet2(commonSet)
    commonSetSize  = len(commonSet)
    statsSet1      = set(a1Stats)
    statsSet2      = set(a2Stats)
    commonStatsSet = statsSet1 & statsSet2
    if (commonSetSize == len(set1) or commonSetSize == len(set2)) and len(commonStatsSet)==0 and (len(set1)>2 or len(set2)>2):
        return True
    return False

def findAttributeIntersectionCorrelation(attributes, contentDict, statsDict):
    output = []
    for index1 in range(0, len(attributes)):
        a1            = attributes[index1]
        a1Content     = contentDict[a1]
        a1Stats       = statsDict[a1]
        for index2 in range(index1+1, len(attributes)):
            a2        = attributes[index2]
            a2Content = contentDict[a2]
            a2Stats   = statsDict[a2]
            status    = checkIntersectionStatusCorrelation(a1, a1Content, a1Stats, a2, a2Content, a2Stats)
            if status == True:
                output.append((a1, a2))
    return output


def writeStrToFile(l, s):
    with open (l, "w") as f:
        f.write(s)


allAttributes              = readAllFileNames(attributesLocation)
attributeDictionaries      = createAttributeDictionaries(allAttributes, attributesLocation)
attributePagesDictionaries = createAttributeDictionaries(allAttributes, attributesPageStatsLocation)
print(allAttributes)
# print(attributeDictionaries)
matchedPairs = findAttributeIntersection(allAttributes, attributeDictionaries)
matchedPairsCorrelation = findAttributeIntersectionCorrelation(allAttributes, attributeDictionaries, attributePagesDictionaries)
print("Matched attributes are:- ")
# print(len(matchedPairs))
# for p in matchedPairs:
#     print(p)
print(len(matchedPairsCorrelation))
count = 1
output=""
for p in matchedPairsCorrelation:
    print(str(count) + " : " + str(p))
    output+=str(count) + " : " + str(p)  +"\n"
    count+=1
writeStrToFile(outputLocation, output)
print("Results written at location: " + outputLocation)
# output = []
# print("Tell us which one are correct(y/n):-")
# for p in matchedPairsCorrelation:
#     ans = input(str(p))
#     if ans=="y":
#         output.append(p)
#
# print("Final output is:- ")
# for p in output:
#     print(p)
# print(matchedPairs)
# print("Similar attributes are:- ")
# similarAttributesByName = isSimilarAttributeByName(allAttributes)
# print(similarAttributesByName)
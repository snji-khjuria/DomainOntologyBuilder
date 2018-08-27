import configparser


myConfigParser                   = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                      = "TrainTestDictionaryComparator"
trainSpecsLocationConfig         = "trainSpecsLocation"
trainTitlesLocationConfig        = "trainTitlesLocation"
testSpecsLocationConfig          = "testSpecsLocation"
testTitlesLocationConfig         = "testTitlesLocation"
extraContentLocationConfig       = "extraContentLocation"
attributesLocationConfig         = "attributesLocation"
configSection                    = myConfigParser[sectionName]
trainSpecsLocation               = configSection[trainSpecsLocationConfig]
trainTitlesLocation              = configSection[trainTitlesLocationConfig]
testSpecsLocation                = configSection[testSpecsLocationConfig]
testTitlesLocation               = configSection[testTitlesLocationConfig]
extraContentLocation             = configSection[extraContentLocationConfig]
attributesLocation               = configSection[attributesLocationConfig]

import re
def getLabelFromWords(label):
    return re.sub('_', ' ', label);


def readContentInList(fileLocation):
    output = []
    with open(fileLocation, "r") as f:
        for line in f:
            line = line.strip()
            if len(line)==0:
                output.append([])
            else:
                line      = line.split()
                output.append(line)
    return output

def getEndIndex(lines, index, attributeIndex, word, label):
    attributeName = getLabelFromWords(label[2:])
    startAttributeName = label[2:]
    totalLines = len(lines)
    attributeValue = word
    if index!=totalLines:
        while index<totalLines:
            line = lines[index]
            # print(line)
            if len(line)==0:
                break
            currentLabel = line[attributeIndex]
            if currentLabel=="O":
                break
            currentLabel =currentLabel[2:]
            if startAttributeName!=currentLabel:
                break
            attributeValue+=" " + line[0]
            index+=1
        index-=1
    return (index, attributeName, attributeValue)

def getAttributesDictionary(lines, attributeIndex):
    index=0
    totalLines = len(lines)
    attributesDict = {}
    while index<totalLines:
        line = lines[index]
        # print(line)
        if len(line)>0:
            label = line[attributeIndex]
            word  = line[0]
            if label!="O":
                index+=1
                (endIndex, attributeName, attributeValue) = getEndIndex(lines, index, attributeIndex, word, label)
                index=endIndex
                if not attributeName in attributesDict:
                    bufferSet = set([])
                else:
                    bufferSet = attributesDict[attributeName]
                bufferSet.add(attributeValue)
                attributesDict[attributeName] = bufferSet
        index+=1
    return attributesDict

def combineDict(d1, d2):
    for (k, v) in d2.items():
        if k in d1:
            d1[k] = d1[k].union(v)
        else:
            d1[k] = v
    return d1

def getExtraContent(testDict, trainDict):
    output = {}
    for (k, v) in testDict.items():
        if not k in trainDict:
            output[k] = v
        else:
            diff = v.difference(trainDict[k])
            if len(diff)>0:
                output[k] = diff
    return output

# testTitlesContent  = readContentInList(testTitlesLocation)
# testTitlesDict  = getAttributesDictionary(testTitlesContent, 3)
# print(testTitlesDict)


def convertSetToStr(s):
    output = ""
    for item in s:
        output+=item+"\n"
    return output

def writeStrToLocation(l, s):
    with open(l, "w") as f:
        f.write(s)


import os.path
def readAllFileNames(folderLocation):
    # print(folderLocation)
    # print(os.listdir(folderLocation))
    return [f for f in os.listdir(folderLocation) if os.path.isfile(folderLocation + "/" + f)]


def readFileContentInListAsSet(fileLocation):
    lines = []
    with open(fileLocation) as file:
        for line in file:
            line = line.strip()  # or some other preprocessing
            lines.append(line)  # storing everything in memory!
    return list(set(lines))



def readAllAttributesDictionary(attributeLocation):
    allAttributesLocation = readAllFileNames(attributeLocation)
    attributesDict = {}
    for attribute in allAttributesLocation:
        attributeFileLocation = attributeLocation + "/" + attribute
        dictContent = readFileContentInListAsSet(attributeFileLocation)
        if len(dictContent)>0:
            attributesDict[attribute] = dictContent
    return attributesDict

trainSpecsContent  = readContentInList(trainSpecsLocation)
trainTitlesContent = readContentInList(trainTitlesLocation)
testSpecsContent   = readContentInList(testSpecsLocation)
testTitlesContent  = readContentInList(testTitlesLocation)
trainSpecsDict = getAttributesDictionary(trainSpecsContent, 2)
trainTitlesDict = getAttributesDictionary(trainTitlesContent, 2)
testSpecsDict   = getAttributesDictionary(testSpecsContent, 3)
testTitlesDict  = getAttributesDictionary(testTitlesContent, 3)
trainDict = combineDict(trainSpecsDict, trainTitlesDict)
testDict  = combineDict(testSpecsDict, testTitlesDict)
completeAttributes = readAllAttributesDictionary(attributesLocation)
extraDictContent = getExtraContent(testDict, trainDict)
completeExtraDictContent = getExtraContent(testDict, completeAttributes)
for (k, v) in completeExtraDictContent.items():
    print("Key:" + str(k))
    print("Value:- " + str(v))

# for (k, v) in trainDict.items():
#     print("Key:" + str(k))
#     print("Value:- " + str(v))
#
# for (k, v) in trainDict.items():
#     print("Key:" + str(k))
#     print("Value:- " + str(v))
output = ""
for (k, v) in extraDictContent.items():
    l = extraContentLocation+"/"+k
    s = convertSetToStr(v)
    output+=k+"\n======================================\n"
    output+=s+"\n-------------------------------------------\n\n"
    writeStrToLocation(l, s)
writeStrToLocation(extraContentLocation+"/completeExtraInfo", output)
print("Written everything")
        # print("TrainSpecs dictionary:-")
# print(trainSpecsDict)
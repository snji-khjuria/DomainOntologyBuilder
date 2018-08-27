import configparser


myConfigParser                   = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                      = "MyAdvancedTagger"

configSection                    = myConfigParser[sectionName]


attributesLocationConfig                = "attributesLocation"
taggedCrfTrainDataLocationConfig        = "taggedCrfTrainDataLocation"
taggedCrfTestDataLocationConfig         = "taggedCrfTestDataLocation"
advancedTaggerTrainOutputLocationConfig = "advancedTaggerTrainOutputLocation"
advancedTaggerTestOutputLocationConfig  = "advancedTaggerTestOutputLocation"


attributesLocation         = configSection[attributesLocationConfig]
taggedCrfTrainDataLocation = configSection[taggedCrfTrainDataLocationConfig]
taggedCrfTestDataLocation  = configSection[taggedCrfTestDataLocationConfig]
advancedTaggedTrainOutputLocation = configSection[advancedTaggerTrainOutputLocationConfig]
advancedTaggedTestOutputLocation  = configSection[advancedTaggerTestOutputLocationConfig]
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


coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"

from stanfordcorenlp import StanfordCoreNLP
nlpEngine = StanfordCoreNLP(coreNLPLocation)

def getNlpWords(s):
    return s
    # words = nlpEngine.word_tokenize(s)
    # output = ""
    # for w in words:
    #     output+=w+" "
    # return output.strip()

def representNum(element):
    try:
        float(element)
        return True
    except ValueError:
        return False
def is_int_or_float(a):
    if type(a) is int or type(a) is float:
        return True
    else:
       return False
# def representsInt(s):
#     try:
#         int(s)
#         return True
#     except ValueError:
#         return False

def readNlpParsedDictionary(fileLocation):
    output = readFileContentInListAsSet(fileLocation)
    result = []
    for item in output:
        if representNum(item) or item.lower()=="yes" or item.lower()=="no":
            continue
        result.append(getNlpWords(item))
    return result

def readAllAttributesDictionary(attributeLocation):
    allAttributesLocation = readAllFileNames(attributeLocation)
    attributesDict = {}
    for attribute in allAttributesLocation:
        attributeFileLocation = attributeLocation + "/" + attribute
        dictContent = readNlpParsedDictionary(attributeFileLocation)
        if len(dictContent)>0:
            attributesDict[attribute] = dictContent
    return attributesDict

#read (sentence, weakSupervision) list.
#now you need to create strong supervision there
#hope to see good results on that part.
import csv
def readCrfData(fileLocation):
    output = []
    with open(fileLocation, "r") as csvfile:
        reader          = csv.reader(csvfile, delimiter="\t")
        line            = ""
        weakSupervision = ""
        for row in reader:
            if len(row)==0:
                output.append((line.strip(), weakSupervision.strip()))
                line            = ""
                weakSupervision = ""
                continue
            word = row[0]
            weak = row[2]
            line            += " " + word
            weakSupervision += " " + weak
    return output

#get all indices for substring in a string
def allindices(string, sub):
    string = string.lower()
    sub    = sub.lower()
    listindex = []
    offset    = 0
    i = 0
    i = string.find(sub)
    while i >= 0:
        # print(i)
        while i>=0 and True:
            j = i-1
            jj = False
            if j<0 or string[j]==' ' or string[j]=='(':
                jj = True
            k = i + len(sub)
            kk=False
            if k==len(string) or string[k] ==' ' or string[k]==')' or string[k]==',':
                kk=True
            if jj==True and kk==True:
                break
            i = string.find(sub, i + len(sub))
            # if i == -1:
            #     break
        if i>=0:
            listindex.append((i, i + len(sub)))
            i = string.find(sub, i + len(sub))
    return listindex

#get all indices for attribute dictionary
def getAllIndicesForDict(string, l):
    positions = []
    for item in l:
        pos = allindices(string, item)
        if len(pos)>0:
            positions.extend(pos)
    return positions


def getPositionsForDictionary(string, d):
    resultingPositions = {}
    for (attribute, values) in d.items():
        positions = getAllIndicesForDict(string, values)
        if len(positions)>0:
            resultingPositions[attribute] = positions
    return resultingPositions


import re
def getLabelFromWords(label):
    return re.sub(' ', '_', label);

def doTaggingForSentence(sentence, d, myLocalTagsSentence):
    words     = sentence.split()
    localTags = myLocalTagsSentence.split()
    startPos  = 0
    endPos    = 0
    content   = []
    index=0
    for word in words:
        endPos           += len(word)-1
        relevantPositions =  set([])
        myLocalTag        = localTags[index]
        content.append((word, startPos, endPos, relevantPositions, myLocalTag))
        startPos  = endPos+2
        endPos    = startPos
        index+=1
    positionsDict = getPositionsForDictionary(sentence, d)
    for (attributeName, positions) in positionsDict.items():
        for p in positions:
            (s, e) = p
            attributeLabel = getLabelFromWords(attributeName)
            for c in content:
                (word, startPos, endPos, relevantPositions, myLocalTag) = c
                if startPos>=s and endPos<=e:
                    relevantPositions.add(attributeLabel)

    return content
    # print(content)

def getGlobalDictStr(globalDict):
    output=""
    for item in globalDict:
        output+="/"+item
    if len(output)==0:
        return "O"
    return output[1:]

def getOutputString(mySentenceResult):
    output = ""
    for wordContent in mySentenceResult:
        (word, startPos, endPos, globalDict, localDict) = wordContent
        globalDictStr = getGlobalDictStr(globalDict)
        output+=word+"\t"+globalDictStr+"\t"+localDict+"\n"
    return output+"\n"

def writeStrToFileLocation(output, outputLocation):
    with open(outputLocation, "w") as f:
        f.write(output)

crfData = readCrfData(taggedCrfTrainDataLocation)
crfTestData = readCrfData(taggedCrfTestDataLocation)
attributesDict = readAllAttributesDictionary(attributesLocation)

def processContent(crfData, attributeDict):
    count=1
    output = ""
    totalCount = len(crfData)
    for item in crfData:
        (sentence, myLocalTags) = item
        # print("Item is:- ")
        # print(item)
        # print("=======================================")
        outputPerSentence = doTaggingForSentence(sentence, attributesDict, myLocalTags)
        outputPerSentence = getOutputString(outputPerSentence)
        output+=outputPerSentence
        count+=1
        if count%10==0:
            print(str(count) + " processed out of " + str(totalCount))
    return output
# print("Output is")
# print(output)
print("Processing training Data:- ")
trainOutput = processContent(crfData, attributesDict)
print("Processing test data:- ")
testOutput  = processContent(crfTestData, attributesDict)
writeStrToFileLocation(trainOutput, advancedTaggedTrainOutputLocation)
writeStrToFileLocation(testOutput, advancedTaggedTestOutputLocation)
print("Train data written at:- " + advancedTaggedTrainOutputLocation)
print("Test data written at:- " + advancedTaggedTestOutputLocation)
# print("Attributes Dictionary")
# print("=================================================")
# for item in attributesDict.items():
#     (k, v) = item
#     print("Attribute key is:- "   + k)
#     print("Attribute value is:- " + str(v))
#
# print("=================================================")
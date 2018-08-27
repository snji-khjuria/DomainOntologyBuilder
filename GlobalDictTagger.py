import configparser


myConfigParser                   = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                      = "GlobalDictTagger"

configSection                    = myConfigParser[sectionName]


attributesLocationConfig                = "attributesLocation"
corpusContentLocationConfig             = "localTaggedDataOutputLocation"
outputLocationConfig                    = "globalTaggedContentLocation"



attributesLocation                      = configSection[attributesLocationConfig]
corpusContentLocation                   = configSection[corpusContentLocationConfig]
outputLocation                          = configSection[outputLocationConfig]


titlesLocation                          = corpusContentLocation + "/taggedTitle"
parasLocation                           = corpusContentLocation + "/taggedPara"
titlesOutputLocation                    = outputLocation  + "/globallyTaggedTitles"
parasOutputLocation                     = outputLocation  + "/globallyTaggedParas"
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


def readFileContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        for line in file:
            line = line.strip()  # or some other preprocessing
            lines.append(line)  # storing everything in memory!
    return lines

def getSentenceAndLocalTags(line):
    words = line.strip().split()
    sentence  = ""
    localTags = ""
    for word in words:
        rIndex = word.rfind("/")
        sentence+=" " + word[:rIndex]
        localTags+=" " + word[rIndex+1:]
    return (sentence.strip(), localTags.strip())

def readTaggedContent(fileLocation):
    lines = readFileContentInList(fileLocation)
    count=0
    output = []
    for line in lines:
        (sentence, localTags) = getSentenceAndLocalTags(line)
        # print("Sentence:- ")
        # print(sentence)
        # print("LocalTgs:- ")
        # print(localTags)
        count+=1
        output.append((sentence, localTags))
        # if count>20:
        #     break
    return output
coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"

from stanfordcorenlp import StanfordCoreNLP
nlpEngine = StanfordCoreNLP(coreNLPLocation)




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


def getNlpWords(s):
    return s

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


import re
def getLabelFromWords(label):
    return re.sub(' ', '_', label);

def getPositionsForDictionary(string, d):
    resultingPositions = {}
    for (attribute, values) in d.items():
        positions = getAllIndicesForDict(string, values)
        if len(positions)>0:
            resultingPositions[attribute] = positions
    return resultingPositions


def modifyContent2(content):
    index = 1
    total = len(content)
    while True:
        if index>=total:
            break
        startIndex = index
        prevIndex  = startIndex-1
        startContent = content[startIndex]
        (word, se, ee, startTags, localTag) = startContent
        (prevWord, seP, eeP, prevTags, prevLocaTag) = content[prevIndex]
        if len(startTags)>1:
            intersection = (prevTags&startTags)
            if len(intersection)>0:
                content[startIndex] = (word, se, ee, intersection, localTag)
        index+=1
    return content



def printContent(content):
    contentStr = ""
    for item in content:
        contentStr += str(item) + "\n"
    return contentStr


def modifyContent(content):
    index=0
    total = len(content)
    while True:
        if index>=total:
            break
        startIndex = index
        endIndex   = startIndex+1
        startContent = content[startIndex]
        (word, se, ee, startTags, localTag) = startContent
        if len(startTags)>1:
            #find the location where the list is of 1 index
            while endIndex<total:
                item = content[endIndex]
                (word, s, e, pos, localItemTag)   = item
                if len(pos)<=1 or len (startTags & pos)==0:
                    break
                endIndex+=1
            endIndex-=1
            # print("for startIndex:- " + str(startIndex) + " ednIndex is " + str(endIndex))
            if startIndex!=endIndex:
                savedIndex=startIndex
                savedTag  = "O"
                for item in startTags:
                    for bufferIndex in range(startIndex+1, endIndex+1):
                        bufferContent = content[bufferIndex]
                        (w, se, ee, bufferTags, bufferLocalTags) = bufferContent
                        if item in bufferTags:
                            if bufferIndex>savedIndex:
                                savedIndex = bufferIndex
                                savedTag = item
                if savedIndex!=startIndex:
                    for bufferIndex in range(startIndex, endIndex+1):
                        bufferContent = content[bufferIndex]
                        (w, se, ee, bufferTags, bufferLocalTags) = bufferContent
                        bufferTags = set([savedTag])
                        content[bufferIndex] = (w, se, ee, bufferTags, bufferLocalTags)
        index+=1
    # print("COntent now is ")
    # print(printContent(content))
    return modifyContent2(content)

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
    # print("COntent is:- ")
    # print(printContent(content))
    return modifyContent(content)
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
    globalDictErrors = []
    prevTag = ""
    for wordContent in mySentenceResult:
        (word, startPos, endPos, globalDict, localDict) = wordContent
        globalDictStr = getGlobalDictStr(globalDict)
        if len(globalDict)>1:
            globalDictErrors.append((globalDict, word))
            tag = globalDictStr
        else:
            if globalDictStr!="O":
                if prevTag == globalDictStr:
                    tag = "I-" + globalDictStr
                else:
                    tag = "B-" + globalDictStr
            else:
                tag = globalDictStr
        prevTag = globalDictStr
        output += word + "\t" + tag + "\t" + localDict + "\n"
    return (output+"\n", globalDictErrors)


def processContent(crfData, attributesDict):
    count=1
    output = ""
    totalCount = len(crfData)
    globalDictError = []
    for item in crfData:
        (sentence, myLocalTags) = item
        # print("Item is:- ")
        # print(item)
        # print("=======================================")
        outputPerSentence = doTaggingForSentence(sentence, attributesDict, myLocalTags)
        (outputPerSentence, errors) = getOutputString(outputPerSentence)
        # print("OutputPerSentence:- ")
        # print(outputPerSentence)
        # globalDictError.extend(errors)
        if len(errors)>0:
            globalDictError.extend(errors)
            # print("OutputPerSentence:- ")
            # print(outputPerSentence)
        output+=outputPerSentence
        count+=1
        if count%10==0:
            print(str(count) + " processed out of " + str(totalCount))
    return (output, globalDictError)



def writeStrToFileLocation(output, outputLocation):
    with open(outputLocation, "w") as f:
        f.write(output)


def convertSetToString(s):
    output = ""
    for item in s:
        output+="\t" + item
    return output.strip()

def handleErrorsInformation(errors):
    conflictDictAnswer = {}
    output             = ""
    for item in errors:
        (conflicts, conflictingWord) = item
        conflictsStr                 = convertSetToString(conflicts)
        conflictWitWordString        = conflictsStr + "\t" + conflictingWord
        if conflictsStr in conflictDictAnswer:
            buffer = conflictDictAnswer[conflictsStr]
        else:
            buffer = 0
        conflictDictAnswer[conflictsStr] = buffer+1
        output +=   conflictWitWordString + "\n"
    distinctConflicts = ""
    conflictWithCountString = ""
    for (conflictKey, count) in conflictDictAnswer.items():
        distinctConflicts+=conflictKey+"\n"
        conflictWithCountString+=conflictKey+"\t"+str(count)+"\n"
    return (output, distinctConflicts, conflictWithCountString)

attributesDict = readAllAttributesDictionary(attributesLocation)
titlesContent  = readTaggedContent(titlesLocation)
parasContent   = readTaggedContent(parasLocation)
# titlesContent = parasContent
# parasContent   = readTaggedContent(parasLocation)
(titlesContent, titleErrors)  = processContent(titlesContent, attributesDict)
(parasContent, parasErrors)   = processContent(parasContent, attributesDict)
# print(titlesContent)
print("Title errors are:- ")
print(titleErrors)
print("Para errors are:- ")
print(parasErrors)
(titleConflictWithWord, titleConflictDistinct, titleConflictCount) = handleErrorsInformation(titleErrors)
(parasConflictWithWord, parasConflictDistinct, parasConflictCount) = handleErrorsInformation(parasErrors)
writeStrToFileLocation(titlesContent, titlesOutputLocation)
writeStrToFileLocation(parasContent, parasOutputLocation)
writeStrToFileLocation(titleConflictWithWord, outputLocation+"/titleConflictWord")
writeStrToFileLocation(titleConflictDistinct, outputLocation+"/titleConflictDistinct")
writeStrToFileLocation(titleConflictCount, outputLocation+"/titleConflictCount")
writeStrToFileLocation(parasConflictWithWord, outputLocation+"/parasConflictWord")
writeStrToFileLocation(parasConflictDistinct, outputLocation+"/parasConflictDistinct")
writeStrToFileLocation(parasConflictCount, outputLocation+"/parasConflictCount")
print("Written at location:- " + str(titlesOutputLocation))
print("Written at location:- " + str(parasOutputLocation))
# for item in titlesContent:
#     print(item)
# for (a, b) in attributesDict.items():
#     print(a)
#     print(b)
nlpEngine.close()
import configparser


myConfigParser = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName    = "LocalDictTagger"
testCorpusConfigLocation   = "testCorpusLocation"
attributesLocationConfig   = "attributesLocation"
attributesPageStatsConfig  = "attributesPageStatsLocation"
patternsLocationConfig     = "patternsLocation"



configSection = myConfigParser[sectionName]



attributesLocation          = configSection[attributesLocationConfig]
attributesPageStatsLocation = configSection[attributesPageStatsConfig]

from PatternsReaderUtil import readPatterns
from PatternMatcherUtil import getProdInfo
import os.path

patternsLocation          = configSection[patternsLocationConfig]

patterns                  = readPatterns(patternsLocation)

testCorpusLocation        = configSection[testCorpusConfigLocation]


def getRealWordsFromNlp(s):
    words = nlpEngine.word_tokenize(s)
    output = ""
    for w in words:
        output+=w+" "
    return output.strip()

def getWordsNlpTable(relations):
    output = []
    for (k, v) in relations:
        output.append((k, getRealWordsFromNlp(v)))
    return output

def getAllFilesInFolder(folderLocation):
    # print(folderLocation)
    # print(os.listdir(folderLocation))
    return [folderLocation + "/" + f for f in os.listdir(folderLocation) if os.path.isfile(folderLocation + "/" + f)]

allTestPages = getAllFilesInFolder(testCorpusLocation)
print("Pages are ")
print(allTestPages)
ontology = []
count=0
coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"
from stanfordcorenlp import StanfordCoreNLP
nlpEngine = StanfordCoreNLP(coreNLPLocation)


total = len(allTestPages)

def replaceMultipleWhiteSpaces(content):
    return " ".join(content.split())

def convertListToSentence(l):
    output = ""
    for item in l:
        output+=item+"\n\n"
    return output


def writeStrToLocation(location, s):
    with open(location, "w") as f:
        f.write(s)


def writeListsAsCsv(outputLocation, triples):
    with open(outputLocation, 'w') as f:
        for sublist in triples:
            for item in sublist:
                f.write(item + '\t')
            f.write('\n')



def createTriples(productTitles, productTable):
    output = []
    for productTitle in productTitles:
        for (k, v) in productTable:
            output.append([productTitle, k, v])
    return output


def makeDictionaries(totalRelations):
    fullDict = {}
    for (key, value) in totalRelations:
        if key in fullDict:
            prev = fullDict[key]
            prev.append(value)
            prev=list(set(prev))
            fullDict[key] = prev
        else:
            fullDict[key] = [value]
    return fullDict


def convertListToStr(l):
    output = ""
    for item in l:
        output+=item+"\n\n"
    return output

def writeDictValues(location, l):
    with open(location, 'w') as fp:
        for item in l:
            fp.write("%s\n" % item)

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


def getPositionsForDictionary(string, d):
    resultingPositions = {}
    for (attribute, value) in d:
        positions = allindices(string, value)
        if len(positions)>0:
            resultingPositions[attribute] = positions
    return resultingPositions

import re
def getLabelFromWords(label):
    return re.sub(' ', '_', label);

def getSentenceStr(l):
    result = ""
    prevTag = ""
    for (word, tag) in l:
        if tag!="O":
            if tag==prevTag:
                mytag="I-"+tag
            else:
                mytag = "B-"+tag
        else:
            mytag = "O"
        result+=" " + word+"/" + mytag
        prevTag = tag
    return result


def getSentencesFromContent(content):
    output = [[]]
    for (word, startPos, endPos, relevantPositions) in content:
        if len(relevantPositions)==0:
            relevantPositions.add("O")
        output2 = []
        for o in output:
            for foundAttribute in relevantPositions:
                buffer = list(o)
                buffer.append((word, foundAttribute))
                output2.append(buffer)
        output = output2
        # print("Output is ")
        # print(output)
    result = []
    # print("Outputs are:- ")
    # print(output)
    for item in output:
        result.append((getSentenceStr(item)))
    return result



def modifyContent2(content):
    index = 1
    total = len(content)
    while True:
        if index>=total:
            break
        startIndex = index
        prevIndex  = startIndex-1
        startContent = content[startIndex]
        (word, se, ee, startTags) = startContent
        (prevWord, seP, eeP, prevTags) = content[prevIndex]
        if len(startTags)>1:
            intersection = (prevTags&startTags)
            if len(intersection)>0:
                content[startIndex] = (word, se, ee, intersection)
        index+=1
    return content

def modifyContent(content):
    index=0
    total = len(content)
    while True:
        if index>=total:
            break
        startIndex = index
        endIndex   = startIndex+1
        startContent = content[startIndex]
        (word, se, ee, startTags) = startContent
        if len(startTags)>1:
            #find the location where the list is of 1 index
            while endIndex<total:
                item = content[endIndex]
                (word, s, e, pos)   = item
                if len(pos)<=1 and len (startTags & pos)==0:
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
                        (w, se, ee, bufferTags) = bufferContent
                        if item in bufferTags:
                            if bufferIndex>savedIndex:
                                savedIndex = bufferIndex
                                savedTag = item
                if savedIndex!=startIndex:
                    for bufferIndex in range(startIndex, endIndex+1):
                        bufferContent = content[bufferIndex]
                        (w, se, ee, bufferTags) = bufferContent
                        bufferTags = set([savedTag])
                        content[bufferIndex] = (w, se, ee, bufferTags)
        index+=1
    return content

def getConflictsFromContent(content):
    output = []
    for item in content:
        (w, se, ee, tags) = item
        if len(tags)>1:
            newTags = list(tags)
            newTags.append(w)
            output.append(newTags)
    return output

def doTaggingForSentence(sentence, d):
    words     = sentence.split()
    startPos  = 0
    endPos    = 0
    content   = []
    index=0
    for word in words:
        endPos           += len(word)-1
        relevantPositions =  set([])
        content.append((word, startPos, endPos, relevantPositions))
        startPos          = endPos+2
        endPos            = startPos
        index            += 1
    positionsDict = getPositionsForDictionary(sentence, d)
    for (attributeName, positions) in positionsDict.items():
        for p in positions:
            (s, e) = p
            attributeLabel = getLabelFromWords(attributeName)
            for c in content:
                (word, startPos, endPos, relevantPositions) = c
                if startPos>=s and endPos<=e:
                    relevantPositions.add(attributeLabel)
    # print("Content is:- ")
    # print(content)
    # print("content was:- ")
    # print(content)
    content   = modifyContent(content)
    conflicts = getConflictsFromContent(content)
    # print("content is:- ")
    # print(content)
    sentences = getSentencesFromContent(content)
    return (sentences, conflicts)
    # print(content)



def doSentenceTagging(sentence, table):
    return sentence

def getDictStats(totalRelationStats):
    fullDict = {}
    for (relations, page) in totalRelationStats:
        for (key, value) in relations:
            if key in fullDict:
                prev = fullDict[key]
                prev.append(page)
                prev=list(set(prev))
                fullDict[key] = prev
            else:
                fullDict[key] = [page]
    return fullDict

untaggedTitles = ""
untaggedParas  = ""
taggedParas    = ""
taggedTitles   = ""
ontology = []
totalRelations = []
totalRelationStats  = []
totalParaConflicts  = []
totalTitleConflicts = []
errorTitles = []
errorParas  = []
for testPage in allTestPages:
    count += 1
    if count % 1000 == 0:
        print("Processed:- " + str(count) + " out of " + str(total))
        # break
    prodInfo     = getProdInfo(patterns, testPage)
    productTitle = prodInfo.getProductTitle()
    untaggedTitle = ""
    if len(productTitle) > 0:
        untaggedTitle           = productTitle[0]
        untaggedTitle           = replaceMultipleWhiteSpaces(untaggedTitle)
        productTable            = prodInfo.getProductTable()
        for (k, v) in productTable:
            if v=="Videocon":
                print(k)
                print(productTitle)
                print(testPage)
                break

def getItemStr(item):
    output = ""
    for i in item:
        output+=i+"\t"
    return output.strip()
def convertllToStr(ll):
    resultText = ""
    output = []
    # print(ll)
    for (l, sentenceText) in ll:
        line = ""
        for item in l:
            itemS = getItemStr(item)
            line+=itemS+"\n"
        line = line.strip()
        output.append(line)
        resultText+=line+"\n"
        resultText+="=========================\n"
        resultText+="Sentence:- \n" + sentenceText
        resultText+="\n=======================\n"
    # output = list(set(output))
    result = ""
    for item in output:
        result+=item+"\n"
    return (result, resultText)

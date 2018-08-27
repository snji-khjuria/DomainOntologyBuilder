import configparser


myConfigParser = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName    = "LocalDictTagger"
testCorpusConfigLocation   = "testCorpusLocation"
attributesLocationConfig   = "attributesLocation"
attributesPageStatsConfig  = "attributesPageStatsLocation"
patternsLocationConfig     = "patternsLocation"
tfattributesLocationConfig = "tfAttributesLocation"


configSection = myConfigParser[sectionName]



attributesLocation          = configSection[attributesLocationConfig]
tfAttributesLocation        = configSection[tfattributesLocationConfig]
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
            (a, b, c) = sublist
            sublist = [a, b, c]
            for item in sublist:
                f.write(item + '\t')
            f.write('\n')



def createTriples(productTitles, productTable):
    output = []
    for productTitle in productTitles:
        for (k, v) in productTable:
            output.append((productTitle, k, v))
    return list(set(output))


def makeDictionaries(totalRelations):
    fullDict = {}
    tfFullDict = {}
    for (key, value) in totalRelations:
        if key in fullDict:
            prev = fullDict[key]
            prev.append(value)
            prev=list(set(prev))
            fullDict[key] = prev
            attribDict    = tfFullDict[key]
            if value in attribDict:
                buffer = attribDict[value]
            else:
                buffer=0
            attribDict[value] = buffer+1
            tfFullDict[key] = attribDict
        else:
            fullDict[key] = [value]
            bufferDict = {}
            bufferDict[value] = 1
            tfFullDict[key] = bufferDict
    tfFullDict2 = {}
    for (attributeName, attributeNameDict) in tfFullDict.items():
        output = []
        for (attributeNameValue, attributeValueCount) in attributeNameDict.items():
            output.append(str(attributeValueCount)+"\t"+attributeNameValue)
        tfFullDict2[attributeName]=output
    return (fullDict, tfFullDict2)


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
    if count % 100 == 0:
        print("Processed:- " + str(count) + " out of " + str(total))
        # break
    prodInfo     = getProdInfo(patterns, testPage)
    productTitle = prodInfo.getProductTitle()
    untaggedTitle = ""
    if len(productTitle) > 0:
        untaggedTitle           = productTitle[0]
        untaggedTitle           = replaceMultipleWhiteSpaces(untaggedTitle)
        productTable            = prodInfo.getProductTable()
        productPara             = convertListToSentence(prodInfo.getProductSpecs()).strip()
        productPara             = replaceMultipleWhiteSpaces(productPara)
        untaggedTitle           = getRealWordsFromNlp(untaggedTitle)
        productPara             = getRealWordsFromNlp(productPara)
        productTable            = getWordsNlpTable(productTable)
        # taggedPara              = doSentenceTagging(productPara, productTable).strip()
        # taggedTitle             = doSentenceTagging(untaggedTitle, productTable).strip()
        taggedPara = ""
        taggedTitle = ""
        (taggedParaList, paraConflicts)          = doTaggingForSentence(productPara, productTable)
        (taggedTitleList, titleConflicts)        = doTaggingForSentence(untaggedTitle, productTable)
        if len(taggedParaList)==1:
            taggedPara = taggedParaList[0]
        else:
            errorParas.extend(taggedParaList)
            totalParaConflicts.append((paraConflicts, productPara))
        if len(taggedTitleList)==1:
            taggedTitle = taggedTitleList[0]
        else:
            errorTitles.extend(taggedTitleList)
            totalTitleConflicts.append((titleConflicts, untaggedTitle))
        # print("Tagged para:- ")
        # print(taggedParaList)
        # print("Title")
        # print(untaggedTitle)
        # print("Tagged title:- ")
        # print(taggedTitleList)
        if len(untaggedTitle) > 0:
            untaggedTitles += untaggedTitle + "\n"
        if len(productPara) > 0:
            untaggedParas += productPara + "\n"
        if len(taggedPara) > 0:
            taggedParas += taggedPara + "\n"
        if len(taggedTitle) > 0:
            taggedTitles += taggedTitle + "\n"
        ontology.extend(createTriples(productTitle, productTable))
        totalRelations.extend(productTable)
        totalRelationStats.append((prodInfo.getProductTable(), count))

def getItemStr(item):
    output = ""
    for i in item:
        output+=i+"\t"
    return output.strip()

def getAllItemsExceptLastStr(item):
    output = ""
    total = len(item)
    for index in range(0, total-1):
        output+=item[index]+"\t"
    return output.strip()

def convertllToStr(ll):
    resultText = ""
    output = []
    conflictCountDict = {}
    noisyTrainingData  = []
    # print(ll)
    for (l, sentenceText) in ll:
        line = ""
        for item in l:
            itemS = getItemStr(item)
            line+=itemS+"\n"
            notLast = getAllItemsExceptLastStr(item)
            if notLast in conflictCountDict:
                count = conflictCountDict[notLast]
                conflictCountDict[notLast] = count+1
            else:
                conflictCountDict[notLast] = 1
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
    return (result, resultText, conflictCountDict)


def clubDictionaries(paraConflictDict, titleConflictDict):
    for (k, v) in titleConflictDict.items():
        if k in paraConflictDict:
            buffer = paraConflictDict[k]
        else:
            buffer = 0
        paraConflictDict[k] = buffer+v
    return paraConflictDict


def getDictStr(dictionary):
    output = ""
    for (k, v) in dictionary.items():
        output+=k+"\t" + str(v) + "\n"
    return output.strip()


taggedDataLocationConfig     = "taggedDataOutputLocation"
ontologyLocationConfig       = "ontologyOutputLocation"
taggedDataLocation           = configSection[taggedDataLocationConfig]
untaggedParaLocation         = taggedDataLocation + "/untaggedPara"
untaggedTitleLocation        = taggedDataLocation + "/untaggedTitle"
taggedParaLocation           = taggedDataLocation + "/taggedPara"
taggedTitleLocation          = taggedDataLocation + "/taggedTitle"
noisyTitleLocation           = taggedDataLocation + "/noisyTitles"
noisyParasLocation           = taggedDataLocation + "/noisyParas"
titleConflictsLocation                          = taggedDataLocation + "/titleConflicts"
paraConflictsLocation                           = taggedDataLocation + "/paraConflicts"
ontologyOutputLocation                          = configSection[ontologyLocationConfig]
(paraConflictsStr, pConflictSentence, paraConflictDict)        = convertllToStr(totalParaConflicts)
(titleConflictsStr, tConflictSentence, titleConflictDict)      = convertllToStr(totalTitleConflicts)
conflictsStr = paraConflictsStr + "\n" + titleConflictsStr
conflictSentence         = pConflictSentence + "\n" + tConflictSentence
conflictsStr = conflictsStr.strip()
conflictSentence = conflictSentence.strip()
conflictDict = clubDictionaries(paraConflictDict, titleConflictDict)
conflictDictStr = getDictStr(conflictDict)
writeStrToLocation(untaggedTitleLocation, untaggedTitles)
writeStrToLocation(taggedTitleLocation, taggedTitles)
writeStrToLocation(untaggedParaLocation, untaggedParas)
writeStrToLocation(taggedParaLocation, taggedParas)


ontology = list(set(ontology))
writeListsAsCsv(ontologyOutputLocation, ontology)
print("Ontology written at location:- "       +       ontologyOutputLocation)
print("Untagged Para present at:-     "       +       untaggedParaLocation)
print("UnTagged Title present at:-    "       +       untaggedTitleLocation)
print("Tagged Para present at:-       "       +       taggedParaLocation)
print("Tagged Title present at:-      "       +       taggedTitleLocation)


(fd, tfDict) = makeDictionaries(totalRelations)
for (attribute, values) in fd.items():
    writeDictValues(attributesLocation + "/" + attribute.replace("/", " "), values)
print("Dictionaries written at location:- " + attributesLocation)

for (attribute, values) in tfDict.items():
    writeDictValues(tfAttributesLocation + "/" + attribute.replace("/", " "), values)
print("Dictionaries written at location:- " + attributesLocation)


dictStats = getDictStats(totalRelationStats)
for (attribute, values) in dictStats.items():
    writeDictValues(attributesPageStatsLocation + "/" + attribute.replace("/", " "), values)
print("Written dict stats")
print(type(errorTitles))
print(len(errorTitles))
if len(conflictsStr)>0:
    writeStrToLocation(taggedDataLocation+"/conflictsListWithWord", conflictsStr)
    writeStrToLocation(taggedDataLocation+"/conflictsSentence", conflictSentence)
    writeStrToLocation(taggedDataLocation+"/conlictingDict", conflictDictStr)
if len(errorParas)>0:
    errorParasStr = convertListToSentence(errorParas)
    writeStrToLocation(noisyParasLocation, errorParasStr)
if len(errorTitles)>0:
    errorTitlesStr = convertListToSentence(errorTitles)
    writeStrToLocation(noisyTitleLocation, errorTitlesStr)

print("Everything Processing done.")
nlpEngine.close()
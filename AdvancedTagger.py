import configparser


myConfigParser                = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                   = "AdvancedTagger"

configSection                 = myConfigParser[sectionName]

attributesLocationConfig   = "attributesLocation"
taggedTitlesLocationConfig = "taggedTitlesLocation"
taggedParasLocationConfig  = "taggedParasLocation"


attributesLocation         = configSection[attributesLocationConfig]
taggedTitlesLocation       = configSection[taggedTitlesLocationConfig]
taggedParasLocation        = configSection[taggedParasLocationConfig]

#read dictionaries
#filter values
#start tagging
#whenever there is string successful tagging do the sequence labeling answer

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

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"

from stanfordcorenlp import StanfordCoreNLP
nlpEngine = StanfordCoreNLP(coreNLPLocation)
def getWordsNLp(s):
    words = nlpEngine.word_tokenize(s)
    output = ""
    for w in words:
        output+=w+" "
    return output.strip()



def getWordsNlpList(values):
    return values
    # return [getWordsNLp(w) for w in values]


def createAttributeDictionaries(attributes, fileLocation):
    d = {}
    for attribute in attributes:
        fullFileLocation = fileLocation + "/" + attribute
        d[attribute]     = readFileContentInList(fullFileLocation)
    return d

def filterValues(values):
    output = []
    for item in values:
        i = item.lower()
        # print("is is " + i)
        if i=="yes" or i=="no" or representsInt(i):
            continue
        output.append(item)
    return getWordsNlpList(output)

def filterDictionaries(attributeDictionaries):
    output = {}
    for (attribute, values) in attributeDictionaries.items():
        print("Filtering :- " + attribute)
        values = filterValues(values)
        if len(values)>0:
            output[attribute] = values
    return output

def makeKVRelations(attributesDict):
    output = []
    for (k, values) in attributesDict.items():
        for v in values:
            output.append((k, v))
    return output


import re
def getLabelFromWords(label):
    return re.sub(' ', '_', label);



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



def doTagging2(sentence, relations):
    for (attribute, v) in relations:
        attribute = attribute.replace("/", " ")
        attribute = getLabelFromWords(attribute)
        pos       = allindices(sentence, v)
        if len(pos) == 0:
            # v = getWordsNLp(v)
            pos = allindices(sentence, v)

        offset    = 0
        attribLength = len(attribute) + 3

        # [(m.start(), m.start()+len(value)) for m in re.finditer(value, sentence)]
        # for (s, e) in pos:
        #     print("Index:- " + str(s) + " " + str(e))
        #     print(sentence[s:e])
        for (s, e) in pos:
            # print("Attribute is:- " + str(attribLength))
            s+=offset
            e+=offset
            sentence = sentence[:s] + "[" + sentence[s:e] + "/" + attribute.upper() + "]" + sentence[e:]
            # print(sentence)
            offset+=attribLength
            # print("Offset is " + str(offset))
    return sentence

def doAdvancedTagging(content, relations):
    output = ""
    while True:
        untaggedLocation = content.find("[")
        if untaggedLocation==-1:
            break
        untaggedContent = content[:untaggedLocation]
        content         = content[untaggedLocation:]
        untaggedContent = doTagging2(untaggedContent, relations)
        output+=untaggedContent
        taggedLocation  = content.find("]", untaggedLocation)
        if taggedLocation==-1:
            break
        output+=content[:taggedLocation+1]
        if taggedLocation+1==len(content):
            content = ""
        else:
            content = content[taggedLocation+1:]
    output+=doTagging2(content, relations)
    return output.strip()

allAttributes              = readAllFileNames(attributesLocation)
attributeDictionaries      = filterDictionaries(createAttributeDictionaries(allAttributes, attributesLocation))
taggedTitles               = readFileContentInList(taggedTitlesLocation)
taggedParas                = readFileContentInList(taggedParasLocation)
# for (k, v) in attributeDictionaries.items():
#     print("Key:- " + k)
#     print("Value:- " + str(v))

tableRelations = makeKVRelations(attributeDictionaries)
outputTitles = []
outputParas  = []
count=0
for title in taggedTitles:
    outputTitle = doAdvancedTagging(title, tableRelations)
    outputTitles.append(outputTitle)
    count+=1
    # if count%10==0:
    #     break
    if title != outputTitle:
        print("Input:-" + title)
        print("Output:- " + outputTitle)
# for para in taggedParas:
#     outputPara = doAdvancedTagging(para, tableRelations)
#     outputParas.append(outputPara)
# print("Tagged paras:- ")
# print(taggedParas)
# print("Tagged titles:- ")
# print(taggedTitles)
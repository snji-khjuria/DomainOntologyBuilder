import configparser


myConfigParser = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName    = "OntologyMaker"


configSection = myConfigParser[sectionName]
testCorpusConfigLocation   = "testCorpus"
ontologyLocationConfig     = "ontologyOutputLocation"
pageClubbedLocationConfig  = "pageClubbedContentLocation"
patternsLocationConfig     = "patternsLocation"


testCorpusLocation        = configSection[testCorpusConfigLocation]
ontologyOutputLocation    = configSection[ontologyLocationConfig]
clubbedPageOutputLocation = configSection[pageClubbedLocationConfig]
patternsLocation          = configSection[patternsLocationConfig]
untaggedParaLocation      = clubbedPageOutputLocation + "/untaggedPara"
untaggedTitleLocation    = clubbedPageOutputLocation + "/untaggedTitle"
taggedParaLocation        = clubbedPageOutputLocation + "/taggedPara"
taggedTitleLocation      = clubbedPageOutputLocation + "/taggedTitle"

from PatternsReaderUtil import readPatterns
from PatternMatcherUtil import getProdInfo
import os.path


def createTriples(productTitles, productTable):
    output = []
    for productTitle in productTitles:
        for (k, v) in productTable:
            output.append([productTitle, k, v])
    return output


def getAllFilesInFolder(folderLocation):
    # print(folderLocation)
    # print(os.listdir(folderLocation))
    return [folderLocation + "/" + f for f in os.listdir(folderLocation) if os.path.isfile(folderLocation + "/" + f)]

patterns = readPatterns(patternsLocation)
# Patterns.Patterns.printProductTitlePatterns(patterns)
# Patterns.Patterns.printProductSpecsPatterns(patterns)
# Patterns.Patterns.printProductRelationPatterns(patterns)
allTestPages = getAllFilesInFolder(testCorpusLocation)
print("Pages are ")
print(allTestPages)


ontology = []
count=0
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


coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"
# from stanfordcorenlp import StanfordCoreNLP
# nlpEngine = StanfordCoreNLP(coreNLPLocation)
def getWordsNLp(s):
    return s
    # words = nlpEngine.word_tokenize(s)
    # output = ""
    # for w in words:
    #     output+=w+" "
    # return output.strip()



def writeStrToLocation(location, s):
    with open(location, "w") as f:
        f.write(s)

def getWordsNlpTable(relations):
    output = []
    for (k, v) in relations:
        output.append((k, getWordsNLp(v)))
    return output


def writeListsAsCsv(outputLocation, triples):
    with open(outputLocation, 'w') as f:
        for sublist in triples:
            for item in sublist:
                f.write(item + '\t')
            f.write('\n')

def improveData(content):
    return " ".join(content.split())

def convertListToSentence(l):
    output = ""
    for item in l:
        output+=item+" "
    return output
untaggedTitles = ""
untaggedParas  = ""
taggedTitles   = ""
taggedParas    = ""
total  = len(allTestPages)
for testPage in allTestPages:
    count+=1
    status = False
    if count%100==0:
        print("Processed:- " + str(count) + " out of " + str(total))
    # if count > 10:
    #     break
    prodInfo     = getProdInfo(patterns, testPage)
    productTitle = prodInfo.getProductTitle()
    untaggedTitle = ""
    if len(productTitle)>0:
        untaggedTitle = productTitle[0]
    # untaggedTitle = improveData(untaggedTitle)
    untaggedTitle = improveData(untaggedTitle)
    productTable = prodInfo.getProductTable()
    productPara = convertListToSentence(prodInfo.getProductSpecs()).strip()
    productPara = improveData(productPara)
    untaggedTitle = getWordsNLp(untaggedTitle)
    productPara = getWordsNLp(productPara)
    productTable = getWordsNlpTable(productTable)
    taggedPara = doTagging2(productPara, productTable).strip()
    taggedTitle = doTagging2(untaggedTitle, productTable).strip()
    if len(productTitle) > 0:
        untaggedTitles += untaggedTitle + "\n"
    if len(productPara) > 0:
        untaggedParas += productPara + "\n"
    if len(taggedPara) > 0:
        taggedParas += taggedPara + "\n"
    if len(taggedTitle) > 0:
        taggedTitles += taggedTitle + "\n"
    # for (k, v) in productTable:
    #     if v=="Videocon":
    #         print("Key is:- " + k)
    #         print("Page is:- " + testPage)
    ontology.extend(createTriples(productTitle, productTable))


writeStrToLocation(untaggedTitleLocation, untaggedTitles)
writeStrToLocation(taggedTitleLocation, taggedTitles)
writeStrToLocation(untaggedParaLocation, untaggedParas)
writeStrToLocation(taggedParaLocation, taggedParas)

writeListsAsCsv(ontologyOutputLocation, ontology)
print("Ontology written at location:- "       + ontologyOutputLocation)
print("Untagged Para present at:-     "       + untaggedParaLocation)
print("UnTagged Title present at:-    "       + untaggedTitleLocation)
print("Tagged Para present at:-       "       + taggedParaLocation)
print("Tagged Title present at:-      "       + taggedTitleLocation)
# nlpEngine.close()


import configparser

myConfigParser = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName    = "DictionaryMakerFromPatterns"

patternsLocationConfig     = "patternsLocation"
testCorpusConfig           = "testCorpus"
attributesLocationConfig   = "attributesLocation"
attributesPageStatsConfig  = "attributesPageStatsLocation"



configSection = myConfigParser[sectionName]


patternsInputLocation       = configSection[patternsLocationConfig]
testCorpusLocation          = configSection[testCorpusConfig]
attributesLocation          = configSection[attributesLocationConfig]
attributesPageStatsLocation = configSection[attributesPageStatsConfig]

import os.path
def getAllFilesInFolder(folderLocation):
    # print(folderLocation)
    # print(os.listdir(folderLocation))
    return [folderLocation + "/" + f for f in os.listdir(folderLocation) if os.path.isfile(folderLocation + "/" + f)]

def writeDictValues(location, l):
    with open(location, 'w') as fp:
        for item in l:
            fp.write("%s\n" % item)

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

from PatternsReaderUtil import readPatterns
from PatternMatcherUtil import getProdInfo

patterns     = readPatterns(patternsInputLocation)
allTestPages = getAllFilesInFolder(testCorpusLocation)
print("Pages are ")
print(allTestPages)
count              = 0
totalRelations     = []
totalRelationStats = []

totalPages = len(allTestPages)
for testPage in allTestPages:
    print("test page is ")
    print(testPage)
    prodInfo = getProdInfo(patterns, testPage)
    # print("ProductTitles are:- ")
    # print(prodInfo.getProductTitle())
    # print("Product Specs are:- ")
    # print(prodInfo.getProductSpecs())
    # print("Product relations:- ")
    # print(prodInfo.getProductTable())
    # print("Patterns read")
    count+=1
    if count%10==0:
        print("count:- " + str(count) + " processed out of " + str(totalPages))
    # print("Product table is :- ")
    #print(prodInfo.getProductTable())
    totalRelations.extend(prodInfo.getProductTable())
    totalRelationStats.append((prodInfo.getProductTable(), count))

print("Processed everythinf=g")

fd = makeDictionaries(totalRelations)
for (attribute, values) in fd.items():
    writeDictValues(attributesLocation + "/" + attribute.replace("/", " "), values)
print("Dictionaries written at location:- " + attributesLocation)

dictStats = getDictStats(totalRelationStats)
for (attribute, values) in dictStats.items():
    writeDictValues(attributesPageStatsLocation + "/" + attribute.replace("/", " "), values)
print("Written dict stats")
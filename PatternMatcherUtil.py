from FileUtil import readPlainHtmlPageContent

# from MatchersUtil import getAllEntitiesInsideLeftRightPattern, getAllRelations, getClusterInsideLeftRightPattern, getElementsOfCluster
from RegexMatcherUtil import getAllEntitiesInsideLeftRightPattern, getAllRelations, getClusterInsideLeftRightPattern, getElementsOfCluster

def extractProductTitle(pageContent, numPageContent, titlePattern):
    (leftTitlePattern, rightTitlePattern, patternType) = titlePattern
    if patternType == "NUM":
        pageContent = numPageContent
    return getAllEntitiesInsideLeftRightPattern(pageContent, leftTitlePattern, rightTitlePattern)


def extractProductTitles(pageContent, numPageContent, titlePatterns):
    output = []
    for titlePattern in titlePatterns:
        output.extend(extractProductTitle(pageContent, numPageContent, titlePattern))
    return output


def extractProductSpec(pageContent, numPageContent, productSpecsPattern):
    (leftSpecsPattern, insideSpecsPattern, rightSpecsPattern, patternType) = productSpecsPattern
    if patternType == "NUM":
        pageContent = numPageContent
    found = getClusterInsideLeftRightPattern(pageContent, leftSpecsPattern, insideSpecsPattern, rightSpecsPattern)
    totalFound = []
    for cluster in found:
        clusterItems = getElementsOfCluster(cluster, insideSpecsPattern)
        totalFound.extend(clusterItems)
    totalFound = set(totalFound)
    return list(totalFound)
    # return getClusterInsideLeftRightPattern(pageContent, leftSpecsPattern, insideSpecsPattern, rightSpecsPattern)

def extractProductSpecs(pageContent, numPageContent, productSpecsPatterns):
    output = []
    for pattern in productSpecsPatterns:
        output.extend(extractProductSpec(pageContent, numPageContent, pattern))
    return output


def extractProductRelation(pageContent, numPageContent, productRelationPattern):
    (leftTablePattern, middleTablePattern, rightTablePattern, patternType) = productRelationPattern
    if patternType=="NUM":
        pageContent = numPageContent
    # print("Going to find the pattern results")
    found = getAllRelations(leftTablePattern, middleTablePattern, rightTablePattern, pageContent)
    return found

def extractProductRelations(pageContent, numPageContent, productRelationPatterns):
    output = []
    for pattern in productRelationPatterns:
        output.extend(extractProductRelation(pageContent, numPageContent, pattern))
    return output

from StringUtil import replaceNumWordsInStr
from ProductInfo import ProductInfo
def getProdInfo(patterns, pageLocation):
    pageContent        = readPlainHtmlPageContent(pageLocation)
    numProcessedPageContent = replaceNumWordsInStr(pageContent)
    titlePatterns      = patterns.getProductTitlePatterns()
    specsPatterns      = patterns.getProductSpecsPatterns()
    relationPatterns   = patterns.getProductRelationPatterns()
    productTitles      = extractProductTitles(pageContent, numProcessedPageContent, titlePatterns)
    productSpecs       = extractProductSpecs(pageContent, numProcessedPageContent, specsPatterns)
    productRelations   = extractProductRelations(pageContent, numProcessedPageContent, relationPatterns)
    return ProductInfo(pageLocation, productTitles, productSpecs, productRelations)
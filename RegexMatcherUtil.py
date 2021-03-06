import re
def removeRegExpStar(s):
    old = re.compile("\*")
    new = "STAR"
    return re.sub(old, new, s)
def getRegExpStarBack(s):
    old = re.compile("STAR")
    new = ".*?"
    return re.sub(old, new, s)

def getAllPatternLocations(pattern, s):
    regexp = re.compile("(?=" + pattern + ")")
    output = []
    for m in regexp.finditer(s):
        startPos = m.start()
        sObj = re.search(pattern, s[startPos:])
        endPos   = startPos + sObj.end()
        output.append((startPos, endPos))
    return output


from bs4 import BeautifulSoup

def isHtmlString(item):
    return bool(BeautifulSoup(item, "html.parser").find())

#########################################################
###############Entity extraction code####################

#find entity set in left and right pattern.
def getAllEntitiesInsideLeftRightPattern(pageContent, leftPattern, rightPattern, threshold=1000):
    output = []
    leftPattern  = getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    rightPattern = getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        rpLoc = re.search(rightPattern, pageContent[endL:])
        if not rpLoc is None:
            element = pageContent[endL:endL+rpLoc.start()]
            if len(element)<=threshold:
                output.append(element.strip())
    return list(set(output))
###############Entity extraction code ends here##############
#############################################################

def getAllRelations(leftPattern, middlePattern, rightPattern, pageContent, key_threshold=1000, value_threshold=1000):
    searchIndex = 0
    output = []
    mp = middlePattern
    rp = rightPattern
    leftPattern   =  getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    middlePattern =  getRegExpStarBack(re.escape(removeRegExpStar(middlePattern)))
    rightPattern  =  getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        mLoc = re.search(middlePattern, pageContent[endL:])
        if not mLoc is None:
            startM = endL + mLoc.start()
            endM   = endL + mLoc.end()
            key    = pageContent[endL:startM].strip()
            # print("Key is ")
            # print(key)
            # print(rp)
            # print(pageContent[endM:endM+300])
            rLoc = re.search(rightPattern, pageContent[endM:])
            if not rLoc is None:
                startR = endM + rLoc.start()
                # endR   = endM + rLoc.end()
                value  = pageContent[endM:startR].strip()
                if len(key) <= key_threshold and len(value) <= value_threshold and not isHtmlString(key+value):
                    output.append((key, value))
    return list(set(output))

from bs4 import BeautifulSoup
#return ''.join(BeautifulSoup(htmlTxt).findAll(text=True))
# from bs4 import BeautifulSoup
#
# soup = BeautifulSoup(html)
# text = soup.get_text()
# print(text)

def withoutHtml(s):
    return ''.join(BeautifulSoup(s).findAll(text=True)).encode('utf-8').strip()

def isClusterOnlyHtmlUnderLengthThrehold(cluster, threshold):
    cluster = cluster.strip()
    if len(cluster)>threshold:
        return False
    if withoutHtml(cluster)==cluster:
        return True
    return True

def getClusterInsideLeftRightPattern(pageContent, leftPattern, insidePattern, rightPattern, threshold=30000):
    output = []
    leftPattern   = getRegExpStarBack(re.escape(removeRegExpStar(leftPattern)))
    insidePattern = getRegExpStarBack(re.escape(removeRegExpStar(insidePattern)))
    rightPattern = getRegExpStarBack(re.escape(removeRegExpStar(rightPattern)))
    leftPatternsLocation = getAllPatternLocations(leftPattern, pageContent)
    for (startL, endL) in leftPatternsLocation:
        rpLoc = re.search(rightPattern, pageContent[endL:])
        if not rpLoc is None:
            cluster = pageContent[endL:endL+rpLoc.start()]
            if len(cluster)<=threshold and not re.search(insidePattern, cluster) is None:
                output.append(cluster)
            if isClusterOnlyHtmlUnderLengthThrehold(cluster, threshold)==True:
                output.append(cluster)
    return list(set(output))

def getElementsOfCluster(cluster, insidePattern):
    insidePattern = getRegExpStarBack(re.escape(removeRegExpStar(insidePattern)))
    output = []
    patternsLocation = getAllPatternLocations(insidePattern, cluster)
    ePrev = 0
    for (s, e) in patternsLocation:
        output.append(cluster[ePrev:s])
        ePrev = e
    if len(cluster) - ePrev>0:
        output.append(cluster[ePrev:])
    return output
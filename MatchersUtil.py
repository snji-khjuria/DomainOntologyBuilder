#find entity set in left and right pattern.
def getAllEntitiesInsideLeftRightPattern(pageContent, leftPattern, rightPattern):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL+len(leftPattern)
            end    = pageContent.index(rightPattern, endL)
            if end-endL<=1000:
                output.append(pageContent[endL:end])
            searchIndex = startL+1
        except ValueError:
            return list(set(output))
    return list(set(output))


def notHtml(key, value):
    if "<" in key and ">" in key:
        return False
    return True

def getAllRelations(leftPattern, middlePattern, rightPattern, pageContent):
    searchIndex = 0
    output = []
    # print("LeftPattern:- " + leftPattern)
    # print("MiddlePattern:- " + middlePattern)
    # print("RightPattern:- " + rightPattern)
    # print(leftPattern in pageContent)
    # print(middlePattern in pageContent)
    # print(rightPattern in pageContent)
    while True:
        # print("Called")
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL+len(leftPattern)
            startM = pageContent.index(middlePattern, endL)
            endM   = startM + len(middlePattern)
            startR = pageContent.index(rightPattern, endM)
            searchIndex = startL+1
            key = pageContent[endL:startM].strip()
            value = pageContent[endM:startR].strip()
            # print("StartL is:- " + str(startL))
            # print("EndL   is:- " + str(endL))
            # print("startM is:- " + str(startM))
            # print("EndM is :- " + str(endM))
            # print("startR is:- " + str(startR))
            # print("Key is " + str(key))
            # print("Value is " + str(value))
            if len(key)<=1000 and len(value)<=1000 and notHtml(key, value):
                output.append((key, value))
        except ValueError:
            return list(set(output))
    return list((output))





def getClusterInsideLeftRightPattern(pageContent, leftPattern, insidePattern, rightPattern):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL+len(leftPattern)
            end    = pageContent.index(rightPattern, endL)
            cluster = pageContent[endL:end]
            if len(cluster)<=30000 and (insidePattern in cluster):
                output.append(cluster)
            searchIndex = startL+1
        except ValueError:
            return list(set(output))
    return list(set(output))


def getElementsOfCluster(cluster, insidePattern):
    output = []
    while True:
        index = cluster.find(insidePattern)
        if index==-1:
            cluster = cluster.strip()
            if len(cluster)>=1:
                output.append(cluster.strip())
            break
        output.append(cluster[:index].strip())
        index+=len(insidePattern)
        cluster = cluster[index:]
    return output





#Pattern matching code available in python jupyter notebook

#Pattern is (l, r) and match them to htmlPageContent
#def findEntitySetwrtPattern(htmlPageContent, (l, r)):
    #for each start location of pattern find its end
    #for each end page find the pattern right
    #extract everything till that point
    #after extraction move one point above that pattern string
    # results = []
    # for m in re.finditer(re.escape(l), htmlPageContent):
    #     start = m.start()
    #     end = m.end()
    #     rightPage = htmlPageContent[end:]
    #     rightLoc  = rightPage.find(r)
    #     if rightLoc==-1:
    #         break
    #     element = rightPage[:rightLoc]
    #     if len(element)>1 and len(element)<300:
    #         results.append(element)
    # return set(results)
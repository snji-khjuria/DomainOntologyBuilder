import os.path
#create the directories if not available
def createDirectoriesIfNotAvailable(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

#get all subdirectories in a directory
def getSubdirsInDirectory(dirPath):
    return [os.path.join(dirPath, o) for o in os.listdir(dirPath)
     if os.path.isdir(os.path.join(dirPath, o))]

#get website locations
def getWebsiteLocations(dirPath):
    return getSubdirsInDirectory(dirPath)

#get pages present inside website
def getAllPagesInsideWebsite(websiteLocation):
    return getSubdirsInDirectory(websiteLocation)


#reading the contents of file in a python list
def readFileContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        lines = [line.strip() for line in file]
    return lines

import re

def readFileRelationContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        lines = [line.strip() for line in file]
    output = []
    for line in lines:
        relation = re.split(r'\t+', line)
        if len(relation)==2:
            output.append((relation[0], relation[1]))
    return output


from StringUtil import replaceMultiWhitespaceWithSingle, replaceHtmlTags

#read full page plain html
def readPlainHtmlPageContent(fileLocation):
    fullPage = ""
    with open(fileLocation, 'r') as myfile:
        fullPage = myfile.read()
    return replaceHtmlTags(replaceMultiWhitespaceWithSingle(fullPage))
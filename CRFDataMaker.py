import configparser


myConfigParser                = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                   = "CRFDataMaker"

configSection                 = myConfigParser[sectionName]
paraContentLocationConfig     = "paraContentLocation"
titleContentLocationConfig    = "titleContentLocation"
paraTrainLocationConfig       = "paraTrainLocation"
paraTestLocationConfig        = "paraTestLocation"
titleTrainLocationConfig      = "titleTrainLocation"
titleTestLocationConfig       = "titleTestLocation"

paraContentLocation           = configSection[paraContentLocationConfig]
titleContentLocation          = configSection[titleContentLocationConfig]
paraTrainOutputLocation       = configSection[paraTrainLocationConfig]
paraTestOutputLocation        = configSection[paraTestLocationConfig]
titleTrainOutputLocation      = configSection[titleTrainLocationConfig]
titleTestOutputLocation       = configSection[titleTestLocationConfig]

coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"
from stanfordcorenlp import StanfordCoreNLP
nlpEngine = StanfordCoreNLP(coreNLPLocation)

#reading the contents of file in a python list
def readFileContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        lines = [line.strip() for line in file]
    return lines

def getOtherWordsList(words):
    l = words.split()
    output = []
    for item in l:
        output.append((item, "O"))
    return output

def getTaggingWords(words):
    l = words.strip().split()
    lastWord = l[len(l)-1]
    loc      = lastWord.find("/")
    lastWordStr   = lastWord[:loc]
    attributeName = lastWord[loc+1:]
    l[len(l)-1]   = lastWordStr
    output        = []
    # print("L is:- " + str(l))
    output.append((l[0], "B-" + attributeName))
    for index in range(1, len(l)):
        buffer = l[index].strip()
        if len(buffer)==0:
            continue
        output.append((l[index], "I-" + attributeName))
    return output

def getTrainingLine(line):
    startBracketIndex = 0
    offset            = 0
    output = []
    while True:
        startBracketIndex = line.find("[", offset)
        if startBracketIndex==-1:
            break
        endBracketIndex   = line.find("]", startBracketIndex)
        otherWords        = line[:startBracketIndex]
        otherWordsList    = getOtherWordsList(otherWords)
        # print(otherWordsList)
        if len(otherWordsList)>0:
            output.extend(otherWordsList)
        myTaggingWords    = line[startBracketIndex+1:endBracketIndex]
        myTaggingWords    = getTaggingWords(myTaggingWords)
        if len(myTaggingWords)>0:
            output.extend(myTaggingWords)
        if endBracketIndex+1==len(line):
            line = ""
        else:
            line              = line[endBracketIndex+1:]
    otherWordsList = getOtherWordsList(line)
    output.extend(otherWordsList)
    return output


def convertListToLine(l, posTags):
    output = ""
    # if len(l)!=len(posTags):
    #     print("ERROR" + str(len(l)) +" " + str(len(posTags)))
    #     print(l)
    #     print(posTags)
        # exit(1)
    for index in range(0, len(l)):
        item              = l[index]
        (word, attribTag) = item
        if word in posTags:
            posTag = posTags[word]
        else:
            posTag = "NOT_KNOWN"
        # posTagPlusWord    = posTags[index]
        # (w, posTag)       = posTagPlusWord
        # print("Word:- " + str(word))
        # print("attribTag:- " +str(attribTag))

        output           += word + "\t" + posTag + "\t" + attribTag + "\n"
    return output

def writeStrToFile(outputLocation, output):
    with open(outputLocation, "w") as f:
        f.write(output)

def getPosTags(line):
    l = nlpEngine.pos_tag(line)
    # return l
    output = {}
    # print(l)
    for (a, b) in l:
        output[a] = b
    return output

def getPlainLine(l):
    output = ""
    for(k, v) in l:
        output+=k+" "
    return output.strip()

def getTrainTestContent(lines):
    count = 1
    trainOutput = ""
    testOutput  = ""
    totalCount = len(lines)
    threshold = (int)(0.80*totalCount)
    for line in lines:
        count+=1
        if count%10==0:
            print(str(count) + " processed out of " + str(totalCount))
        # print(line)
        trainingLine = getTrainingLine(line)
        plainLine    = getPlainLine(trainingLine)
        # print("LIne is " + plainLine)
        posTags      = getPosTags(plainLine)
        trainingLine = convertListToLine(trainingLine, posTags)
        if count<=threshold:
            trainOutput+=trainingLine+"\n"
        else:
            testOutput+=trainingLine+"\n"
        # output+=trainingLine+"\n"
        # print(trainingLine)
    return (trainOutput, testOutput)


paraLines                = readFileContentInList(paraContentLocation)
titleLines               = readFileContentInList(titleContentLocation)
(paraTrain, paraTest)    = getTrainTestContent(paraLines)
(titleTrain, titleTest)  = getTrainTestContent(titleLines)
writeStrToFile(paraTrainOutputLocation, paraTrain)
writeStrToFile(paraTestOutputLocation, paraTest)
writeStrToFile(titleTrainOutputLocation, titleTrain)
writeStrToFile(titleTestOutputLocation, titleTest)
print("Output written at location:- " + paraTrainOutputLocation)
print("Output written at location:- " + paraTestOutputLocation)
print("Output written at location:- " + titleTrainOutputLocation)
print("Output written at location:- " + titleTestOutputLocation)
#training line algorithm
#for all [ in string read string till that position
#for each word produce other symbol
#now find the ] position and once found then for all the words inside produce that label with B and I
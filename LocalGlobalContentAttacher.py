import configparser


myConfigParser                   = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                      = "LocalGlobalContentAttacher"

configSection                    = myConfigParser[sectionName]
localTagsContentLocationConfig   = "localTagsContentLocation"
globalTagsContentLocationConfig  = "globalTagsContentLocation"
outputLocationConfig             = "outputLocation"


localTagsContentLocation  = configSection[localTagsContentLocationConfig]
globalTagsContentLocation = configSection[globalTagsContentLocationConfig]
outputLocation            = configSection[outputLocationConfig]



globalTagTitleContentLocation = globalTagsContentLocation + "/globallyTaggedTitles"
globalTagParaContentLocation  = globalTagsContentLocation + "/globallyTaggedParas"
from stanfordcorenlp import StanfordCoreNLP
coreNLPLocation       = "/home/sanjeevk/Desktop/NellKgExtraction/javaLib/stanford-corenlp-full-2017-06-09"
nlpEngine = StanfordCoreNLP(coreNLPLocation)

def getPosTags(line):
    l = nlpEngine.pos_tag(line)
    # return l
    output = ""
    # print(l)
    for (a, b) in l:
        output+=" " + b
    return output.strip()

def readFileContentInList(fileLocation):
    output = []
    with open(fileLocation, "r") as f:
        for line in f:
            line = line.strip()
            if len(line)==0:
                output.append([])
            else:
                line      = line.split()
                word      = line[0]
                globalTag = line[1]
                localTag  = line[2]
                output.append([word, globalTag, localTag])
    return output

def getMyGlobalTagEndIndex(lines, index):
    i = index+1
    [w, g, l] = lines[index]
    startTag  = "I-" + g[2:]
    while i<len(lines):
        line = lines[i]
        if len(line)<=0:
            break
        [w, g, l] = line
        if g!=startTag:
            break
        else:
            i+=1
    return i-1

def checkValidity(lines, startIndex, endIndex):
    for buffer in range(startIndex, endIndex+1):
        [w, g, l] = lines[buffer]
        if l!="O":
            return False
    return True

def readContentWRTGlobal(fileLocation):
    goodContent  = []
    errorContent = []
    sentence = ""
    tags     = ""
    errorFlag = False
    count = 0
    # errorCount = 0
    f = readFileContentInList(fileLocation)
    for index in range(0, len(f)):
        line = f[index]
        if len(line)==0:
            count+=1
            if errorFlag==False:
                posTags = getPosTags(sentence)
                goodContent.append((sentence, posTags, tags))
            else:
                errorContent.append((sentence, tags))
            sentence  = ""
            tags      = ""
            errorFlag = False
            if count%1000==0:
                print("Count " + str(count) + " processed.")
            continue
        [word, globalTag, localTag] = line
        if localTag == "O":
            if globalTag!="O" and globalTag.startswith("B-"):
                indexEnd            = getMyGlobalTagEndIndex(f, index)
                indexEndCheckStatus = checkValidity(f, index, indexEnd)
                if indexEndCheckStatus==True:
                    # print("Yo")
                    for buffer in range(index, indexEndCheckStatus+1):
                        # print("Buffered line: - " + str(line[buffer]) )
                        [w, g, l] = f[buffer]
                        print([w, g, l])
                        f[buffer] = [w, g, g]
            if "/" in globalTag:
                errorFlag = True

        #get that line back because is updated
        [word, globalTag, localTag] = f[index]
            # errorCount+=1
        sentence+=" " + word
        tags+=" " + localTag
    # print("Errro count:- " + str(errorCount))
    return (goodContent, errorContent)


def readContentWRTGlobal2(fileLocation):
    goodContent  = []
    errorContent = []
    errorCount = 0
    with open(fileLocation, "r") as f:
        sentence = ""
        tags     = ""
        errorFlag = False
        count = 0
        for line in f:
            line = line.strip()
            if len(line)==0:
                count+=1
                if errorFlag==False:
                    posTags = getPosTags(sentence)
                    goodContent.append((sentence, posTags, tags))
                else:
                    errorContent.append((sentence, tags))
                sentence  = ""
                tags      = ""
                errorFlag = False
                if count%10==0:
                    print("Count " + str(count) + " processed.")
                continue
            lineContent = line.split()
            word        = lineContent[0]
            globalTag   = lineContent[1]
            localTag    = lineContent[2]
            if localTag=="O":
                localTag = globalTag
                if "/" in globalTag:
                    errorFlag=True
            sentence+=" " + word
            tags+=" " + localTag
    return (goodContent, errorContent)

def getTrainTestSplit(content, inTrain):
    train = []
    test = []
    index = 0
    trainTotal = (int)(len(content)*inTrain)
    for index in range(0, len(content)):
        if index<=trainTotal:
            train.append(content[index])
        else:
            test.append(content[index])
    return (train, test)

def getCrfTrainData(content):
    outputStr = ""
    errorSentenceCount = 0
    for item in content:
        (sentence, posTags, groundTruth) = item
        # print("Sentence is :- " + str(sentence))
        # print("postags ")
        sentence = sentence.strip().split()
        posTags = posTags.strip().split()
        groundTruth = groundTruth.strip().split()
        if len(sentence)!=len(posTags) or len(sentence)!=len(groundTruth):
            # print("Error Sentence is:- ")
            # print(sentence)
            # print(len(sentence))
            # print(posTags)
            # print(len(posTags))
            # print(groundTruth)
            # print(len(groundTruth))
            errorSentenceCount+=1
            continue
        for index in range(0, len(sentence)):
            word = sentence[index]
            posTag = posTags[index]
            gTruth = groundTruth[index]
            # print(word + " " + posTag + " " + gTruth)
            outputStr+=word+"\t"+posTag+"\t"+gTruth+"\n"
        outputStr+="\n"
    print("Total Error sentences:- " + str(errorSentenceCount))
    return outputStr

def getErrorDataStr(content):
    outputStr = ""
    for item in content:
        (sentence, groundTruth) = item
        sentence = sentence.strip().split()
        groundTruth = groundTruth.strip().split()
        outputSentences = [""]
        for index in range(0, len(sentence)):
            word = sentence[index]
            noisyLabelsList = groundTruth[index].split("/")
            outputBuffer = []
            for item in outputSentences:
                for noisyLabel in noisyLabelsList:
                    nextContent = word+"/"+noisyLabel
                    buffer = item+" " + nextContent
                    outputBuffer.append(buffer)
            outputSentences = outputBuffer
        for item in outputSentences:
            outputStr+=item+"\n\n"
    return outputStr





def writeStrToFile(content, fileLocation):
    with open(fileLocation, "w") as f:
        f.write(content)
def writeLToFile(content, fileLocation):
    output = ""
    for item in content:
        output+=str(item)+"\n"
    writeStrToFile(output, fileLocation)

print("Reading titles content:- ")
(goodTitles, errorTitles)         = readContentWRTGlobal(globalTagTitleContentLocation)
# writeLToFile(goodTitles, "/home/sanjeevk/Desktop/helperContent/localTagger/laptops/globallyTaggedData/buffer")
(goodParas, errorParas)           = readContentWRTGlobal(globalTagParaContentLocation)
(goodTitlesTrain, goodTitlesTest) = getTrainTestSplit(goodTitles, 0.80)
(goodParasTrain, goodParasTest)   = getTrainTestSplit(goodParas, 0.80)
titleTrainCrf                     = getCrfTrainData(goodTitlesTrain)
titleTestCrf                      = getCrfTrainData(goodTitlesTest)
parasTrainCrf                     = getCrfTrainData(goodParasTrain)
parasTestCrf                      = getCrfTrainData(goodParasTest)
errorTitlesStr                    = getErrorDataStr(errorTitles)
errorParasStr                     = getErrorDataStr(errorParas)
writeStrToFile(titleTrainCrf, outputLocation  + "/titleTrainCrf")
writeStrToFile(titleTestCrf, outputLocation   + "/titleTestCrf")
writeStrToFile(parasTrainCrf, outputLocation  + "/parasTrainCrf")
writeStrToFile(parasTestCrf, outputLocation   + "/parasTestCrf")
writeStrToFile(errorTitlesStr, outputLocation + "/globalLevelTitleErrors")
writeStrToFile(errorParasStr, outputLocation  + "/globalLevelParasErrors")
print("Outputted everything")
nlpEngine.close()
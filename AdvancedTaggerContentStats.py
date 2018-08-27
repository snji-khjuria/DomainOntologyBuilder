trainLocation               = "/home/sanjeevk/Desktop/helperContent/localTagger/mobiles/clubbedContent/titlesOutputLocation"
# testLocation                = "/home/sanjeevk/Desktop/helperContent/crfData/mobile/title/test_advanced.data"
trainExtraOutputLocation    = "/home/sanjeevk/Desktop/helperContent/localTagger/mobiles/clubbedContent/extraTags.data"
# testExtraOutputLocation     = "/home/sanjeevk/Desktop/helperContent/crfData/mobile/title/test_extraTags.data"
trainSentenceOutputLocation = "/home/sanjeevk/Desktop/helperContent/localTagger/mobiles/clubbedContent/advsentences.data"
# testSentenceOutputLocation  = "/home/sanjeevk/Desktop/helperContent/crfData/mobile/title/test_Advsentences.data"

def writeStrToFileLocation(output, outputLocation):
    with open(outputLocation, "w") as f:
        f.write(output)


import csv
def readCoverage(fileLocation):
    total          = 0
    globalNotOther = 0
    words          = []
    sentences      = []
    with open(fileLocation, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        line = ""
        localSentence  = ""
        globalSentence = ""
        holySentence   = ""
        changedWords   = ""
        flagInclude    = False
        for row in reader:
            if len(row)==0:
                if flagInclude == True:
                    if len(changedWords)>1:
                        changedWords = changedWords[1:]
                    sentences.append((localSentence, globalSentence, holySentence, changedWords))
                localSentence  = ""
                globalSentence = ""
                holySentence   = ""
                flagInclude    = False
                changedWords   = ""
                continue
            word      = row[0]
            globalTag = row[1]
            localTag  = row[2]
            localSentence+=" " + word + "/" + localTag
            globalSentence+=" " + word + "/" + globalTag
            holySentence  += " " + word
            if localTag=="O" and globalTag!="O":
                flagInclude = True
                globalNotOther+=1
                changedWords+=", " + word
                words.append((word, globalTag))
            total+=1
    return (total, globalNotOther, words, sentences)

def getStr(words):
    outputList = []
    output = ""
    for (a, b) in words:
        outputList.append(a+"\t" + b)
        # output+=a+"\t" + b+"\n"
    outputList = list(set(outputList))
    for a in outputList:
        output+=a+"\n"
    return output

def getSentenceStr(sentences):
    output = ""
    for (a, b, c, d) in sentences:
        a=a.strip()
        b=b.strip()
        c=c.strip()
        d=d.strip()
        output+="Local:- "+a+"\nGlobal:- "+b+"\nActual:- "+c+"\nWordsChanged:- "+d+"\n\n\n\n"
    return output

(totalTrain, globalNotOtherTrain, wordsTrain, sentences) = readCoverage(trainLocation)
print("Total:- " + str(totalTrain))
print("Global not other train:- " + str(globalNotOtherTrain))
print(wordsTrain)
wordsTrain = getStr(wordsTrain)
sentencesStr = getSentenceStr(sentences)
writeStrToFileLocation(wordsTrain, trainExtraOutputLocation)
writeStrToFileLocation(sentencesStr, trainSentenceOutputLocation)
# (totalTest, globalNotOtherTest, wordsTest, sentences) = readCoverage(testLocation)
# print("Total:- " + str(totalTest))
# print("Global not other test:- " + str(globalNotOtherTest))
# print(wordsTest)
# wordsTest = getStr(wordsTest)
# sentencesStr = getSentenceStr(sentences)
# writeStrToFileLocation(wordsTest, testExtraOutputLocation)
# writeStrToFileLocation(sentencesStr, testSentenceOutputLocation)
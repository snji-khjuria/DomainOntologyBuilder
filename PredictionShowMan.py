import configparser


myConfigParser                = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                   = "PredictionShowMan"

configSection                 = myConfigParser[sectionName]

paraInputConfig    = "paraPredictionInputLocation"
paraOutputConfid   = "paraPredictionOutputLocation"
titleInputConfig   = "titlePredictionInputLocation"
titleOutputConfig  = "titlePredictionOutputLocation"

paraInputLocation   = configSection[paraInputConfig]
paraOutputLocation  = configSection[paraOutputConfid]
titleInputLocation  = configSection[titleInputConfig]
titleOutputLocation = configSection[titleOutputConfig]

import csv
def readFileContent(fileLocation):
    output = []
    with open(fileLocation, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        line = ""
        for row in reader:
            # print("Row is:- " + str(row))
            if len(row)==0:
                output.append(line.strip())
                line = ""
                continue
            word  = row[0]
            label = row[3]
            if label!="O" and (label.startswith("B-") or label.startswith("I-")):
                word+="/"+label[2:]
            line+=word+" "
    return output

def getListAsStr(l):
    output = ""
    for item in l:
        output+=item+"\n\n"
    return output.strip()

def writeStrAsOutput(fileLocation, s):
    with open(fileLocation, 'w') as f:
        f.write(s)



def readLabels(lines):
    predicted = []
    gold      = []
    for line in lines:
        line = line.strip()
        if len(line)==0:
            continue
        line = line.split()
        gold.append(line[2])
        predicted.append(line[3])
    return (gold, predicted)

def findTotalCorrect(gold, predicted):
    total = len(gold)
    count=0
    for index in range(0, total):
        if gold[index]==predicted[index]:
            count+=1
    return count

def findTotalCorrectWithNotOtherTag(gold, predicted):
    total = len(gold)
    count=0
    for index in range(0, total):
        if gold[index]==predicted[index] and gold[index]!='O':
            count+=1
    return count

def findJunkStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords):
    total = len(gold)
    count=0
    output          = []
    wordsOutput     = []
    sentencesOutput = []
    separator = "----------------------------------------------------\n"
    for index in range(0, total):
        if predicted[index]!='O' and gold[index]=='O':
            count+=1
            output.append(predicted[index])
            wordsOutput.append(words[index])
            # print("Keys are:- " + str(sentenceIndexForWords.keys()))
            sentenceIndex = sentenceIndexForWords[index]
            sentencesOutput.append(separator + sentences[sentenceIndex] + "\n\nGold: " + goldSentences[sentenceIndex] + "\n\nPredicted: " + predictedSentences[sentenceIndex]+"\n"+separator)
    return (count, output, wordsOutput, sentencesOutput)


def findLostInfoStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords):
    total = len(gold)
    count=0
    output          = []
    wordsOutput     = []
    sentencesOutput = []
    separator = "----------------------------------------------------\n"
    for index in range(0, total):
        if predicted[index]=='O' and gold[index]!='O':
            count+=1
            output.append(gold[index])
            wordsOutput.append(words[index])
            sentenceIndex = sentenceIndexForWords[index]
            sentencesOutput.append(separator + sentences[sentenceIndex] + "\nGold: " + goldSentences[sentenceIndex] + "\nPredicted: " + predictedSentences[sentenceIndex]+"\n"+separator)
    return (count, output, wordsOutput, sentencesOutput)


def findAllInfo(elt):
    count=0
    for item in elt:
        if item!='O':
            count+=1
    return count

def readWords(lines):
    output = []
    for item in lines:
        item = item.strip()
        if len(item)==0:
            continue
        item = item.split()
        output.append(item[0])
    return output

def getMappedList(l1, l2, l3):
    output = ""
    for index in range(0, len(l1)):
        output+=l1[index] + "\t" + l2[index] + "\nIn\n" + l3[index] + "\n----------\n"
    return output

#reading the contents of file in a python list
def readFileContentInList(fileLocation):
    lines = []
    with open(fileLocation) as file:
        lines = [line.strip() for line in file]
    return lines

def readSentences(lines):
    sentences = []
    predictedSentences = []
    goldSentences      = []
    sentence = ""
    predictedSentence  = ""
    goldSentence       = ""
    for line in lines:
        line = line.strip()
        if len(line)==0:
            sentences.append(sentence)
            predictedSentences.append(predictedSentence)
            goldSentences.append(goldSentence)
            sentence          = ""
            goldSentence      = ""
            predictedSentence = ""
        else:
            line = line.split()
            sentence+=" " + line[0]
            goldLabel = line[2]
            if goldLabel=="O":
                goldLabel = ""
            else:
                goldLabel="/"+goldLabel
            weakLabel = line[3]
            if weakLabel=="O":
                weakLabel = ""
            else:
                weakLabel = "/" + weakLabel
            goldSentence+=" " + line[0] + goldLabel
            predictedSentence+=" " + line[0]+weakLabel
    return (sentences, goldSentences, predictedSentences)

def getIndexToSentenceMapping(lines):
    index=0
    sentenceDict = {}
    sentenceIndex = 0
    wordIndex     = 0
    for index in range(0, len(lines)):
        line = lines[index]
        line = line.strip()
        if len(line)==0:
            sentenceIndex+=1
            continue
        sentenceDict[wordIndex] = sentenceIndex
        wordIndex+=1
    return sentenceDict

def getStats(inputLocation):
    lines                                             = readFileContentInList(inputLocation)
    words                                             = readWords(lines)
    (sentences, goldSentences, predictedSentences)    = readSentences(lines)
    sentenceIndexForWords                             = getIndexToSentenceMapping(lines)
    (gold, predicted)                                 = readLabels(lines)
    totalCorrect                                      = findTotalCorrect(gold, predicted)
    totalCorrectWithNoOtherTag                        = findTotalCorrectWithNotOtherTag(gold, predicted)
    (totalJunk, junkLabels, junkWords, junkSentences) = findJunkStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords)
    (totalLost, lostLabels, lostWords, lostSentences) = findLostInfoStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords)
    total = len(gold)
    output = ""
    output+="Total:-                   " + str(total) + "\n"
    output+="Total correct:-           " + str(totalCorrect) + "\n"
    output+="Total Incorrect:-         " + str(total-totalCorrect) + "\n"
    output+="Total Information:-       " + str(findAllInfo(gold)) + "\n"
    output+="Information lost:-        "  + str(findAllInfo(gold)-totalCorrectWithNoOtherTag) + "\n"
    output+="New information found/Total Correct without O tag:-   " + str(totalCorrectWithNoOtherTag) + "\n"
    output+="Junk:-" + str(totalJunk) + "\n"
    output+=getMappedList(junkLabels, junkWords, junkSentences) + "\n"
    output+="\n\n=============================================\n\n\n"
    output+="Lost Information:- " + str(totalLost) + "\n"
    output+=getMappedList(lostLabels, lostWords, lostSentences)   + "\n"

    return output

outputPara  = readFileContent(paraInputLocation)
outputTitle = readFileContent(titleInputLocation)



sPara       = getStats(paraInputLocation)  + getListAsStr(outputPara)
sTitle      = getStats(titleInputLocation) + getListAsStr(outputTitle)
writeStrAsOutput(paraOutputLocation, sPara)
writeStrAsOutput(titleOutputLocation, sTitle)
print("Written at location:- " + paraOutputLocation)
print("Written at location:- " + titleOutputLocation)
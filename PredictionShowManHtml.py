import configparser


myConfigParser                = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                   = "PredictionShowManHtml"

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
    output = "<ul>"
    for item in l:
        output+="<li>" + item+"</li></br>"
    return output.strip() + "</ul>"

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


def findLostInfoCount(gold, predicted):
    total = len(gold)
    count = 0
    for index in range(0, total):
        if predicted[index]=="O" and gold[index] != 'O':
            count += 1
    return count


def createTableRowsForSentence(sentence, gold, predicted):
    output = "\n<table border=1px>"
    row1   = "<tr><td>Sentence</td><td>" + sentence + "</td></tr>"
    row2   = "<tr><td>Gold</td><td>" + gold     + "</td></tr>"
    row3   = "<tr><td>Predicted</td><td>" + predicted  + "</td></tr>"
    return output + row1 + row2 + row3 + "</table>\n"


def findJunkStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords):
    total = len(gold)
    count=0
    output          = []
    wordsOutput     = []
    sentencesOutput = []
    relevantSentencesStrList = []
    separator = "----------------------------------------------------\n"
    for index in range(0, total):
        if predicted[index]!='O' and gold[index]=='O':
            count+=1
            output.append(predicted[index])
            wordsOutput.append(words[index])
            # print("Keys are:- " + str(sentenceIndexForWords.keys()))
            sentenceIndex = sentenceIndexForWords[index]
            sentencesOutput.append(createTableRowsForSentence(sentences[sentenceIndex], goldSentences[sentenceIndex],
                                                              predictedSentences[sentenceIndex]))
            relevantSentencesStrList.append((sentences[sentenceIndex], goldSentences[sentenceIndex], predictedSentences[sentenceIndex]))
            # sentencesOutput.append(separator + sentences[sentenceIndex] + "\n\nGold: " + goldSentences[sentenceIndex] + "\n\nPredicted: " + predictedSentences[sentenceIndex]+"\n"+separator)
    return (count, output, wordsOutput, sentencesOutput, relevantSentencesStrList)



def findLostInfoStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords):
    total = len(gold)
    count=0
    output          = []
    wordsOutput     = []
    sentencesOutput = []
    relevantSentencesStrList = []
    tableStart = "<table>"
    tableEnd   = "</table>"
    for index in range(0, total):
        if predicted[index]=='O' and gold[index]!='O':
            count+=1
            output.append(gold[index])
            wordsOutput.append(words[index])
            sentenceIndex = sentenceIndexForWords[index]
            sentencesOutput.append(createTableRowsForSentence(sentences[sentenceIndex], goldSentences[sentenceIndex], predictedSentences[sentenceIndex]))
            relevantSentencesStrList.append(
                (sentences[sentenceIndex], goldSentences[sentenceIndex], predictedSentences[sentenceIndex]))
        # sentencesOutput.append(separator + sentences[sentenceIndex] + "<br/>Gold: " + goldSentences[sentenceIndex] + "<br/>Predicted: " + predictedSentences[sentenceIndex]+"<br/>"+separator)
    return (count, output, wordsOutput, sentencesOutput, relevantSentencesStrList)

def findOtherErrors(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords):
    total = len(gold)
    count=0
    output          = []
    predictedOutput       = []
    wordsOutput     = []
    sentencesOutput = []
    relevantSentencesStrList = []
    tableStart = "<table>"
    tableEnd   = "</table>"
    for index in range(0, total):
        if predicted[index]!='O' and gold[index]!='O' and predicted[index]!=gold[index]:
            count+=1
            output.append(gold[index])
            predictedOutput.append(predicted[index])
            wordsOutput.append(words[index])
            sentenceIndex = sentenceIndexForWords[index]
            sentencesOutput.append(createTableRowsForSentence(sentences[sentenceIndex], goldSentences[sentenceIndex], predictedSentences[sentenceIndex]))
            relevantSentencesStrList.append(
                (sentences[sentenceIndex], goldSentences[sentenceIndex], predictedSentences[sentenceIndex]))
        # sentencesOutput.append(separator + sentences[sentenceIndex] + "<br/>Gold: " + goldSentences[sentenceIndex] + "<br/>Predicted: " + predictedSentences[sentenceIndex]+"<br/>"+separator)
    return (count, output, predictedOutput, wordsOutput, sentencesOutput, relevantSentencesStrList)


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

def createTableHtml(item1, item2):
    return "<table border=1px><tr><td>" + item1 + "</td><td>" + item2 + "</td></tr></table>"

def createTableHtml2(item1, item2, item3):
    return "<table border=1px><tr><td>" + item1 + "</td><td>" + item2 + "</td><td>" + item3 + "</td></tr></table>"
def getBoldSentence(sentence, word):
    index = 0
    while True:
        index = sentence.find(word, index)
        print("Index is " + str(index))
        print(sentence)
        if index==-1:
            return sentence
        prevContent = sentence[:index] + "<b>"
        nextContent = sentence[index:index+len(word)] + "</b>" + sentence[index+len(word):]
        sentence = prevContent + nextContent
        #for the bold element added
        index+=3
        index+=1

def getMappedList(l1, l2, l3):
    output = ""
    for index in range(0, len(l1)):
        tag = l1[index]
        word = l2[index]
        s = createTableHtml(tag, word)
        fullPredictedWord = word +"/" + tag
        boldSentence = getBoldSentence(l3[index], fullPredictedWord)
        output+="Error " + str(index+1) + ":-<br/>" + s + "<br/>Content<br/>" + boldSentence + "<br/>----------<br/>"
    return output


def getMappedList2(l1, l2, l3, l4):
    output = ""
    for index in range(0, len(l1)):
        tag = l1[index]
        predictedTag = l2[index]
        word = l3[index]
        s = createTableHtml2(tag, predictedTag, word)
        fullPredictedWord = word +"/" + tag
        fullMyPredictedWord = word + "/" + predictedTag
        boldSentence = getBoldSentence(l4[index], fullPredictedWord)
        boldSentence = getBoldSentence(boldSentence, fullMyPredictedWord)
        output+="Error " + str(index+1) + ":-<br/>" + s + "<br/>Content<br/>" + boldSentence + "<br/>----------<br/>"
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

def sortDict(d):
    items = [(v, k) for k, v in d.items()]
    items.sort()
    items.reverse()
    return [(k, v) for (v, k) in items]
def getErrorSet(gold, predicted):
    d = {}
    bufferStr = "<table border=1px><tr><td>GoldLabel</td><td>PredictedLabel</td><td>count</td></tr>"
    for index in range(0, len(gold)):
        goldLabel = gold[index]
        predictedLabel = predicted[index]
        key = goldLabel + "</td><td>" + predictedLabel
        if key in d:
            buffer=d[key]
        else:
            buffer=0
        d[key] = buffer+1
    dictStr = ""
    d = sortDict(d)
    for (k, v) in d:
        dictStr+="<tr><td>" + k+"</td><td>" + str(v) + "</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr

def getErrorSetWithWords(gold, predicted, words):
    d = {}
    bufferStr = "<table border=1px><tr><td>GoldLabel</td><td>PredictedLabel</td><td>Word</td><td>count</td></tr>"
    for index in range(0, len(gold)):
        goldLabel = gold[index]
        predictedLabel = predicted[index]
        word           = words[index]
        key = goldLabel + "</td><td>" + predictedLabel + "</td><td>" + word
        if key in d:
            buffer=d[key]
        else:
            buffer=0
        d[key] = buffer+1
    dictStr = ""
    d=sortDict(d)
    for (k, v) in d:
        dictStr+="<tr><td>" + k+"</td><td>" + str(v) + "</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr

def getErrorSetWithOtherTag(notOther):
    d = {}
    bufferStr = "<table border=1px><tr><td>NotOtherTag</td><td>OtherTag</td><td>count</td></tr>"
    for index in range(0, len(notOther)):
        notOtherLabel = notOther[index]
        key = notOtherLabel + "</td><td>Other"
        if key in d:
            buffer=d[key]
        else:
            buffer=0
        d[key] = buffer+1
    dictStr = ""
    d = sortDict(d)
    for (k, v) in d:
        dictStr+="<tr><td>" + k+"</td><td>" + str(v) + "</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr

def getErrorSetWithOtherTagAndWord(notOther, words):
    d = {}
    bufferStr = "<table border=1px><tr><td>NotOtherTag</td><td>Other</td><td>Word</td><td>count</td></tr>"
    for index in range(0, len(notOther)):
        notOtherLabel = notOther[index]
        word           = words[index]
        key = notOtherLabel + "</td><td>Other</td><td>" + word
        if key in d:
            buffer=d[key]
        else:
            buffer=0
        d[key] = buffer+1
    dictStr = ""
    d=sortDict(d)
    for (k, v) in d:
        dictStr+="<tr><td>" + k+"</td><td>" + str(v) + "</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr

def getErrorSetWithOtherTagAndWordSentence(notOther, words, sentences):
    d = {}
    s = {}
    bufferStr = "<table border=1px><tr><td>NotOtherTag</td><td>Other</td><td>Word</td><td>Sentence</td><td>Gold</td><td>Predicted</td><td>count</td></tr>"
    for index in range(0, len(notOther)):
        notOtherLabel = notOther[index]
        word           = words[index]
        sentence       = sentences[index]
        (trueSentence, goldTagged, predicted) = sentence
        key = notOtherLabel + "</td><td>Other</td><td>" + word
        if key in d:
            buffer=d[key]
            bufferS = s[key]
        else:
            buffer=0
            bufferS = ("", "", "")
        d[key] = buffer+1
        (s1, s2, s3) = bufferS
        s1 += "<br></br>" + trueSentence
        s2 += "<br></br>" + goldTagged
        s3 += "<br></br>" + predicted
        s[key] = (s1, s2, s3)
        # s[key] = bufferS + "<br/><br/>" + sentence
    dictStr = ""
    d=sortDict(d)
    for (k, v) in d:
        (s1, s2, s3) = s[k]
        dictStr+="<tr><td>" + k+"</td><td>" + s1 + "</td><td>" + s2 + "</td><td>" + s3 + "</td><td>" + str(v) +"</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr


def getErrorSetWithWordSentence(gold, predicted, words, sentences):
    d = {}
    s = {}
    bufferStr = "<table border=1px><tr><td>GoldLabel</td><td>PredictedLabel</td><td>Word</td><td>Sentence</td><td>Gold</td><td>Predicted</td><td>count</td></tr>"
    for index in range(0, len(gold)):
        goldLabel = gold[index]
        predictedLabel = predicted[index]
        word           = words[index]
        sentence       = sentences[index]
        (trueSentence, goldTagged, predictedS) = sentence
        key = goldLabel + "</td><td>" + predictedLabel + "</td><td>" + word
        if key in d:
            buffer=d[key]
            bufferS = s[key]
        else:
            buffer=0
            bufferS = ("", "", "")
        d[key] = buffer+1
        (s1, s2, s3) = bufferS
        s1 += "<br></br>" + trueSentence
        s2 += "<br></br>" + goldTagged
        s3 += "<br></br>" + predictedS
        s[key] = (s1, s2, s3)
        # s[key] = bufferS + "<br/><br/>" + sentence
    dictStr = ""
    d=sortDict(d)
    for (k, v) in d:
        (s1, s2, s3) = s[k]
        dictStr+="<tr><td>" + k+"</td><td>" + s1 + "</td><td>" + s2 + "</td><td>" + s3 + "</td><td>" + str(v) +"</td></tr>"
    dictStr = bufferStr + dictStr + "</table>"
    return dictStr




def getStats(inputLocation):
    lines                                             = readFileContentInList(inputLocation)
    words                                             = readWords(lines)
    (sentences, goldSentences, predictedSentences)    = readSentences(lines)
    sentenceIndexForWords                             = getIndexToSentenceMapping(lines)
    (gold, predicted)                                 = readLabels(lines)
    totalCorrect                                      = findTotalCorrect(gold, predicted)
    totalCorrectWithNoOtherTag                        = findTotalCorrectWithNotOtherTag(gold, predicted)
    newInfoFound                                      = findTotalCorrectWithNotOtherTag(gold, predicted)
    lostInfoCount                                     = findLostInfoCount(gold, predicted)
    (totalJunk, junkLabels, junkWords, junkSentences, relJunk)       = findJunkStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords)
    (totalLost, lostLabels, lostWords, lostSentences, relLost)       = findLostInfoStatsFromPredictions(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords)
    (otherErrors, otherLabels, otherPredicted, otherWords, otherSentences, relOther)  = findOtherErrors(gold, predicted, words, sentences, goldSentences, predictedSentences, sentenceIndexForWords)
    total = len(gold)
    output = ""
    output+="Total:-                   " + str(total) + "<br/>"
    output+="Total Information was present(rest was O):-       " + str(findAllInfo(gold)) + "<br/>"
    output+="Total correct:-           " + str(totalCorrect) + "<br/>"
    output+="Total Incorrect:-         " + str(total-totalCorrect) + "<br/>"
    # output+="Information lost:-        "  + str(findAllInfo(gold)-totalCorrectWithNoOtherTag) + "<br/>"
    output+="Information lost:-    "  + str(lostInfoCount) + "<br/>"
    # output+="New information found/Total Correct without O tag:-   " + str(totalCorrectWithNoOtherTag) + "<br/>"
    output+="Junk:-" + str(totalJunk) + "<br/>"
    output += "Other errors:- " + str(otherErrors) + "<br/>"
    output+=getErrorSetWithOtherTag(junkLabels)
    output+=getErrorSetWithOtherTagAndWord(junkLabels, junkWords)
    output+=getErrorSetWithOtherTagAndWordSentence(junkLabels, junkWords, relJunk)
    output+=getMappedList(junkLabels, junkWords, junkSentences) + "<br/>"
    output+="<br/><br/>=============================================<br/><br/><br/>"
    output+="Lost Information:- " + str(totalLost) + "<br/>"
    output += getErrorSetWithOtherTag(lostLabels)
    output += getErrorSetWithOtherTagAndWord(lostLabels, lostWords)
    output+=getErrorSetWithOtherTagAndWordSentence(lostLabels, lostWords, relLost)
    output+=getMappedList(lostLabels, lostWords, lostSentences)   + "<br/>"
    output+="Other errors:- " + str(otherErrors) + "<br/>"
    output+=getErrorSet(otherLabels, otherPredicted)
    output+=getErrorSetWithWords(otherLabels, otherPredicted, otherWords)
    output+=getErrorSetWithWordSentence(otherLabels, otherPredicted, otherWords, relOther)
    output+=getMappedList2(otherLabels, otherPredicted, otherWords, otherSentences)
    return output

outputPara  = readFileContent(paraInputLocation)
outputTitle = readFileContent(titleInputLocation)


htmlStart = "<html><head><title></title></head><body>"
htmlEnd   = "</body></html>"
sPara       = getStats(paraInputLocation)  + getListAsStr(outputPara)
sTitle      = getStats(titleInputLocation) + getListAsStr(outputTitle)
writeStrAsOutput(paraOutputLocation, htmlStart + sPara + htmlEnd)
writeStrAsOutput(titleOutputLocation, htmlStart + sTitle + htmlEnd)
print("Written at location:- " + paraOutputLocation)
print("Written at location:- " + titleOutputLocation)
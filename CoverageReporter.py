import configparser


myConfigParser                = configparser.ConfigParser()
myConfigParser.read("config.ini")
sectionName                   = "CoverageReporter"

configSection                 = myConfigParser[sectionName]

titleTrainLocationConfig = "titleTrainDataLocation"
titleTestLocationConfig  = "titleTestDataLocation"
paraTrainLocationConfig  = "paraTrainDataLocation"
paraTestLocationConfig   = "paraTestDataLocation"

titleTrainLocation       = configSection[titleTrainLocationConfig]
titleTestLocation        = configSection[titleTestLocationConfig]
paraTrainLocation        = configSection[paraTrainLocationConfig]
paraTestLocation         = configSection[paraTestLocationConfig]


import csv
def readCoverage(fileLocation):
    covered = 0
    total   = 0
    with open(fileLocation, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        line = ""
        for row in reader:
            if len(row)==0:
                continue
            tag = row[2]
            if tag!="O":
                covered+=1
            total+=1
    return (covered, total)


(titleTrainCoverage, titleTrainTotal) = readCoverage(titleTrainLocation)
(titleTestCoverage, titleTestTotal)   = readCoverage(titleTestLocation)
(paraTrainCoverage, paraTrainTotal)   = readCoverage(paraTrainLocation)
(paraTestCoverage, paraTestTotal)     = readCoverage(paraTestLocation)

print("TrainTitleCoverage:- " + str(titleTrainCoverage))
print("TrainTitleTotal:- "    + str(titleTrainTotal))
print("TestTitleCoverage:- "  + str(titleTestCoverage))
print("TestTitleTotal:- "     + str(titleTestTotal))
print("ParaTrainCoverage:- "  + str(paraTrainCoverage))
print("ParaTrainTotal:- "     + str(paraTrainTotal))
print("PraTestCoverage:- "    + str(paraTestCoverage))
print("ParaTestTotal:- "      + str(paraTestTotal))
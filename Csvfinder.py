fileLocation = "/home/sanjeevk/Desktop/helperContent/localTagger/mobiles/ontology/ontology.csv"
import csv
def readCrfData(fileLocation):
    output = []
    count=0
    with open(fileLocation, "r") as csvfile:
        reader          = csv.reader(csvfile, delimiter="\t")
        line            = ""
        weakSupervision = ""
        for row in reader:
            count+=1
            w1 = row[0]
            w2 = row[1]
            w3 = row[3]
            if w3.lower()=="videocon":
                print(w1)
            if count%1000000==0:
                print(str(count) + " processed")

readCrfData(fileLocation)

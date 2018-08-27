import csv
class Patterns:
    def __init__(self, productTitlePatterns, productSpecsPatterns, productRelationPatterns):
        self.productTitlePatterns     = productTitlePatterns
        self.productSpecsPatterns     = productSpecsPatterns
        self.productRelationPatterns  = productRelationPatterns


    #get product title patterns
    def getProductTitlePatterns(self):
        return self.productTitlePatterns


    def getProductSpecsPatterns(self):
        return self.productSpecsPatterns

    def getProductRelationPatterns(self):
        return self.productRelationPatterns


    # def getProductCategoryPatterns(self):
    #     return self.productCategoryPatterns

    def printProductSpecsPatterns(self):
        for (l, i, r) in self.productSpecsPatterns:
            print("Left:- " + l)
            print("Inside:- " + i)
            print("Right:- " + r)

    # def printProductCategoriesPatterns(self):
    #     for (l, i, r) in self.productCategoryPatterns:
    #         print("Left: " + l)
    #         print("Inside:- " + i)
    #         print("Right:- " + r)

    def printProductRelationPatterns(self):
        for (l, m, r) in self.productRelationPatterns:
            print("Left:- " + l)
            print("Middle:- " + m)
            print("RIght:- " + r)

    def printProductTitlePatterns(self):
        # print("Type is " + str(type(self.productTitlePatterns)))
        for (l, r) in self.productTitlePatterns:
            print("Left: " + l)
            print("Right: " + r)


    def writePatterns(self, location):
        output = [["LeftPatterns", "RightPatterns"]]
        for (l, r) in self.productTitlePatterns:
            output.append([l, r])
        productTitlePatternsLocation = location + "/productTitlePatterns.tsv"
        with open(productTitlePatternsLocation, "w") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(output)

class ProductInfo():
    def __init__(self, pageLocation, productTitle, productSpecs, productTable):
        self.pageLocation = pageLocation
        self.productTitle = productTitle
        self.productSpecs = productSpecs
        self.productTable = productTable

    def getPageLocation(self):
        return self.pageLocation

    def getProductTitle(self):
        return self.productTitle

    def getProductSpecs(self):
        return self.productSpecs

    def getProductTable(self):
        return self.productTable

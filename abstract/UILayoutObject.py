

class UILayoutObject(object):
    def __init__(self, cis, packageName, className, isScrollable):
        self.cis = cis
        self.packageName = packageName
        self.className = className

        self.isScrollable = isScrollable
        self.boundsX = None
        self.boundsY = None
        self.boundsWidth = None
        self.boundsHight = None
        pass

    def setBoundsAttr(self, x, y, width, hight):
        self.boundsX = x
        self.boundsY = y
        self.boundsWidth = width
        self.boundsHight = hight


    def __str__(self):
        return 'cis: '+ self.cis + ' packageName: '+ self.packageName + ' className: '+ self.className + ' bounds:['+ str(self.boundsX) + ' ' + str(self.boundsY) + ' ' + str(self.boundsWidth) + ' ' + str(self.boundsHight) + ']'
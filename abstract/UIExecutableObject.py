


class UIExecutableObject(object):

    def __init__(self, cis, packageName, className, clickable,
                 longClickable, checkable, text, resourceId, contentDesc,
                 index):
        self.cis = cis
        self.packageName = packageName
        self.className = className

        self.clickable = clickable
        self.longClickable = longClickable
        self.checkable = checkable
        self.text = text
        self.resourceId = resourceId
        self.contentDesc = contentDesc
        self.index = index

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
        return 'cis: '+ self.cis + ' packageName: '+ self.packageName + ' className: '+ self.className + ' click: '+ str(self.clickable) + ' longclick: '+ str(self.longClickable) +' checkable: '+ str(self.checkable) +  ' bounds:['+ str(self.boundsX) + ' ' + str(self.boundsY) + ' ' + str(self.boundsWidth) + ' ' + str(self.boundsHight) + ']'

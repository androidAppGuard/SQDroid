

class Utils(object):
    @staticmethod
    def parseBoundsStr(bounds):
        leftBrackets = bounds.index(']')
        firstComma = bounds.index(',')
        secondComma = bounds.index(',', firstComma + 1)

        x = int(bounds[1:firstComma])
        y = int(bounds[firstComma + 1:leftBrackets])
        width = int(bounds[leftBrackets + 2:secondComma]) - x
        hight = int(bounds[secondComma + 1:len(bounds)-1]) - y
        return (x, y, width, hight)

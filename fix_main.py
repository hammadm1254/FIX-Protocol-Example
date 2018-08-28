import functools
def getSecTransactions(fileName):
    with open(fileName, 'r') as datFile:
        data = datFile.read()
    _output = formatSecData(data)
    del data
    return _output

def formatSecData(secString):
    secDataList =[]
    for line in secString.split('\n'):
        secDataJSON = {}
        for tagValuePair in line.split('\x01'):
            if len(tagValuePair) > 0:
                tagValueList = tagValuePair.split('=')
                secDataJSON[int(tagValueList[0])] = tagValueList[1]
        if len(secDataJSON) > 0:
            secDataList.append(secDataJSON)
    return secDataList

def getTagCount(tagName, tagValue, trnsxnList):
    try:
        tagName = int(tagName)
    except ValueError:
        return 'Tag names are integers'
    try:
        tagValue = str(tagValue)
    except ValueError:
        return 'Tag Values are strings'
    count = 0
    for aTrnsxn in trnsxnList:
        try:
            if aTrnsxn[tagName] == tagValue:
                count += 1
        except KeyError:
            pass
    return count

def main():
    secFileName = 'secdef.dat'
    secTrans = getSecTransactions(secFileName)
    print(len(secTrans))

if __name__ == '__main__':
    main()
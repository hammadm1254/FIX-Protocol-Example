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

def verifyInput(tagName, tagValue, trnsxnList):
    assert(type(tagName) == int or tagName is None), 'Tag names are integer values'
    assert(type(tagValue) == str or tagValue is None), 'Tag values are strings'
    assert(type(trnsxnList) == list and len(trnsxnList) > 0), 'List of transactions must not be empty'

def getTransCountByTagValue(tagName, tagValue, trnsxnList):
    return len(getTransByTagValue(tagName, tagValue, trnsxnList))

def getTransByTagValue(tagName, tagValue, trnsxnList):
    verifyInput(tagName, tagValue, trnsxnList)
    return [aTrnsxn for aTrnsxn in trnsxnList if aTrnsxn[tagName] == tagValue]

def getTransByTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    return [aTrnsxsn for aTrnsxsn in trnsxnList if tagName in aTrnsxsn]

def getTransCountByTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    return len(getTransByTag(tagName, trnsxnList))

def countByTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    resultDict = {}
    for aTrnsxn in trnsxnList:
        try:
            resultDict[aTrnsxn[tagName]] += 1
        except KeyError:
            resultDict[aTrnsxn[tagName]] = 1
    return resultDict

def main():
    secFileName = 'secdef.dat'
    secTrans = getSecTransactions(secFileName)
    print(len(secTrans))

if __name__ == '__main__':
    main()
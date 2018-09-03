def getSecTransactions(fileName):
    with open(fileName, 'r') as datFile:
        data = datFile.readlines()
    assert(len(data) > 0), 'Data file must be non-empty and contain valid FIX data'
    _output = formatSecData(data)
    assert(len(_output) > 0), 'No FIX data was found in file'
    del data
    return _output

def formatSecData(dataList):
    secDataList = []
    for line in dataList:
        secDataJSON = {}
        for tagValuePair in line.split('\x01'):
            if len(tagValuePair) > 1:
                tagValueList = tagValuePair.split('=')
                if len(tagValueList) == 2:
                    secDataJSON[int(tagValueList[0])] = tagValueList[1]
        if len(secDataJSON) > 0 and 35 in secDataJSON:
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
    return [aTrnsxn for aTrnsxn in trnsxnList if tagName in aTrnsxn and aTrnsxn[tagName] == tagValue]

def getTransByTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    return [aTrnsxsn for aTrnsxsn in trnsxnList if tagName in aTrnsxsn]

def getTransCountByTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    return len(getTransByTag(tagName, trnsxnList))

def countValuesByTag(tagName, trnsxnList): #Q1
    verifyInput(tagName, None, trnsxnList)
    resultDict = {}
    for aTrnsxn in trnsxnList:
        if tagName in aTrnsxn:
            try:
                resultDict[aTrnsxn[tagName]] += 1
            except KeyError:
                resultDict[aTrnsxn[tagName]] = 1
    return resultDict

def joinByTag(innerTag, outerTag, trnsxnList):
    verifyInput(innerTag, None, trnsxnList)
    verifyInput(outerTag, None, trnsxnList)
    outerTagTagValues = countValuesByTag(outerTag, trnsxnList).keys()
    result = {}
    for value in outerTagTagValues:
        result[str(outerTag) + '=' + value] = countValuesByTag(innerTag, getTransByTagValue(outerTag, value, trnsxnList))
    return result

def sortByTagsValue(tagName, trnsxnList): #Nulls are first
    verifyInput(tagName, None, trnsxnList)
    def getKey(dictItem):
        if tagName in dictItem:
            return dictItem[tagName]
        else:
            return ''
    return sorted(trnsxnList, key=getKey)

def getTransWOTag(tagName, trnsxnList):
    verifyInput(tagName, None, trnsxnList)
    return [aTrnsxsn for aTrnsxsn in trnsxnList if tagName not in aTrnsxsn]

def getTransWOTagValue(tagName, tagValue, trnsxsnList):
    verifyInput(tagName, tagValue, trnsxsnList)
    return [aTrnsxsn for aTrnsxsn in trnsxsnList if tagName not in aTrnsxsn or aTrnsxsn[tagName] != tagValue]


def main():
    secFileName = 'secdef.dat'
    secTrans = getSecTransactions(secFileName)
    print(len(secTrans))

if __name__ == '__main__':
    main()
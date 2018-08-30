from multiprocessing import Process
from multiprocessing import Queue

def getSecTransactions(fileName):
    with open(fileName, 'r') as datFile:
        data = datFile.read()
    _output = multiProcesFormat(data)
    del data
    return _output

def multiProcesFormat(secString):
    resultQueue = Queue()
    secTransCollection = []
    secTransTemp = secString.split('\n')
    numOfProc = 10
    index = 0
    transLength = len(secTransTemp)
    step = int(transLength / numOfProc) + 1
    offset = step
    while index < transLength:
        secTransCollection.append(secTransTemp[index:offset])
        if (offset + step) > transLength:
            index = offset
            offset = transLength
        else:
            index = offset
            offset += step

    secTransCollection = []
    for i in range(5):
        secTransCollection.append(secTransTemp[:3])

    print(secTransCollection)
    procs = [Process(target=formatSecData, args=(collection, resultQueue)) for collection in secTransCollection]
    print('Number of procs: ', len(procs))
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    __rQ = []
    while not resultQueue.empty():
        __rQ.append(resultQueue.get())

    return __rQ

def formatSecData(transCollection, aQueue):
    secDataList = []
    for line in transCollection:
        secDataJSON = {}
        for tagValuePair in line.split('\x01'):
            if len(tagValuePair) > 0:
                tagValueList = tagValuePair.split('=')
                secDataJSON[int(tagValueList[0])] = tagValueList[1]
        if len(secDataJSON) > 0:
            #secDataList.append(secDataJSON)
            aQueue.put(secDataJSON)
    #aQueue.put(secDataList)

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

def getValueCountForTag(tagName, trnsxnList):
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
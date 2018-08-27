def getSecData(fileName):
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

def main():
    secFileName = 'secdef.dat'
    secData = getSecData(secFileName)
    print(len(secData))

if __name__ == '__main__':
    main()
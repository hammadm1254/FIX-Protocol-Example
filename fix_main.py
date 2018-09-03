import glob
from multiprocessing import Pool
import time
from pprint import pprint

def loadFiles(filesList):
    print("\nLoading data...\n")
    data = []
    for fileName in filesList:
        with open(fileName, 'r') as datFile:
            data += datFile.readlines()
        assert(len(data) > 0), 'Data file must be non-empty and contain valid FIX data'
    return data

def getDefsDict(defLine):
    secDataJSON = {}
    for tagValuePair in defLine.split('\x01'):
        if len(tagValuePair) > 1:
            tagValueList = tagValuePair.split('=')
            if len(tagValueList) == 2:
                secDataJSON[int(tagValueList[0])] = tagValueList[1]
    if len(secDataJSON) > 0 and 35 in secDataJSON:
        return secDataJSON
    else:
        raise TypeError('Definition type is invalid, Tag-35 not found')

def verifyInput(tagName, tagValue, defList):
    assert(type(tagName) == int or tagName is None), 'Tag names are integer values'
    assert(type(tagValue) == str or tagValue is None), 'Tag values are strings'
    assert(type(defList) == list and len(defList) > 0), 'List of transactions must not be empty'

def countDefTagValue(tagName, tagValue, defList):
    return len(getDefByTagValue(tagName, tagValue, defList))

def getDefByTagValue(tagName, tagValue, defList):
    verifyInput(tagName, tagValue, defList)
    return [definition for definition in defList if tagName in definition and definition[tagName] == tagValue]

def getDefByTag(tagName, defList):
    verifyInput(tagName, None, defList)
    return [definition for definition in defList if tagName in definition]

def countDefByTag(tagName, defList):
    verifyInput(tagName, None, defList)
    return len(getDefByTag(tagName, defList))

def countValuesByTag(tagName, defList):
    verifyInput(tagName, None, defList)
    resultDict = {}
    for definition in defList:
        if tagName in definition:
            try:
                resultDict[definition[tagName]] += 1
            except KeyError:
                resultDict[definition[tagName]] = 1
    return resultDict

def getValuesOfTag(tagName, defList):
    verifyInput(tagName, None, defList)
    return list(countValuesByTag(tagName, defList).keys())

def joinByTag(innerTag, outerTag, defList):
    verifyInput(innerTag, None, defList)
    verifyInput(outerTag, None, defList)
    outerTagTagValues = countValuesByTag(outerTag, defList).keys()
    result = {}
    for value in outerTagTagValues:
        result[str(outerTag) + '=' + value] = countValuesByTag(innerTag, getDefByTagValue(outerTag, value, defList))
    return result

def sortByTagsValue(tagName, defList): #Nulls are first
    verifyInput(tagName, None, defList)
    def getKey(dictItem):
        if tagName in dictItem:
            return dictItem[tagName]
        else:
            return ''
    return sorted(defList, key=getKey)

def getDefsExcludingTag(tagName, defList):
    verifyInput(tagName, None, defList)
    return [definition for definition in defList if tagName not in definition]

def getDefsExcludingTagValue(tagName, tagValue, defList):
    verifyInput(tagName, tagValue, defList)
    return [definition for definition in defList if tagName not in definition or definition[tagName] != tagValue]


def main():
    pool = Pool()
    secFileNames = glob.glob('*.dat')
    secFileNamesSize = len(secFileNames)
    print("Available .dat files found in directory: \n")
    for i in range(secFileNamesSize):
        print(i+1, secFileNames[i])
    inStr = input("\nPress Enter to load all files. Data from files wll be concatenated.\nElse indicate number of the file to load and press Enter: ")
    if inStr != '':
        try:
            index = int(inStr)
            if index < 1 or index > secFileNamesSize:
                raise ValueError
            else:
                index -= 1
                secFileNames = [secFileNames[index]]
        except ValueError:
            print("Input must be integer between 1 and ", secFileNamesSize, "\n")
            main()
    startLoad = time.time()
    defLines = loadFiles(secFileNames)
    loadTime = time.time() - startLoad
    startProcess = time.time()
    secDefs = list(pool.map(getDefsDict, defLines))
    processTime = time.time() - startProcess
    del defLines
    print("Load Time:", loadTime, "| Process Time:", processTime, "\n")
    del pool
    print("Question 1:")
    pprint(countValuesByTag(167, secDefs))
    print("\n")
    print("Question 2:")
    pprint(joinByTag(167, 462, secDefs))
    print("\n")
    print("Question 3:")
    pprint(getValuesOfTag(55, sortByTagsValue(200, getDefByTagValue(167, 'FUT', getDefByTagValue(6937, 'GE', getDefsExcludingTag(555, secDefs))))[:4]))
    print("\nExiting...\n")
    exit()

if __name__ == '__main__':
    main()
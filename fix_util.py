def loadFiles(filesList):
    """
    Reads the lines in the file(s) and returns a list of the lines.
    If multiple files are in a list the lines of all the files are
    contained in a single list. The files are read one by one.
    :param filesList: List of file names
    :return: List of lines in a file as strings
    """
    print("\nLoading data...\n")
    data = []
    for fileName in filesList:
        with open(fileName, 'r') as datFile:
            data += datFile.readlines()
        assert(len(data) > 0), 'Data file must be non-empty and contain valid FIX data'
    return data

def getDefsDict(defLine):
    """
    Uses line splitting to parse the lines of strings in the list
    and generate a dictionary of Key-value pairs for tags and their
    respected values.
    :param defLine: Lines of security definition data in a list
    :return: List of dictionaries of security definition with
            Tag=Key in dictionary, value of tag=value in dictionary.
    """
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
    """
    Checks the input type input variables. Throws asserts if type is mismatch
    :param tagName: Value of tag as integer
    :param tagValue: The value of a specific tag as string
    :param defList: List of dictionaries which contain security definition data
    :return: None
    """
    assert(type(tagName) == int or tagName is None), 'Tag names are integer values'
    assert(type(tagValue) == str or tagValue is None), 'Tag values are strings'
    assert(type(defList) == list and len(defList) > 0), 'List of transactions must not be empty'

def countDefTagValue(tagName, tagValue, defList):
    """
    Uses getDefByTagValue function to count how many security definition lines
    contain a specific tag/value pair
    :param tagName: Value of tag as integer
    :param tagValue: The value of a specific tag as string
    :param defList: List of dictionaries which contain security definition data
    :return: Integer value of length of list of security definition dictionary
            which contain a specific tag/value pair.
    """
    return len(getDefByTagValue(tagName, tagValue, defList))

def getDefByTagValue(tagName, tagValue, defList):
    """
    Returns the list of dictionary objects containing security definitions
    which contain a specific tag-value pair
    :param tagName: Value of tag as integer
    :param tagValue: The value of a specific tag as string
    :param defList: List of dictionaries which contain security definition data
    :return: Returns the list of dictionary objects containing security definitions
            which contain a specific tag-value pair
    """
    verifyInput(tagName, tagValue, defList)
    return [definition for definition in defList if tagName in definition and definition[tagName] == tagValue]

def getDefByTag(tagName, defList):
    """
    Returns the list of dictionary objects containing security definitions
    which contain a specific tag
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Returns the list of dictionary objects containing security definitions
            which contain a specific tag
    """
    verifyInput(tagName, None, defList)
    return [definition for definition in defList if tagName in definition]

def countDefByTag(tagName, defList):
    """
    Counts the number of security definitions which contain a specific tag
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Return an integer of the number of security definitions containing
            the specified tag
    """
    verifyInput(tagName, None, defList)
    return len(getDefByTag(tagName, defList))

def countValuesByTag(tagName, defList):
    """
    This functions generates a dictionary of all the possible values found
    in the security definitions list for a specific tag and the number of times
    they appear as the value in the dictionary
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Dictionary of tag values and their occurrences
    """
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
    """
    This function uses the countValuesByTag function to generate a set of all
    the possible tag values found in the security definitions for a specific tag
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Set of values of specific tag
    """
    verifyInput(tagName, None, defList)
    return list(countValuesByTag(tagName, defList).keys())

def joinByTag(innerTag, outerTag, defList):
    """
    This function uses countValuesByTag and getDefByTagValue functions to find the
    intersection of security definitions which contain both specified tags. The resulting
    dictionary has all possible tag values for outerTag as keys and the values for each is
    the occurrences of values of the inner tag for the specific outer tag and value as key.
    Example:
            {'462=12': {'FUT': 4994, 'MLEG': 43, 'OOF': 1312},
             '462=14': {'FUT': 3424, 'IRS': 7, 'OOF': 208},
             '462=16': {'FUT': 111868, 'OOF': 50281},
             '462=17': {'FUT': 5587, 'OOF': 34},
             '462=2': {'FUT': 10776, 'OOF': 3560},
             '462=4': {'FUT': 2890, 'OOF': 24998},
             '462=5': {'FUT': 635, 'OOF': 2178}}
    :param innerTag: Value of tag as integer
    :param outerTag: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Dictionary of occurrences of intersection tags/values
    """
    verifyInput(innerTag, None, defList)
    verifyInput(outerTag, None, defList)
    outerTagTagValues = countValuesByTag(outerTag, defList).keys()
    result = {}
    for value in outerTagTagValues:
        result[str(outerTag) + '=' + value] = countValuesByTag(innerTag, getDefByTagValue(outerTag, value, defList))
    return result

def sortByTagsValue(tagName, defList): #Nulls are first
    """
    This function sorts the security definitions list on the values of the
    specified tagName
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: Sorted security definitions list
    """
    verifyInput(tagName, None, defList)
    def getKey(dictItem):
        if tagName in dictItem:
            return dictItem[tagName]
        else:
            return ''
    return sorted(defList, key=getKey)

def getDefsExcludingTag(tagName, defList):
    """
    This function generates a list of security definitions which do not contain a
    specific tag
    :param tagName: Value of tag as integer
    :param defList: List of dictionaries which contain security definition data
    :return: List of security definitions which do not contain a
            specific tag
    """
    verifyInput(tagName, None, defList)
    return [definition for definition in defList if tagName not in definition]

def getDefsExcludingTagValue(tagName, tagValue, defList):
    """
    This function uses the getDefsExcludingTag function to generate a list of
    security definitions which do not contain the specified tag-value pair.
    :param tagName: Value of tag as integer
    :param tagValue: The value of a specific tag as string
    :param defList: List of dictionaries which contain security definition data
    :return: List of security definitions which do not contain a
            specific tag-value pair
    """
    verifyInput(tagName, tagValue, defList)
    return [definition for definition in defList if tagName not in definition or definition[tagName] != tagValue]
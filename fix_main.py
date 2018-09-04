from fix_util import *
from glob import glob
from multiprocessing import Pool
from time import time
from pprint import pprint

def main():
    """
    Main function uses glob to find *.dat files in the running program directory.
    Allows the user to select which file to work on, otherwise select all as default.
    Uses Pool() and map() to perform the generation of security definition dictionaries
    using multi-processing to speed up things.
    Prints out the answers to the 3 questions in the coding challenge using pprint to
    display dictionary objects in a legible fashion.
    :return: None
    """
    pool = Pool()
    secFileNames = glob('*.dat')
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
    startLoad = time()
    defLines = loadFiles(secFileNames)
    loadTime = time() - startLoad
    startProcess = time()
    secDefs = list(pool.map(getDefsDict, defLines))
    processTime = time() - startProcess
    del defLines
    print("Load Time:", loadTime, "| Process Time:", processTime, "\n")
    pool.close()
    print("Question 1:")
    pprint(countValuesByTag(167, secDefs))
    print("\n")
    print("Question 2:")
    pprint(joinByTag(167, 462, secDefs))
    print("\n")
    print("Question 3:")
    pprint(getValuesOfTag(55, sortByTagsValue(200, getDefByTagValue(167, 'FUT', getDefByTagValue(6937, 'GE', getDefsExcludingTag(555, secDefs))))[:4]))
    _ = input("\nPress Enter to exit...\n")
    exit()

if __name__ == '__main__':
    main()
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
    defLines = load_files(secFileNames)
    loadTime = time() - startLoad
    startProcess = time()
    secDefs = list(pool.map(get_defs_dict, defLines))
    processTime = time() - startProcess
    del defLines
    print("Load Time:", loadTime, "| Process Time:", processTime, "\n")
    pool.close()
    print("Question 1:")
    pprint(count_values_by_tag(167, secDefs))
    print("\n")
    print("Question 2:")
    pprint(join_by_tag(167, 462, secDefs))
    print("\n")
    print("Question 3:")
    pprint(get_values_of_tag(55, sort_by_tag(200, get_defs_by_tag_value(167, 'FUT', get_defs_by_tag_value(6937, 'GE', get_defs_excluding_tag(555, secDefs))))[:4]))
    _ = input("\nPress Enter to exit...\n")
    exit()

if __name__ == '__main__':
    main()
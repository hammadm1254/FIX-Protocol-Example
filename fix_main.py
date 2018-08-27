def getSecData(fileName):
    with open(fileName, 'r') as datFile:
        return datFile.read()

def main():
    secFileName = 'secdef.dat'
    secData = getSecData(secFileName)
    print(secData[:500])

if __name__ == '__main__':
    main()
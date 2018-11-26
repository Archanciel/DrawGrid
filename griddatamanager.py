import csv

class GridDataManager():
    '''
    This class reads/writes the internal grid data from/to a csv file.
    '''

    def __init__(self, filename, configManager):
        self.configMgr = configManager
        self.filename = filename

    def writeGridData(self, gridData):
        with open(self.filename, 'w', newline = '') as file:
            writer = csv.writer(file, delimiter = '\t')

            # write col header row
            csvFileHeader = [''] + [i for i in range(0, len(gridData[0]))]
            writer.writerow(csvFileHeader)

            for li in range(0, len(gridData)):
                line = [li] + gridData[li]
                writer.writerow(line)

    def readGridData(self, requiredDimX, requiredDimY):
        '''
        Loads the grid data stored in self.filename. If the input file contains less data than what is
        required to fill a grid table of dimension dimX x dimY, empty (0) cells are added to the
        data read from the input file so that a dimX x dimY matrix is returned to the caller.

        :param requiredDimX: 1 based horizontal dimension of returned grid table
        :param requiredDimY: 1 based vertical dimension of returned grid table

        :return: 2 elements tuple: first element is the 2 dimensional grid matrix (list of list) or None
                 if fileName not found.

                 Second element is None or the name of the missing file if fileName not found.
        '''
        twoDIntMatrix = []
        fileNotFoundName = None

        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file, delimiter='\t')

                # reading the header line and use it to determine the x dimension of the input data

                header = next(reader)
                dataDimX = len(header) - 1
                fillerDimX = 0

                # if fillerDimX is larger than 0, then the read data matrix col number is smaller
                # than the expected matrix x size and filler col data will have to be generated.
                # If it is smaller than 0, then the read data matrix col number is larger than the
                # expected matrix x size and will have to be truncated
                fillerDimX = requiredDimX - dataDimX

                dataDimY = 0

                for row in reader:
                    dataDimY += 1
                    if dataDimY > requiredDimY:
                        # if the number of read rows data is larger than the expected matrix y size then
                        # the excess rows are ignored
                        break
                    else:
                        intLst = [int(s) for s in row] # converting the row which contains strings into integers
                    cellDataRow = intLst[1:] # stripping off col 0 which contains line numbers
                    if fillerDimX > 0:
                        # building a filler list denoting the missing col in the read matrix data
                        fillerList = [0 for _ in range(fillerDimX)]
                    elif fillerDimX < 0:
                        # truncating the read row data to respect the required col number (x dimension)
                        cellDataRow = cellDataRow[:fillerDimX]
                        fillerList = []
                    else:
                        # read and expected col numbers are identical
                        fillerList = []
                    twoDIntMatrix.append(cellDataRow + fillerList)

                if dataDimY < requiredDimY:
                    # if the read data matrix row number is smaller than the expected matrix y size
                    # filler row data will have to be generated for each missing row
                    fillerDimY = requiredDimY - dataDimY

                    for _ in range(fillerDimY):
                        # adding a filler list for each missing row in the read matrix data
                        twoDIntMatrix.append([0 for _ in range(requiredDimX)])
        except FileNotFoundError as e:
            fileNotFoundName = e.filename
            return None, fileNotFoundName

        return twoDIntMatrix, fileNotFoundName

    def insertGridPatternToGridData(self, gridPatternMatrix, gridDataMatrix, zeroBasedInsertPosX, zeroBasedInsertPosY, doOverwrite = True):
        '''
        This method inserts the passed gridPatternMatrix in the passed gridDataMatrix at the position
        insertPosX, insertPosY. If doOverwrite is True, then the gridDataMatrix size is not changed
        and the inserted data overwrites the existing data. Else, cols and rows are added to
        gridDataMatrix to make room to the inserted data.

        :param gridPatternMatrix: 2 dimensions list
        :param gridDataMatrix: 2 dimensions list
        :param zeroBasedInsertPosX: integer
        :param zeroBasedInsertPosY: integer
        :param doOverwrite: boolean

        :return: the modified gridDataMatrix (or a copy ?)
        '''
        pass

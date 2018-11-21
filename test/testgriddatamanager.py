import unittest
import os,sys,inspect
import csv
from io import StringIO

DUMMY_HEADER = ["DUMMY HEADER 1", "DUMMY HEADER 2"]

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from griddatamanager import GridDataManager

class TestGridDataManager(unittest.TestCase):#

    def testWriteGridData(self):
        '''
        This test case ensures that the grid data are written into the csv file with a column title
        line as well as with a 0 index column storing the 0 based line index.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        with open(csvFileName, 'r') as file:
            reader = csv.reader(file, delimiter='\t')

            # reading the header line and use it to determine the x dimension of the input data

            header = next(reader)
            self.assertEqual(['','0','1','2','3'], header)

            self.assertEqual(['0','1','1','0','0'], next(reader), 'csv matrix data line 0')
            self.assertEqual(['1','1','0','1','1'], next(reader), 'csv matrix data line 1')
            self.assertEqual(['2','0','0','1','1'], next(reader), 'csv matrix data line 2')
            self.assertEqual(['3','1','1','1','1'], next(reader), 'csv matrix data line 3')


        os.remove(csvFileName)

    def testReadGridDataSquareMatrix(self):
        '''
        This test case ensures that when reading a matrix data csv file whose first line is the
        column title line and the first column the line index, the returned data matrix contains
        only the data, neither the column title line nor the first line index column. Here, a square
        matrix is read
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=4, requiredDimY=4)

        self.assertEqual([[1, 1, 0, 0],[1, 0, 1, 1],[0, 0, 1, 1],[1, 1, 1, 1]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadGridDataRectangularMatrix(self):
        '''
        This test case ensures that when reading a matrix data csv file whose first line is the
        column title line and the first column the line index, the returned data matrix contains
        only the data, neither the column title line nor the first line index column. Here, a rectangular
        matrix is read
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=4, requiredDimY=3)

        self.assertEqual([[1, 1, 0, 0],[1, 0, 1, 1],[0, 0, 1, 1]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataSquareMatrix1MissingRow1MissingCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a square matrix is handled with only 1 missing row and 1 missing column.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=5, requiredDimY=5)

        self.assertEqual([[1, 1, 0, 0, 0],[1, 0, 1, 1, 0],[0, 0, 1, 1, 0],[1, 1, 1, 1, 0],[0, 0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooLargeGridDataSquareMatrix1ExcessRow1ExcessCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix larger than the expected size, the excess data is wiped out. Here, a 4 x 4 square matrix
        is read and a 3 x 3 matrix is returned.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=3, requiredDimY=3)

        self.assertEqual([[1, 1, 0],[1, 0, 1],[0, 0, 1]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooLargeGridDataSquareMatrix2ExcessRow2ExcessCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix larger than the expected size, the excess data is wiped out. Here, a 4 x 4 square matrix
        is read and a 2 x 2 matrix is returned.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=2, requiredDimY=2)

        self.assertEqual([[1, 1],[1, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataSquareMatrix2MissingRow2MissingCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a square matrix is handled with 2 missing rows and 2 missing columns.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=6, requiredDimY=6)

        self.assertEqual([[1, 1, 0, 0, 0, 0],[1, 0, 1, 1, 0, 0],[0, 0, 1, 1, 0, 0],[1, 1, 1, 1, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular4x3Matrix1MissingRow2MissingCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 4 x 3 matrix is handled with returning a 5 x 5 square matrix, i.e.
        1 missing rows and 2 missing columns.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0],
                    [1, 0, 1],
                    [0, 0, 1],
                    [1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=5, requiredDimY=5)

        self.assertEqual([[1, 1, 0, 0, 0],[1, 0, 1, 0, 0],[0, 0, 1, 0, 0],[1, 1, 1, 0, 0],[0, 0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooLargeGridDataRectangular4x3Matrix1ExcessRow2ExcessCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix larger than the expected size, the excess data are ignored. Here, a rectangular 4 x 3
        matrix is handled with returning a 3 x 1 rectangular matrix, i.e. 1 excess rows and 2 excess
        columns
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0],
                    [1, 0, 1],
                    [0, 0, 1],
                    [1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=3, requiredDimY=1)

        self.assertEqual([[1, 1, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooLargeGridDataRectangular4x3Matrix2ExcessRow1ExcessCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix larger than the expected size, the excess data are ignored. Here, a rectangular 4 x 3
        matrix is handled with returning a 2 x 2 square matrix, i.e. 2 excess rows and 1 excess columns
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0],
                    [1, 0, 1],
                    [0, 0, 1],
                    [1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=2, requiredDimY=2)

        self.assertEqual([[1, 1], [1, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular3x4Matrix2MissingRow1MissingCol(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 3 x 4 matrix is handled with returning a 5 x 5 square matrix, i.e.
        2 missing rows and 1 missing columns.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 1],
                    [1, 0, 1, 1],
                    [0, 0, 1, 0]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=5, requiredDimY=5)

        self.assertEqual([[1, 1, 0, 1, 0],[1, 0, 1, 1, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular4x3Matrix(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 4 x 3 matrix is handled with only 1 missing row and 1 missing
        column.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0],
                    [1, 0, 1],
                    [0, 0, 1],
                    [1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=4, requiredDimY=5)

        self.assertEqual([[1, 1, 0, 0],[1, 0, 1, 0],[0, 0, 1, 0],[1, 1, 1, 0],[0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular3x4Matrix(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 3 x 4 matrix is handled with only 1 missing row and 1 missing column.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=5, requiredDimY=4)

        self.assertEqual([[1, 1, 0, 0, 0],[1, 0, 1, 1, 0],[1, 1, 1, 1, 0],[0, 0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular3x4MatrixOnly2columnsMissing(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 3 x 4 matrix is handled with 0 missing row and 2 missing columns.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=6, requiredDimY=3)

        self.assertEqual([[1, 1, 0, 0, 0, 0],[1, 0, 1, 1, 0, 0],[1, 1, 1, 1, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

    def testReadTooSmallGridDataRectangular3x4MatrixOnly2RowsMissing(self):
        '''
        This test case ensures that when reading a matrix data csv file which contains data denoting
        a matrix smaller than the expected size, the missing data are completed with 0 values to fill
        the gap. Here, a rectangular 3 x 4 matrix is handled with 2 missing row and no missing column.
        '''
        csvFileName = "test.csv"
        gridDataMgr = GridDataManager(csvFileName)
        gridData = [[1, 1, 0, 0],
                    [1, 0, 1, 1],
                    [1, 1, 1, 1]]
        gridDataMgr.writeGridData(gridData)

        gridDataMgr = GridDataManager(csvFileName)
        gridData, fileNotFoundName = gridDataMgr.readGridData(requiredDimX=4, requiredDimY=5)

        self.assertEqual([[1, 1, 0, 0],[1, 0, 1, 1],[1, 1, 1, 1],[0, 0, 0, 0],[0, 0, 0, 0]], gridData)
        self.assertIsNone(fileNotFoundName)

        os.remove(csvFileName)

if __name__ == '__main__':
    unittest.main()
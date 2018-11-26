import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            self.filePath = '/sdcard/gridview_test.ini'
        else:
            self.filePath = 'c:\\temp\\gridview_test.ini'


    def testConfigurationManagerInstanciation(self):
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.windowTitle, 'Draw grid')
        self.assertEqual(self.configMgr.windowLocation, '400, 20')
        self.assertEqual(self.configMgr.gridWidth, '791')
        self.assertEqual(self.configMgr.fps, '20')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, 'Half')
            self.assertEqual(self.configMgr.defaultCellSize, '35')
        else:
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, '1, 0')
            self.assertEqual(self.configMgr.defaultCellSize, '15')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, 'griddata.csv')
        self.assertEqual(self.configMgr.activeCellColor, '0, 255, 0')
        self.assertEqual(self.configMgr.gridCoordMarginHideCellSizeLimit, '11')
        self.assertEqual(self.configMgr.gridCoordMarginSize, '20')
        self.assertEqual(self.configMgr.gridAxisFontSize, '12')
        self.assertEqual(self.configMgr.gridMoveIncrement, '1')


    def testConfigurationManagerInstanciationNoConfigFile(self):
        os.remove(self.filePath)
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.windowTitle, 'Draw grid')
        self.assertEqual(self.configMgr.windowLocation, '400, 20')
        self.assertEqual(self.configMgr.gridWidth, '791')
        self.assertEqual(self.configMgr.fps, '20')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, 'Half')
            self.assertEqual(self.configMgr.defaultCellSize, '35')
        else:
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, '1, 0')
            self.assertEqual(self.configMgr.defaultCellSize, '15')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, 'griddata.csv')
        self.assertEqual(self.configMgr.activeCellColor, '0, 255, 0')
        self.assertEqual(self.configMgr.gridCoordMarginHideCellSizeLimit, '11')
        self.assertEqual(self.configMgr.gridCoordMarginSize, '20')
        self.assertEqual(self.configMgr.gridAxisFontSize, '12')
        self.assertEqual(self.configMgr.gridMoveIncrement, '1')


    def testConfigurationManagerInstanciationEmptyConfigFile(self):
        open(self.filePath, 'w').close()
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.windowTitle, 'Draw grid')
        self.assertEqual(self.configMgr.windowLocation, '400, 20')
        self.assertEqual(self.configMgr.gridWidth, '791')
        self.assertEqual(self.configMgr.fps, '20')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, 'Half')
            self.assertEqual(self.configMgr.defaultCellSize, '35')
        else:
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, '1, 0')
            self.assertEqual(self.configMgr.defaultCellSize, '15')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, 'griddata.csv')
        self.assertEqual(self.configMgr.activeCellColor, '0, 255, 0')
        self.assertEqual(self.configMgr.gridCoordMarginHideCellSizeLimit, '11')
        self.assertEqual(self.configMgr.gridCoordMarginSize, '20')
        self.assertEqual(self.configMgr.gridAxisFontSize, '12')
        self.assertEqual(self.configMgr.gridMoveIncrement, '1')


    def testConfigurationManagerInstanciationOneMissingKey(self):
        #removing second line in config file
        with open(self.filePath, 'r') as configFile:
            lines = configFile.readlines()

        with open(self.filePath, 'w') as configFile:
            # first line contains [General] section name !
            configFile.write(''.join(lines[0:1] + lines[2:]))

        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.windowTitle, 'Draw grid')
        self.assertEqual(self.configMgr.windowLocation, '400, 20')
        self.assertEqual(self.configMgr.gridWidth, '791')

        if os.name == 'posix':
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, 'Half')
            self.assertEqual(self.configMgr.defaultCellSize, '35')
        else:
            self.assertEqual(self.configMgr.gridWidth, '791')
            self.assertEqual(self.configMgr.gridHeight, '791')
            self.assertEqual(self.configMgr.gridLineWidthTuple, '1, 0')
            self.assertEqual(self.configMgr.defaultCellSize, '15')

        self.assertEqual(self.configMgr.loadAtStartPathFilename, 'griddata.csv')
        self.assertEqual(self.configMgr.activeCellColor, '0, 255, 0')
        self.assertEqual(self.configMgr.gridCoordMarginHideCellSizeLimit, '11')
        self.assertEqual(self.configMgr.gridCoordMarginSize, '20')
        self.assertEqual(self.configMgr.gridAxisFontSize, '12')
        self.assertEqual(self.configMgr.gridMoveIncrement, '1')


if __name__ == '__main__':
    unittest.main()

import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import pygame as pg

from configurationmanager import ConfigurationManager
from gridview import GridView


class TestGridView(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGridView, self).__init__(*args, **kwargs)
        if os.name == 'posix':
            self.configFilePath = '/sdcard/gridview_test.ini'
        else:
            self.configFilePath = 'TestGridView_config.ini'

        configMgr = ConfigurationManager(self.configFilePath)

        # setting Pygame window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = configMgr.windowLocation

        pg.init()
        self.screen = pg.display.set_mode((configMgr.gridWidth, configMgr.gridHeight))
        pg.display.set_caption(configMgr.windowTitle)
        self.clock = pg.time.Clock()

    def testLoadGridData(self):
        '''
        Ensures None is returned by GridView.loadGridData() if the grid data csv file specified in
        the config ini file was found.
        '''
        # instanciating a ConfigurationManager on the general TestGridView config ini file
        configMgr = ConfigurationManager(self.configFilePath)

        gridView = GridView(surface=self.screen, configManager=configMgr)
        fileNotFoundName = gridView.loadGridData()

        self.assertIsNone(fileNotFoundName)

    def testLoadGridDataFileNotFound(self):
        '''
        Ensures the missing file name is returned by GridView.loadGridData() if the grid data csv file
        specified in the config ini file was not found.
        '''
        # instanciating a ConfigurationManager on a test case specific config ini file
        configMgr = ConfigurationManager('testLoadGridDataFileNotFound_config.ini')

        gridView = GridView(surface=self.screen, configManager=configMgr)
        fileNotFoundName = gridView.loadGridData()

        self.assertEqual(fileNotFoundName, 'gridview_test_griddata_not_exist.csv')


if __name__ == '__main__':
    unittest.main()

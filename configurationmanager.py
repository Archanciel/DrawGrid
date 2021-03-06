import os
from configobj import ConfigObj

class ConfigurationManager:
    # those constants are used outside of ConfigurationManager. For this reason,
    # they are declared inside the class

    CONFIG_SECTION_VIEW_LAYOUT = 'View layout'

    # view options/settings

    CONFIG_KEY_WINDOW_TITLE = "Window title"
    DEFAULT_WINDOW_TITLE = "Draw grid"

    CONFIG_KEY_WINDOW_LOCATION = "Window location"  # 400 enables to read output in Pycharm console window !
    DEFAULT_WINDOW_LOCATION = "400, 20"  # 400 enables to read output in Pycharm console window !

    CONFIG_KEY_GRID_WIDTH = "Grid width"  # grid is always a square !
    DEFAULT_GRID_WIDTH_ANDROID = "791"  # grid is always a square !
    DEFAULT_GRID_WIDTH_WINDOWS = "791"  # grid is always a square !

    CONFIG_KEY_GRID_HEIGHT = "Grid height"  # grid is always a square !
    DEFAULT_GRID_HEIGHT_ANDROID = "791"  # grid is always a square !
    DEFAULT_GRID_HEIGHT_WINDOWS = "791"  # grid is always a square !

    CONFIG_KEY_FPS = "Frames per second (FPS)"
    DEFAULT_FPS = "20"

    CONFIG_SECTION_GRID_LAYOUT = "Grid layout"

    # color constants
    CONFIG_KEY_ACTIVE_CELL_COLOR = "Active cell color"
    DEFAULT_ACTIVE_CELL_COLOR = "0, 255, 0"

    # grid constants

    CONFIG_KEY_GRID_LINE_WIDTH_TUPLE = "Grid line width tuple"
    DEFAULT_GRID_LINE_WIDTH_TUPLE = "1, 0"
    # GRID_LINE_WIDTH_TUPLE = (2, 0)
    # GRID_LINE_WIDTH_TUPLE = (3, 1)
    # GRID_LINE_WIDTH_TUPLE = (4, 1)
    # GRID_LINE_WIDTH_TUPLE = (5, 2)
    # GRID_LINE_WIDTH_TUPLE = (6, 2)
    # GRID_LINE_WIDTH_TUPLE = (7, 3)
    # GRID_LINE_WIDTH_TUPLE = (8, 3)

    #    GRID_LINE_WIDTH = GRID_LINE_WIDTH_TUPLE[0]
    #    CELL_SIZE_OFFSET = GRID_LINE_WIDTH_TUPLE[1] # constant used when drawing an active cell to correct an unexplained
    # error which introduce blank pixels at top and left of the drawned
    # rectangle when the grid line width is bigger than 2 !

    CONFIG_KEY_CELL_SIZE = "Default cell size"

    DEFAULT_CELL_SIZE_WINDOWS = "15"
    DEFAULT_CELL_SIZE_ANDROID = "35"

    CONFIG_KEY_GRID_LINE_WIDTH_TUPLE_FULL = "Grid line width tuple"
    DEFAULT_GRID_LINE_WIDTH_TUPLE_FULL = "1, 0"

    # Since one cell can occupy a minimum of 1 px and the grid line width
    # is 1 px at the minimum, 2 cells will require at least 1 + 1 + 1 + 1 + 1 = 5 px.
    # 3 cells require at least 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
    # n cells require at least 1 + (n * 2) px. This explains that the smallest possible
    # cell constant SMALLEST_CELL_REQUIRED_PX_NUMBER is 2 pixels. This constant is not
    # settable in the .ini file.
    SMALLEST_CELL_REQUIRED_PX_NUMBER = 2

    # Cell size under which the grid axis label zone is no longer displayed
    CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT = "Grid coord margin hide cell size limit"
    DEFAULT_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT = '11'

    CONFIG_KEY_GRID_COORD_MARGIN_SIZE = 'Grid coord margin size'  # 20 Windows, 40 Android
    DEFAULT_GRID_COORD_MARGIN_SIZE = '20'  # 20 Windows, 40 Android

    CONFIG_KEY_GRID_AXIS_FONT_SIZE = 'Grid axis font size'
    DEFAULT_GRID_AXIS_FONT_SIZE = '12'

    CONFIG_KEY_GRID_MOVE_INCREMENT = 'Grid move increment'
    DEFAULT_GRID_MOVE_INCREMENT = '1'

    CONFIG_KEY_LOAD_AT_START_PATH_FILENAME = 'loadatstartpathfilename'
    DEFAULT_LOAD_AT_START_PATH_FILENAME = 'griddata.csv'

    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self._updated = False

        if len(self.config) == 0:
            self._setAndStoreDefaultConf()

        try:
            self.__windowTitle = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_TITLE]
        except KeyError:
            self.__windowTitle = self.DEFAULT_WINDOW_TITLE
            self._updated = True
    
        try:
            self.__windowLocation = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_LOCATION]
        except KeyError:
            self.__windowLocation = self.DEFAULT_WINDOW_LOCATION
            self._updated = True

        try:
            self.__gridWidth = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_WIDTH]
        except KeyError:
            if os.name == 'posix':
                self.__gridWidth = self.DEFAULT_GRID_WIDTH_ANDROID
            else:
                self.__gridWidth = self.DEFAULT_GRID_WIDTH_WINDOWS
            self._updated = True

        try:
            self.__gridHeight = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_HEIGHT]
        except KeyError:
            if os.name == 'posix':
                self.__gridHeight = self.DEFAULT_GRID_HEIGHT_ANDROID
            else:
                self.__gridHeight = self.DEFAULT_GRID_HEIGHT_WINDOWS
                
            self._updated = True
        try:
            self.__fps = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_FPS]
        except KeyError:
            self.__fps = self.DEFAULT_FPS
            self._updated = True

        try:
            self.__gridCoordMarginHideCellSizeLimit = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT]
        except KeyError:
            self.__gridCoordMarginHideCellSizeLimit = self.DEFAULT_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT
            self._updated = True

        try:
            self.__gridCoordMarginSize = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_COORD_MARGIN_SIZE]
        except KeyError:
            self.__gridCoordMarginSize = self.DEFAULT_GRID_COORD_MARGIN_SIZE
            self._updated = True

        try:
            self.__gridAxisFontSize = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_AXIS_FONT_SIZE]
        except KeyError:
            self.__gridAxisFontSize = self.DEFAULT_GRID_AXIS_FONT_SIZE
            self._updated = True

        try:
            self.__gridMoveIncrement = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_MOVE_INCREMENT]
        except KeyError:
            self.__gridMoveIncrement = self.DEFAULT_GRID_MOVE_INCREMENT
            self._updated = True

        try:
            self.__activeCellColor = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_ACTIVE_CELL_COLOR]
        except KeyError:
            self.__activeCellColor = self.DEFAULT_ACTIVE_CELL_COLOR
            self._updated = True

        try:
            self.__gridLineWidthTuple = self.config[self.CONFIG_SECTION_GRID_LAYOUT][
                self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE]
        except KeyError:
            self.__gridLineWidthTuple = self.DEFAULT_GRID_LINE_WIDTH_TUPLE
            self._updated = True

        try:
            self.__defaultCellSize = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_CELL_SIZE]
        except KeyError:
            if os.name == 'posix':
                self.__defaultCellSize = self.DEFAULT_CELL_SIZE_ANDROID
            else:
                self.__defaultCellSize = self.DEFAULT_CELL_SIZE_WINDOWS
            self._updated = True

        try:
            self.__loadAtStartPathFilename = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME]
        except KeyError:
            self.__loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
            self._updated = True


        self.storeConfig() #will save config file in case one config key raised an exception


    def _setAndStoreDefaultConf(self):
        '''
        In case no config file exists or if config file is empty,
        defines default values for config properties. Then creates
        or updates the config file.
        :return: nothing
        '''
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT] = {}
        self.config[self.CONFIG_SECTION_GRID_LAYOUT] = {}
        self.windowTitle = self.DEFAULT_WINDOW_TITLE
        self.windowLocation = self.DEFAULT_WINDOW_LOCATION
        self.gridWidth = self.DEFAULT_GRID_WIDTH_WINDOWS
        self.gridLineWidthTuple = self.DEFAULT_GRID_LINE_WIDTH_TUPLE

        if os.name == 'posix':
            self.gridWidth = self.DEFAULT_GRID_WIDTH_ANDROID
            self.gridHeight = self.DEFAULT_GRID_HEIGHT_ANDROID
            self.defaultCellSize = self.DEFAULT_CELL_SIZE_ANDROID
        else:
            self.gridWidth = self.DEFAULT_GRID_WIDTH_WINDOWS
            self.gridHeight = self.DEFAULT_GRID_HEIGHT_WINDOWS
            self.defaultCellSize = self.DEFAULT_CELL_SIZE_WINDOWS

        self.activeCellColor = self.DEFAULT_ACTIVE_CELL_COLOR
        self.loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
        self.fps = self.DEFAULT_FPS
        self.gridCoordMarginHideCellSizeLimit = self.DEFAULT_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT
        self.gridCoordMarginSize = self.DEFAULT_GRID_COORD_MARGIN_SIZE
        self.gridAxisFontSize = self.DEFAULT_GRID_AXIS_FONT_SIZE
        self.gridMoveIncrement = self.DEFAULT_GRID_MOVE_INCREMENT
        self._updated = True

        self.storeConfig()


    @property
    def windowTitle(self):
        return self.__windowTitle

    @windowTitle.setter
    def windowTitle(self, timezoneStr):
        self.__windowTitle = timezoneStr
        self._updated = True


    @property
    def windowLocation(self):
        return self.__windowLocation

    @windowLocation.setter
    def windowLocation(self, windowLocationStr):
        self.__windowLocation = windowLocationStr
        self._updated = True


    @property
    def gridWidth(self):
        return int(self.__gridWidth)

    @gridWidth.setter
    def gridWidth(self, gridWidthStr):
        self.__gridWidth = gridWidthStr
        self._updated = True


    @property
    def gridHeight(self):
        return int(self.__gridHeight)

    @gridHeight.setter
    def gridHeight(self, gridHeightStr):
        self.__gridHeight = gridHeightStr
        self._updated = True


    @property
    def loadAtStartPathFilename(self):
        return self.__loadAtStartPathFilename

    @loadAtStartPathFilename.setter
    def loadAtStartPathFilename(self, loadAtStartPathFilenameStr):
        self.__loadAtStartPathFilename = loadAtStartPathFilenameStr
        self._updated = True


    @property
    def fps(self):
        return int(self.__fps)

    @fps.setter
    def fps(self, fpsStr):
        self.__fps = fpsStr
        self._updated = True


    @property
    def activeCellColor(self):
        colorRGB = self.__activeCellColor.split(',')
        return int(colorRGB[0]), int(colorRGB[1]), int(colorRGB[2])

    @activeCellColor.setter
    def activeCellColor(self, activeCellColorStr):
        self.__activeCellColor = activeCellColorStr
        self._updated = True


    @property
    def gridLineWidth(self):
        '''
        Returns first component of grid line width tuple as integer.
        '''
        return self.gridLineWidthTuple[0]

    @property
    def cellSizeOffset(self):
        '''
        Returns second component of grid line width tuple as integer.

        The second value in the tuple is a constant used when drawing an active cell to correct
        an unexplained error which introduce blank pixels at top and left of the drawned
        rectangle when the grid line width is bigger than 2 !
        '''
        return self.gridLineWidthTuple[1]

    @property
    def gridLineWidthTuple(self):
        '''
        Possible values for Grid line width tuple:
        "1, 0", "2, 0", "3, 1", "4, 1", "5, 2", "6, 2", "7, 3", "8, 3"
        The second value in the tuple is a constant used when drawing an active cell to correct
        an unexplained error which introduce blank pixels at top and left of the drawned
        rectangle when the grid line width is bigger than 2 !

        :return: 2 integers tuple
        '''
        tupleData = self.__gridLineWidthTuple.split(',')
        return int(tupleData[0]), int(tupleData[1])

    @gridLineWidthTuple.setter
    def gridLineWidthTuple(self, gridLineWidthTupleStr):
        self.__gridLineWidthTuple = gridLineWidthTupleStr
        self._updated = True


    @property
    def defaultCellSize(self):
        return int(self.__defaultCellSize)

    @defaultCellSize.setter
    def defaultCellSize(self, defaultCellSizeStr):
        self.__defaultCellSize = defaultCellSizeStr
        self._updated = True


    @property
    def gridCoordMarginHideCellSizeLimit(self):
        return int(self.__gridCoordMarginHideCellSizeLimit)

    @gridCoordMarginHideCellSizeLimit.setter
    def gridCoordMarginHideCellSizeLimit(self, gridCoordMarginHideCellSizeLimitStr):
        self.__gridCoordMarginHideCellSizeLimit = gridCoordMarginHideCellSizeLimitStr
        self._updated = True


    @property
    def gridCoordMarginSize(self):
        return int(self.__gridCoordMarginSize)

    @gridCoordMarginSize.setter
    def gridCoordMarginSize(self, gridCoordMarginSizeStr):
        self.__gridCoordMarginSize = gridCoordMarginSizeStr
        self._updated = True


    @property
    def gridAxisFontSize(self):
        return int(self.__gridAxisFontSize)

    @gridAxisFontSize.setter
    def gridAxisFontSize(self, gridAxisFontSizeStr):
        self.__gridAxisFontSize = gridAxisFontSizeStr
        self._updated = True


    @property
    def gridMoveIncrement(self):
        return int(self.__gridMoveIncrement)

    @gridMoveIncrement.setter
    def gridMoveIncrement(self, gridMoveIncrementStr):
        self.__gridMoveIncrement = gridMoveIncrementStr
        self._updated = True


    def storeConfig(self):
        if not self._updated:
            return

        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_ACTIVE_CELL_COLOR] = self.__activeCellColor
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE] = self.__gridLineWidthTuple
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_CELL_SIZE] = self.__defaultCellSize
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.__loadAtStartPathFilename
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_TITLE] = self.__windowTitle
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_LOCATION] = self.__windowLocation
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_WIDTH] = self.__gridWidth
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_HEIGHT] = self.__gridHeight
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_FPS] = self.__fps
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT] = self.__gridCoordMarginHideCellSizeLimit
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_COORD_MARGIN_SIZE] = self.__gridCoordMarginSize
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_AXIS_FONT_SIZE] = self.__gridAxisFontSize
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_MOVE_INCREMENT] = self.__gridMoveIncrement

        self.addCommentsToIniFile()

        self.config.write()
        
        self._updated = False

    def addCommentsToIniFile(self):
        '''
        This method fills the comments and inline_comments dictionaries of the ConfigObj sections.
        It ensures that if an entry is added to one of the two dictionaries, it is added to the other
        one. If this rule is violated, the ConfigObj.write() method raises a KeyError exception.
        '''

        # add comments before each parm in the view layout section
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT].comments = {
            self.CONFIG_KEY_WINDOW_TITLE: ["",""],
            self.CONFIG_KEY_WINDOW_LOCATION: [""],
            self.CONFIG_KEY_GRID_WIDTH: [""],
            self.CONFIG_KEY_GRID_HEIGHT: [""],
            self.CONFIG_KEY_FPS: [""],
            self.CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT: ["",
                                                               self.CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT + " explanation:",
                                                               "Specifies under what cell size the grid view coord horizontal and",
                                                               "vertical margin showing the cell x y coordinates are hidden. This",
                                                               "value is used when zooming in or out"],
            self.CONFIG_KEY_GRID_COORD_MARGIN_SIZE: [""],
            self.CONFIG_KEY_GRID_AXIS_FONT_SIZE: [""],
            self.CONFIG_KEY_GRID_MOVE_INCREMENT: [""],
        }

        # add inline comments for each parm in the view layout section
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT].inline_comments = {
            self.CONFIG_KEY_WINDOW_TITLE: None,
            self.CONFIG_KEY_WINDOW_LOCATION: "value in pixel(s)",
            self.CONFIG_KEY_GRID_WIDTH: "value in pixel(s)",
            self.CONFIG_KEY_GRID_HEIGHT: "value in pixel(s)",
            self.CONFIG_KEY_FPS: None,
            self.CONFIG_KEY_COORD_MARGIN_HIDE_CELL_SIZE_LIMIT: "value in pixel(s)",
            self.CONFIG_KEY_GRID_COORD_MARGIN_SIZE: "value in pixel(s)",
            self.CONFIG_KEY_GRID_AXIS_FONT_SIZE: None,
            self.CONFIG_KEY_GRID_MOVE_INCREMENT: "value in pixel(s)",
        }

        # add empty comment before grid layout section which translates into a blank line before the section tag
        self.config.comments[self.CONFIG_SECTION_GRID_LAYOUT] = [""]

        # add comments before each parm in the grid layout section
        self.config[self.CONFIG_SECTION_GRID_LAYOUT].comments = {
            self.CONFIG_KEY_CELL_SIZE: ["",
                                        self.CONFIG_KEY_CELL_SIZE + " explanation:",
                                        "Since one cell can occupy a minimum of 1 px and the grid line width",
                                        "is 1 px at the minimum, 2 cells will require at least 1 + 1 + 1 + 1 + 1 = 5 px.",
                                        "3 cells require at least 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.",
                                        "n cells require at least 1 + (n * 2) px. This explains that the smallest possible",
                                        "cell constant SMALLEST_CELL_REQUIRED_PX_NUMBER is 2 pixels."],
            self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE:
                ["",
                 "Other possible values for " + self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE + ":",
                 "\"2, 0\", \"3, 1\", \"4, 1\", \"5, 2\", \"6, 2\", \"7, 3\", \"8, 3\"",
                 "The second value in the tuple is a constant used when drawing an active cell to correct",
                 "an unexplained error which introduce blank pixels at top and left of the drawned",
                 "rectangle when the grid line width is bigger than 2 !"],
            self.CONFIG_KEY_ACTIVE_CELL_COLOR: ["",
                                                self.CONFIG_KEY_ACTIVE_CELL_COLOR + " alternatives:",
                                                "WHITE = (255, 255, 255)",
                                                "BLACK = (0, 0, 0)",
                                                "RED = (255, 0, 0)",
                                                "GREEN = (0, 255, 0)",
                                                "BLUE = (0, 0, 255)",
                                                "YELLOW = (255, 255, 0)"],
            self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME: [""],
        }

        # add inline comments for each parm in the grid layout section
        self.config[self.CONFIG_SECTION_GRID_LAYOUT].inline_comments = {
            self.CONFIG_KEY_CELL_SIZE: "value in pixels. On Windows: 15, on Android: 35",
            self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE: "value in pixel(s)",
            self.CONFIG_KEY_ACTIVE_CELL_COLOR: None,
            self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME: None,
        }


if __name__ == '__main__':
    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'
        
    cm = ConfigurationManager(FILE_PATH)
    print(cm.windowTitle)
    print(cm.windowLocation)
    print(cm.gridWidth)
    print(cm.gridHeight)
    print("loadAtStartPathFilename: '" + cm.loadAtStartPathFilename + "'")
    import pytz
    print(sorted(pytz.all_timezones_set))

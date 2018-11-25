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
    CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT = "Grid axis hide cell size limit"
    DEFAULT_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT = '11'

    GRID_COORD_MARGIN_SIZE = '20'  # 20 Windows, 40 Android
    GRID_AXIS_FONT_SIZE = '12'

    GRID_MOVE_INCREMENT = '1'

    DEFAULT_DATA_PATH_IOS = '~/Documents'

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
            self.__axisLegendHideCellSizeLimit = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT]
        except KeyError:
            self.__axisLegendHideCellSizeLimit = self.DEFAULT_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT
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
        self.axisLegendHideCellSizeLimit = self.DEFAULT_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT
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
        return self.__gridWidth

    @gridWidth.setter
    def gridWidth(self, gridWidthStr):
        self.__gridWidth = gridWidthStr
        self._updated = True


    @property
    def gridHeight(self):
        return self.__gridHeight

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
        return self.__fps

    @fps.setter
    def fps(self, fpsStr):
        self.__fps = fpsStr
        self._updated = True


    @property
    def activeCellColor(self):
        return self.__activeCellColor

    @activeCellColor.setter
    def activeCellColor(self, activeCellColorStr):
        self.__activeCellColor = activeCellColorStr
        self._updated = True


    @property
    def gridLineWidthTuple(self):
        return self.__gridLineWidthTuple

    @gridLineWidthTuple.setter
    def gridLineWidthTuple(self, gridLineWidthTupleStr):
        self.__gridLineWidthTuple = gridLineWidthTupleStr
        self._updated = True


    @property
    def defaultCellSize(self):
        return self.__defaultCellSize

    @defaultCellSize.setter
    def defaultCellSize(self, defaultCellSizeStr):
        self.__defaultCellSize = defaultCellSizeStr
        self._updated = True


    @property
    def axisLegendHideCellSizeLimit(self):
        return self.__axisLegendHideCellSizeLimit

    @axisLegendHideCellSizeLimit.setter
    def axisLegendHideCellSizeLimit(self, axisLegendHideCellSizeLimitStr):
        self.__axisLegendHideCellSizeLimit = axisLegendHideCellSizeLimitStr
        self._updated = True


    def storeConfig(self):
        if not self._updated:
            return

        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_ACTIVE_CELL_COLOR] = self.activeCellColor
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE] = self.gridLineWidthTuple
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_CELL_SIZE] = self.defaultCellSize
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.loadAtStartPathFilename
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_TITLE] = self.windowTitle
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_LOCATION] = self.windowLocation
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_WIDTH] = self.gridWidth
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_HEIGHT] = self.gridHeight
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_FPS] = self.fps
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT] = self.axisLegendHideCellSizeLimit

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
            self.CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT: ["",
                                                               self.CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT + " explanation:",
                                                               "Specifies under what cell size the grid view axis labels showing",
                                                               "the cell x y coordinates are hidden. This value is used when zooming",
                                                               "in or out"],
        }

        # add inline comments for each parm in the view layout section
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT].inline_comments = {
            self.CONFIG_KEY_WINDOW_TITLE: None,
            self.CONFIG_KEY_WINDOW_LOCATION: None,
            self.CONFIG_KEY_GRID_WIDTH: None,
            self.CONFIG_KEY_GRID_HEIGHT: None,
            self.CONFIG_KEY_FPS: None,
            self.CONFIG_KEY_AXIS_LEGEND_HIDE_CELL_SIZE_LIMIT: None,
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
                 "(2, 0), (3, 1), (4, 1), (5, 2), (6, 2), (7, 3), (8, 3)",
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
            self.CONFIG_KEY_CELL_SIZE: "on Windows: 15, on Android: 35",
            self.CONFIG_KEY_GRID_LINE_WIDTH_TUPLE: None,
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

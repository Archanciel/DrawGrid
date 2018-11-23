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

    GRID_LINE_WIDTH_TUPLE = (1, 0)
    # GRID_LINE_WIDTH_TUPLE = (2, 0)
    # GRID_LINE_WIDTH_TUPLE = (3, 1)
    # GRID_LINE_WIDTH_TUPLE = (4, 1)
    # GRID_LINE_WIDTH_TUPLE = (5, 2)
    # GRID_LINE_WIDTH_TUPLE = (6, 2)
    # GRID_LINE_WIDTH_TUPLE = (7, 3)
    # GRID_LINE_WIDTH_TUPLE = (8, 3)

    GRID_LINE_WIDTH = GRID_LINE_WIDTH_TUPLE[0]
    CELL_SIZE_OFFSET = GRID_LINE_WIDTH_TUPLE[1] # constant used when drawing an active cell to correct an unexplained
                                                # error which introduce blank pixels at top and left of the drawned
                                                # rectangle when the grid line width is bigger than 2 !

    DEFAULT_CELL_SIZE = 15  # 15 Windows, 35 Android

    # Since one cell can occupy a minimum of 1 px and the grid line width
    # is 1 px at the minimum, 2 cells will require at least 1 + 1 + 1 + 1 + 1 = 5 px.
    # 3 cells require at least 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
    # n cells require at least 1 + (n * 2) px. This explains that the smallest possible
    # cell constant SMALLEST_CELL_REQUIRED_PX_NUMBER is 2 pixels.
    SMALLEST_CELL_REQUIRED_PX_NUMBER = 2

    # Cell size under which the grid axis label zone is no longer displayed
    AXIS_HIDE_CELL_SIZE_LIMIT = 11

    GRID_COORD_MARGIN_SIZE = 20  # 20 Windows, 40 Android
    GRID_AXIS_FONT_SIZE = 12

    GRID_MOVE_INCREMENT = 1

    DEFAULT_DATA_PATH_IOS = '~/Documents'

    CONFIG_KEY_REFERENCE_CURRENCY = 'referencecurrency'
    DEFAULT_REFERENCE_CURRENCY = 'USD'

    CONFIG_KEY_LOAD_AT_START_PATH_FILENAME = 'loadatstartpathfilename'
    DEFAULT_LOAD_AT_START_PATH_FILENAME = 'griddata.csv'

    CONFIG_KEY_APP_SIZE = 'defaultappsize'
    DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION = '0.56'

    DEFAULT_CONFIG_KEY_ACTIVE_CELL_COLOR_ANDROID = '90'

    CONFIG_KEY_APP_SIZE_HALF_PROPORTION = 'appsizehalfproportion'
    APP_SIZE_HALF = 'Half'
    APP_SIZE_FULL = 'Full'

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
                self.__gridWidth = self.DEFAULT_GRID_WIDTHe_ANDROID
            else:
                self.__gridWidth = self.DEFAULT_GRID_WIDTHe_WINDOWS
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
            self.__loadAtStartPathFilename = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME]
        except KeyError:
            self.__loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
            self._updated = True

        try:
            self.__fps = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_FPS]
        except KeyError:
            self.__fps = self.DEFAULT_FPS
            self._updated = True

        try:
            self.__activeCellColor = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_ACTIVE_CELL_COLOR]
        except KeyError:
            self.__activeCellColor = self.DEFAULT_ACTIVE_CELL_COLOR
            self._updated = True

        try:
            self.__appSize = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_APP_SIZE]
        except KeyError:
            self.__appSize = self.APP_SIZE_HALF
            self._updated = True

        try:
            self.__appSizeHalfProportion = self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION]
        except KeyError:
            self.__appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
            self._updated = True

        try:
            self.__referenceCurrency = self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_REFERENCE_CURRENCY]
        except KeyError:
            self.__referenceCurrency = self.DEFAULT_REFERENCE_CURRENCY
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

        if os.name == 'posix':
            self.gridWidth = self.DEFAULT_GRID_WIDTH_ANDROID
            self.gridHeight = self.DEFAULT_GRID_HEIGHT_ANDROID
            self.appSize = self.APP_SIZE_HALF
        else:
            self.gridWidth = self.DEFAULT_GRID_WIDTH_WINDOWS
            self.gridHeight = self.DEFAULT_GRID_HEIGHT_WINDOWS
            self.appSize = self.APP_SIZE_FULL

        self.activeCellColor = self.DEFAULT_ACTIVE_CELL_COLOR
        self.loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
        self.fps = self.DEFAULT_FPS
        self.appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
        self.referenceCurrency = self.DEFAULT_REFERENCE_CURRENCY
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
    def appSize(self):
        return self.__appSize

    @appSize.setter
    def appSize(self, appSizeStr):
        self.__appSize = appSizeStr
        self._updated = True


    @property
    def appSizeHalfProportion(self):
        return self.__appSizeHalfProportion

    @appSizeHalfProportion.setter
    def appSizeHalfProportion(self, appSizeHalfProportionStr):
        self.__appSizeHalfProportion = appSizeHalfProportionStr
        self._updated = True


    @property
    def referenceCurrency(self):
        return self.__referenceCurrency

    @referenceCurrency.setter
    def referenceCurrency(self, referenceCurrencyStr):
        self.__referenceCurrency = referenceCurrencyStr
        self._updated = True


    def storeConfig(self):
        if not self._updated:
            return

        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_TITLE] = self.windowTitle
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_WINDOW_LOCATION] = self.windowLocation
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_WIDTH] = self.gridWidth
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_GRID_HEIGHT] = self.gridHeight
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.loadAtStartPathFilename
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_FPS] = self.fps
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_ACTIVE_CELL_COLOR] = self.activeCellColor
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_APP_SIZE] = self.appSize
        self.config[self.CONFIG_SECTION_GRID_LAYOUT][self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION] = self.appSizeHalfProportion
        self.config[self.CONFIG_SECTION_VIEW_LAYOUT][self.CONFIG_KEY_REFERENCE_CURRENCY] = self.referenceCurrency

        self.config.write()
        
        self._updated = False


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

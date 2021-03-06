import pygame as pg

from centercell import CenterCell
from griddatamanager import GridDataManager
from cell import Cell
from bordercell import BorderCell

GRID_LINE_COLOR_BLACK = (0, 0, 0)

# Since one cell can occupy a minimum of 1 px and the grid line width
# is 1 px at the minimum, 2 cells will require at least 1 + 1 + 1 + 1 + 1 = 5 px.
# 3 cells require at least 1 + 1 + 1 + 1 + 1 + 1 + 1 = 7 px.
# n cells require at least 1 + (n * 2) px. This explains that the smallest possible
# cell constant SMALLEST_CELL_REQUIRED_PX_NUMBER is 2 pixels.
SMALLEST_CELL_REQUIRED_PX_NUMBER = 2

class GridView():

    def __init__(self, surface, configManager):
        self.changed = True
        self.surface = surface
        self.configMgr = configManager
        self.cellSize = configManager.defaultCellSize
        self.activeCellColor = configManager.activeCellColor
        self.gridLineWidth = configManager.gridLineWidth
        self.cellSizeOffset = configManager.cellSizeOffset
        self.gridDataMgr = GridDataManager(configManager=configManager)
        self.gridCoordMarginSize = configManager.gridCoordMarginSize
        self.gridCoordMarginHideCellSizeLimit = configManager.gridCoordMarginHideCellSizeLimit
#        self. = configManager.

        # varinst storing the number of row/col number that can be displayed in function
        # of the cell size which depends of the zoom in/out level. Their values are set
        # by the setGridDimension() method.
        self.gridViewDisplayableColNb = 0
        self.gridViewDisplayableRowNb = 0

        self.setGridDimension()

        # the max horz and vert cell number is set as below
        self.horizontalMaxManagedCellNumber = (surface.get_width())
        self.verticalMaxManagedCellNumber = (surface.get_height())

        self.cellValueGrid = None

        self.font = pg.font.SysFont('arial', configManager.gridAxisFontSize, False)
        self.drawAxisLabel = True

        # when opening the grid windows, the visible part of the cells is set at the very
        # left and very top. This means that the self.gridOffsetXPx and self.gridOffsetYPx
        # have a value of 0 pixel. When clicking on the left arrow, the self.gridOffsetXPx
        # will be subtracted the number of pixels set in the GRID_MOVE_INCREMENT constant.
        # On the contrary, pressing the right arrow will increment the self.gridOffsetXPx,
        # this up to 0. Same behavior for the up and down keys, respectively.
        self.gridOffsetXPx = 0
        self.gridOffsetYPx = 0

        self.startDrawRowIndex = 0
        self.startDrawColIndex = 0

    def setStartPattern(self):
        pass

    def setGridDimension(self):
        '''
        Sets the number of row/col number that can be displayed by the grid view. This
        number is function of the cell size which itself depends of the zoom in/out level
        (i.e. how many times the zoomIn()/zoomOut() methods were called.
        '''
        self.gridViewDisplayableColNb = (self.surface.get_width() - self.gridCoordMarginSize - self.gridLineWidth) // (self.cellSize + self.gridLineWidth)
        self.gridViewDisplayableRowNb = (self.surface.get_height() - self.gridCoordMarginSize - self.gridLineWidth) // (self.cellSize + self.gridLineWidth)

    def draw(self):
        drawnedRowNumber = self.gridViewDisplayableRowNb
        row = 0
        currentRowIndex = self.gridOffsetYPx // (self.cellSize + self.gridLineWidth)

        # for all the lines, drawing the y axis line number label and the horizontal line itself

        while row <= drawnedRowNumber:
            drawnedRowYCoord = self.gridCoordMarginSize - self.gridOffsetYPx + (currentRowIndex * (self.cellSize + self.gridLineWidth))

            if self.drawAxisLabel:
                if drawnedRowYCoord < self.gridCoordMarginSize // 2:
                    # this happens when the grid view is down shifted (down arrow or mouse down)
                    # so that more than half of the top most cell row is hidden. in this case,
                    # the row number is not written
                    pass
                else:
                    if currentRowIndex < 10:
                        ident = '  '
                    elif currentRowIndex < 100:
                        ident = ' '
                    else:
                        ident = ''

                    rowNumberLabel = self.font.render(ident + str(currentRowIndex), 1, (0, 0, 0))
                    self.surface.blit(rowNumberLabel, (0, drawnedRowYCoord))

            row += 1
            currentRowIndex += 1

            # drawing the row horizontal line

            if drawnedRowYCoord < self.gridCoordMarginSize:
                # We do not draw the line if its y coordinate is less than the grid
                # coordinates margin size. Since the line was skipped, it must be replaced
                # by a supplementary line at the bottom of the grid
                drawnedRowNumber += 1
                continue
            else:
                pg.draw.line(self.surface, GRID_LINE_COLOR_BLACK, (self.gridCoordMarginSize, drawnedRowYCoord), (self.surface.get_width(), drawnedRowYCoord), self.gridLineWidth)

        # for all the columns, drawing the x axis column label and the column vertical line itself

        drawnedColNumber = self.gridViewDisplayableColNb
        col = 0
        currentColIndex = self.gridOffsetXPx // (self.cellSize + self.gridLineWidth)

        while col <= drawnedColNumber:
            drawnedColXCoord = self.gridCoordMarginSize - self.gridOffsetXPx + currentColIndex * (self.cellSize + self.gridLineWidth)

            # handling column number label

            if self.drawAxisLabel:
                if drawnedColXCoord < self.gridCoordMarginSize // 2:
                    # this happens when the grid view is right shifted (right arrow or mouse)
                    # so that more than half of the left most cells is hidden. Then, the col
                    # number is not written
                    pass
                else:
                    if currentColIndex < 10:
                        ident = '  '
                    elif currentColIndex < 100:
                        ident = ' '
                    else:
                        ident = ''
                    colNumberLabel = self.font.render(ident + str(currentColIndex), 1, (0, 0, 0))
                    self.surface.blit(colNumberLabel, (drawnedColXCoord, 1))

            col += 1
            currentColIndex += 1

            # drawing the column vertical line

            if drawnedColXCoord < self.gridCoordMarginSize:
                # We do not draw the column line if its x coordinate is less than the grid
                # coordinates margin size. Since the column was skipped, it must be replaced
                # by a supplementary column at the very right of the grid
                drawnedColNumber += 1
                continue
            else:
                pg.draw.line(self.surface, GRID_LINE_COLOR_BLACK, (drawnedColXCoord, self.gridCoordMarginSize), (drawnedColXCoord, self.surface.get_height()), self.gridLineWidth)

        # drawing active cells

        maxDrawnedRowIndex = min(self.verticalMaxManagedCellNumber, self.gridViewDisplayableRowNb + self.startDrawRowIndex + 2)
        maxDrawnedColIndex = min(self.horizontalMaxManagedCellNumber, self.startDrawColIndex + self.gridViewDisplayableColNb + 2)

        for row in range(self.startDrawRowIndex, maxDrawnedRowIndex):
            for col in range(self.startDrawColIndex, maxDrawnedColIndex):
                if self.cellValueGrid[row][col]:
                    # calculating active cell top left x coord

                    if col == self.startDrawColIndex or col == maxDrawnedColIndex - 1:
                        # current active cell is at the left or right grid view border and
                        # may have to be partially drawned
                        drawnedCellXCoord, drawnedCellWidth = BorderCell.computeBorderCellCoordAndSize(self, col, doComputeX=True)
                    else:
                        drawnedCellXCoord, drawnedCellWidth = Cell.computeBorderIndependentCellXCoord(self, col), self.cellSize

                    # calculating active cell top left y coord

                    if row == self.startDrawRowIndex or row == maxDrawnedRowIndex - 1:
                        # current active cell is at the top or bottom grid view border and
                        # may have to be partially drawned
                        drawnedCellYCoord, drawnedCellHeight = BorderCell.computeBorderCellCoordAndSize(self, row, doComputeX=False)
                    else:
                        drawnedCellYCoord, drawnedCellHeight = Cell.computeBorderIndependentCellYCoord(self, row), self.cellSize
                    pg.draw.rect(self.surface,
                                 self.activeCellColor,
                                 [drawnedCellXCoord - self.cellSizeOffset,
                                      drawnedCellYCoord - self.cellSizeOffset,
                                      drawnedCellWidth,
                                      drawnedCellHeight])

        self.changed = False

    def zoomIn(self):
        midCellBeforeZoom = CenterCell(self)
        delta = self.cellSize // 10
        if delta <= 0:
            delta = 1

        self.cellSize += delta

        if self.cellSize >= self.surface.get_height():
            self.cellSize -= delta

        if self.cellSize > self.gridCoordMarginHideCellSizeLimit:
            self.drawAxisLabel = True
            self.gridCoordMarginSize = self.gridCoordMarginSize

        self.setGridDimension()
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()

        zoomXOffset, zoomYOffset = midCellBeforeZoom.computeXYOffsetAfterZoom()

        self.moveViewRight(-zoomXOffset)
        self.moveViewDown(-zoomYOffset)

        self.changed = True
        print(self.cellSize)

    def zoomOut(self):
        midCellBeforeZoom = CenterCell(self)
        delta = self.cellSize // 10

        if delta <= 0:
            delta = 1

        if self.cellSize > SMALLEST_CELL_REQUIRED_PX_NUMBER:
            self.cellSize -= delta
            if self.cellSize <= self.gridCoordMarginHideCellSizeLimit:
                self.drawAxisLabel = False
                self.gridCoordMarginSize = 0

        # repositionning the display horizontaly so that only editable cells (cells in
        # self.cellValueGrid) are displayed, preventing to set a cell value on a cell
        # which does not exists, which would cause an IndexOutOfRange exception.
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()

        if self.gridOffsetXPx > maxAllowedOffsetXPx:
            self.gridOffsetXPx = maxAllowedOffsetXPx - 1

        # repositionning the display vertically so that only editable cells (cells in
        # self.cellValueGrid) are displayed, preventing to set a cell value on a cell
        # which does not exists, which would cause an IndexOutOfRange exception.
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if self.gridOffsetYPx > maxAllowedOffsetYPx:
            self.gridOffsetYPx = maxAllowedOffsetYPx - 1

        self.setGridDimension()
        self.updateStartDrawRowIndex()
        self.updateStartDrawColIndex()

        zoomXOffset, zoomYOffset = midCellBeforeZoom.computeXYOffsetAfterZoom()
        self.moveViewLeft(zoomXOffset)
        self.moveViewUp(zoomYOffset)

        self.changed = True

    def move(self, xOffset, yOffset):
        if xOffset > 0:
            self.moveViewLeft(xOffset)
        elif xOffset < 0:
            self.moveViewRight(-xOffset)

        if yOffset > 0:
            self.moveViewUp(yOffset)
        elif yOffset < 0:
            self.moveViewDown(-yOffset)

    def moveViewDown(self, pixels):
        newGridYOffset = self.gridOffsetYPx + pixels
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if newGridYOffset >= maxAllowedOffsetYPx:
            #preventing from moving behond grid height. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            return

        self.gridOffsetYPx = newGridYOffset
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewToTop(self):
        '''
        Resets to the top most (0) row.
        '''
        self.gridOffsetYPx = 0
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewUp(self, pixels):
        self.gridOffsetYPx -= pixels
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()

        if self.gridOffsetYPx < 0:
            self.gridOffsetYPx = 0
        elif self.gridOffsetYPx > maxAllowedOffsetYPx:
            # this can happen when zooming out and recentring the displayed zone
            self.gridOffsetYPx = maxAllowedOffsetYPx

        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewToBottom(self):
        '''
        Sets the display to the right most or end column.
        '''
        maxAllowedOffsetYPx = self.computeMaxAllowedVerticalOffsetPx()
        self.gridOffsetYPx = maxAllowedOffsetYPx - 1
        self.updateStartDrawRowIndex()
        self.changed = True

    def moveViewRight(self, pixels):
        newGridXOffsetPx = self.gridOffsetXPx + pixels
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()
        if newGridXOffsetPx >= maxAllowedOffsetXPx:
            #preventing from moving behond grid width. This avoids changing a cell value
            #for a cell outside of the internal cell value grid
            return

        self.gridOffsetXPx = newGridXOffsetPx
        self.updateStartDrawColIndex()
        self.changed = True

    def moveViewToRightEnd(self):
        '''
        Sets the display to the right most or end column.
        '''
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()
        self.gridOffsetXPx = maxAllowedOffsetXPx - 1
        self.updateStartDrawColIndex()
        self.changed = True

    def computeMaxAllowedHorizontalOffsetPx(self):
        '''
        Calculates the maximum possible horizontal offset in pixels so that only columns which exist in the internal
        2 dimensions cell grid table are displayed.

        :return: maximum possible horizontal offset in px
        '''
        # calculate the pixel number required to draw a cell plus one grid line
        cellPlusSideWidthPxNumber = self.cellSize + self.gridLineWidth

        # calculate how many cells can be drawned in the cell display zone
        displayableCellNumber = (self.surface.get_width() - self.gridLineWidth - self.gridCoordMarginSize) / \
                                cellPlusSideWidthPxNumber

        # determine the max allowed horizontal offset in pixels according to how many cells
        # are available in the internal cell table for drawing. If we try to draw more cells,
        # we will get an out of range exception when we try to access a cell in the internal
        # cell table which does not exist (is beyhond the maximal available horizontal (x) cell number)
        maxAllowedHorizontalOffsetPx = ((self.horizontalMaxManagedCellNumber - displayableCellNumber) *
                                        cellPlusSideWidthPxNumber) - self.gridLineWidth

        return int(maxAllowedHorizontalOffsetPx)

    def computeMaxAllowedVerticalOffsetPx(self):
        '''
        Calculates the maximum possible vertical offset in pixels so that only rows which exist in the internal
        2 dimensions cell grid table are displayed.

        :return: maximum possible vertical offset in px
        '''
        # calculate the pixel number required to draw a cell plus one grid line
        cellPlusSideHeightPxNumber = self.cellSize + self.gridLineWidth

        # calculate how many cells can be drawned in the cell display zone
        displayableCellNumber = (self.surface.get_height() - self.gridLineWidth - self.gridCoordMarginSize) / \
                                cellPlusSideHeightPxNumber

        # determine the max allowed vertical offset in pixels according to how many cells
        # are available in the internal cell table for drawing. If we try to draw more cells,
        # we will get an out of range exception when we try to access a cell in the internal
        # cell table which does not exist (is beyhond the maximal available vertical (y) cell number)
        maxAllowedVerticalOffsetPx = ((self.verticalMaxManagedCellNumber - displayableCellNumber) *
                                        cellPlusSideHeightPxNumber) - self.gridLineWidth

        return int(maxAllowedVerticalOffsetPx)

    def moveViewLeft(self, pixels):
        self.gridOffsetXPx -= pixels
        maxAllowedOffsetXPx = self.computeMaxAllowedHorizontalOffsetPx()

        if self.gridOffsetXPx < 0:
            self.gridOffsetXPx = 0
        elif self.gridOffsetXPx > maxAllowedOffsetXPx:
            # this can happen when zooming out and recentring the displayed zone
            self.gridOffsetXPx = maxAllowedOffsetXPx

        self.updateStartDrawColIndex()
        self.changed = True

    def moveViewToLeftHome(self):
        '''
        Resets to the left most (0) column.
        '''
        self.gridOffsetXPx = 0
        self.updateStartDrawColIndex()
        self.changed = True

    def updateStartDrawColIndex(self):
        '''
        Updates the index of the first drawned column. When the grid window is started,
        self.gridOffsetXPx has value 0. This means that the left most drawned cell obtained
        from the internal self.cellValueGrid two dimensional table has an x index value of 0.

        When moving the displayed cell portion to the left, the left most displayed cell
        column x index will become 1, then 2, etc, i.e. the positive value of the
        self.gridOffsetXPx integer divided by the current cell width + grid line width.
        '''
        self.startDrawColIndex = self.gridOffsetXPx // (self.cellSize + self.gridLineWidth)

    def updateStartDrawRowIndex(self):
        '''
        Updates the index of the first drawned row. When the grid window is started,
        self.gridOffsetXYx has value 0. This means that the top most drawned cell obtained
        from the internal self.cellValueGrid two dimensional table has a y index value of 0.

        When moving up the displayed cell portion, the top most displayed cell
        row y index will become 1, then 2, etc, i.e. the positive value of the
        self.gridOffsetYPx integer divided by the current cell height + grid line width.
        '''
        self.startDrawRowIndex = self.gridOffsetYPx // (self.cellSize + self.gridLineWidth)

    def toggleCell(self, xyMousePosTuple):
        x, y = xyMousePosTuple
        col = (x - self.gridCoordMarginSize - self.gridLineWidth + self.gridOffsetXPx) // (self.gridLineWidth + self.cellSize)
        row = (y - self.gridCoordMarginSize - self.gridLineWidth + self.gridOffsetYPx) // (self.gridLineWidth + self.cellSize)

        if self.cellValueGrid[row][col]:
            self.cellValueGrid[row][col] = 0
        else:
            self.cellValueGrid[row][col] = 1

        self.changed = True

    def saveGridData(self):
        self.gridDataMgr.writeGridData(self.cellValueGrid)

    def loadGridData(self):
        '''
        Loads the grid data. If load successful, returns None. If the file was not found, returns the missing
        file name.

        :return: None if ok, missing file name if not.
        '''
        gridTable, fileNotFoundName = self.gridDataMgr.readGridData(requiredDimX=self.horizontalMaxManagedCellNumber,
                                                                    requiredDimY=self.verticalMaxManagedCellNumber)

        if gridTable:
            self.cellValueGrid = gridTable

        return fileNotFoundName

    def initialiseCellsToValue(self, value=0):
        '''
        Sets all cells of the internal cell value grid to the initial value defined at GFrid
        construction.
        :param value: must be 0 (dead) or 1 (alive)
        '''
        self.initCellValue = value
        self.cellValueGrid = [[value for i in range(self.horizontalMaxManagedCellNumber)] for j in range(self.verticalMaxManagedCellNumber)]

